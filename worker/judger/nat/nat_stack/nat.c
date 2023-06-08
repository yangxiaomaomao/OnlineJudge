#include "nat.h"
#include "ip.h"
#include "icmp.h"
#include "tcp.h"
#include "rtable.h"
#include "log.h"

#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>

static struct nat_table nat;

// hash address and port
static int nat_hash(u32 addr, u16 port)
{
	int val = hash8((char *)&addr, 4) ^ hash8((char *)&port, 2);

	return val;
}

// check whether the flow is finished according to FIN bit and sequence number
static int is_flow_finished(struct nat_connection *conn)
{
	return (conn->internal_fin && conn->external_fin) && \
			(conn->internal_ack >= conn->external_seq_end) && \
			(conn->external_ack >= conn->internal_seq_end);
}

// get the interface from iface name
static iface_info_t *if_name_to_iface(const char *if_name)
{
	iface_info_t *iface = NULL;
	list_for_each_entry(iface, &instance->iface_list, list) {
		if (strcmp(iface->name, if_name) == 0)
			return iface;
	}

	log(ERROR, "could not find the desired interface according to if_name '%s'", if_name);
	return NULL;
}

static int entry_has_iface(rt_entry_t *entry, iface_info_t *iface)
{
	return (entry && entry->iface->index == iface->index);
}

// determine the direction of the packet, DIR_IN / DIR_OUT / DIR_INVALID
static int get_packet_direction(char *packet)
{
	struct iphdr *ip = packet_to_ip_hdr(packet);

	rt_entry_t *src_entry = longest_prefix_match(ntohl(ip->saddr)),
			   *dst_entry = longest_prefix_match(ntohl(ip->daddr));

	if (!entry_has_iface(src_entry, nat.internal_iface) && \
			(ntohl(ip->daddr) == nat.external_iface->ip))
		return DIR_IN;

	if (entry_has_iface(src_entry, nat.internal_iface) && \
			!entry_has_iface(dst_entry, nat.internal_iface))
		return DIR_OUT;

	return DIR_INVALID;
}

// lookup the corresponding map from mapping_list according to external_port
struct nat_mapping *nat_lookup_external(struct list_head *mapping_list, u16 external_port)
{
	pthread_mutex_lock(&nat.lock);

	struct nat_mapping *entry;
	list_for_each_entry(entry, mapping_list, list) {
		if (entry->external_port == external_port) {
			entry->update_time = time(NULL);
			goto out;
		}
	}

	entry = NULL;

out:
	pthread_mutex_unlock(&nat.lock);
	return entry;
}

// lookup the corresponding map from mapping_list according to internal_ip and
// internal_port
struct nat_mapping *nat_lookup_internal(struct list_head *mapping_list,
		u32 internal_ip, u16 internal_port)
{
	pthread_mutex_lock(&nat.lock);

	struct nat_mapping *entry;
	list_for_each_entry(entry, mapping_list, list) {
		if (entry->internal_ip == internal_ip && \
				entry->internal_port == internal_port) {
			entry->update_time = time(NULL);
			goto out;
		}
	}

	entry = NULL;

out:
	pthread_mutex_unlock(&nat.lock);
	return entry;
}

// select an external port from the port pool
static u16 assign_external_port()
{
	u16 port = 0;
	for (int i = NAT_PORT_MIN; i < NAT_PORT_MAX; i++) {
		if (nat.assigned_ports[i] == 0) {
			nat.assigned_ports[i] = 1;
			port = i;
			break;
		}
	}

	return port;
}

// free the port
static void free_port(u16 port)
{
	nat.assigned_ports[port] = 0;
}

// insert the new connection into mapping_list
struct nat_mapping *nat_insert_mapping(struct list_head *mapping_list, \
		u32 int_ip, u16 int_port, u32 ext_ip, u16 ext_port)
{
	pthread_mutex_lock(&nat.lock);

	struct nat_mapping *mapping = malloc(sizeof(*mapping));
	if (!mapping) {
		log(ERROR, "malloc nat_mappping failed.");
		goto out;
	}
	memset(mapping, 0, sizeof(*mapping));

	mapping->internal_ip = int_ip;
	mapping->internal_port = int_port;
	mapping->external_ip = ext_ip;
	mapping->external_port = ext_port;
	mapping->update_time = time(NULL);

	list_add_head(&mapping->list, mapping_list);

	pthread_mutex_unlock(&nat.lock);

out:
	return mapping;
}

// update statistics of the tcp connection
void nat_update_tcp_connection(char *packet, struct nat_mapping *mapping, int dir)
{
	struct iphdr *ip = packet_to_ip_hdr(packet);
	struct tcphdr *tcp = (struct tcphdr *)((char *)ip + IP_HDR_SIZE(ip));

	u32 seq_end = tcp->seq + (htons(ip->tot_len) - IP_HDR_SIZE(ip) - TCP_HDR_SIZE(tcp)) + \
				  ((tcp->flags & (TCP_SYN|TCP_FIN)) ? 1 : 0);
	u32	ack = ntohl(tcp->ack);

	pthread_mutex_lock(&nat.lock);

	mapping->update_time = time(NULL);
	struct nat_connection *conn = &mapping->conn;

	if (dir == DIR_IN) {
		if (tcp->flags & TCP_FIN)
			conn->external_fin = 1;

		if (conn->external_fin)
			conn->external_seq_end = seq_end;

		if (conn->internal_fin)
			conn->external_ack = ack;
	}
	else {
		if (tcp->flags & TCP_FIN)
			conn->internal_fin = 1;

		if (conn->internal_fin)
			conn->internal_seq_end = seq_end;

		if (conn->internal_fin)
			conn->internal_ack = ack;
	}

	if (conn->external_fin && conn->internal_fin) {
		// log(DEBUG, "received both fin packets for the flow.");
	}

	if ((tcp->flags & TCP_RST) || is_flow_finished(conn)) {
		free_port(mapping->external_port);
		list_delete_entry(&mapping->list);
		log(DEBUG, "delete fishished flow: ("IP_FMT":%d)", \
				HOST_IP_FMT_STR(mapping->internal_ip), mapping->internal_port);
		free(mapping);
	}

	pthread_mutex_unlock(&nat.lock);
}

struct dnat_rule *find_dnat_rule(u32 ext_ip, u16 ext_port)
{
	struct dnat_rule *entry = NULL, *q;
	list_for_each_entry_safe(entry, q, &(nat.rules), list) {
		if (ext_ip == entry->external_ip && ext_port == entry->external_port) {
			// log(DEBUG, "success:search dnat rule: ex %x:%x",external_ip,external_port);
			return entry;
		}
	}

	return NULL;
}

// find the mapping corresponding to the packet from nat table 
struct nat_mapping *nat_get_mapping_from_packet(char *packet, int len, iface_info_t *iface, int dir)
{
	struct iphdr *ip = packet_to_ip_hdr(packet);

	char *ip_data = (char *)ip + IP_HDR_SIZE(ip);
	struct tcphdr *tcp = (struct tcphdr *)ip_data;
	int hash = 0;
	struct list_head *mapping_list;
	struct nat_mapping *mapping = NULL;
	if (dir == DIR_IN) {
		u32 ext_ip = ntohl(ip->daddr);
		u16 ext_port = ntohs(tcp->dport);
		hash = nat_hash(ntohl(ip->saddr), ntohs(tcp->sport));
		mapping_list = &nat.nat_mapping_list[hash];
		mapping = nat_lookup_external(mapping_list, ext_port);
		if (!mapping) {
			if (tcp->flags != TCP_SYN) {
				log(ERROR, "could not get mapping for non-SYN ingoing packet.");
				goto out;
			}

			struct dnat_rule *rule = find_dnat_rule(ext_ip, ext_port);
			if (!rule) {
				log(ERROR, "could not find the dnat rule for ingoing SYN packet.");
				goto out;
			}

			u32 int_ip = rule->internal_ip;
			u16 int_port = rule->internal_port;
			mapping = nat_insert_mapping(mapping_list, int_ip, int_port, ext_ip, ext_port);
		}
	}
	else {
		u32 int_ip = ntohl(ip->saddr);
		u16 int_port = ntohs(tcp->sport);
		hash = nat_hash(ntohl(ip->daddr), ntohs(tcp->dport));
		mapping_list = &nat.nat_mapping_list[hash];
		mapping = nat_lookup_internal(mapping_list, int_ip, int_port);
		if (!mapping) {
			if (tcp->flags != TCP_SYN) {
				log(ERROR, "could not get mapping for non-SYN outgoing packet.");
				goto out;
			}

			u32 ext_ip = nat.external_iface->ip;
			u32 ext_port = assign_external_port();
			mapping = nat_insert_mapping(mapping_list, int_ip, int_port, ext_ip, ext_port);
		}
	}

out:
	return mapping;
}

// do translation for the packet: replace the ip/port, recalculate ip & tcp
// checksum, update the statistics of the tcp connection
void do_translation(iface_info_t *iface, char *packet, int len, int dir)
{
	struct iphdr *ip = packet_to_ip_hdr(packet);

	struct nat_mapping *mapping = nat_get_mapping_from_packet(packet, len, iface, dir);
	if (!mapping) {
		log(ERROR, "could not find mapping for the packet.");
		free(packet);
		return ;
	}

	ip = packet_to_ip_hdr(packet);

	struct tcphdr *tcp = (struct tcphdr *)((char *)ip + IP_HDR_SIZE(ip));
	if (dir == DIR_IN) {
		ip->daddr = htonl(mapping->internal_ip);
		tcp->dport = htons(mapping->internal_port);
	}
	else {
		ip->saddr = htonl(mapping->external_ip);
		tcp->sport = htons(mapping->external_port);
	}
	tcp->checksum = tcp_checksum(ip, tcp);
	ip->checksum = ip_checksum(ip);

	// after this function, the mapping entry may be removed if it's completed.
	nat_update_tcp_connection(packet, mapping, dir);

	ip_send_packet(packet, len);
}

void nat_translate_packet(iface_info_t *iface, char *packet, int len)
{
	int dir = get_packet_direction(packet);
	if (dir == DIR_INVALID) {
		log(ERROR, "invalid packet direction, drop it.");
		icmp_send_packet(packet, len, ICMP_DEST_UNREACH, ICMP_HOST_UNREACH);
		free(packet);
		return ;
	}

	struct iphdr *ip = packet_to_ip_hdr(packet);
	if (ip->protocol != IPPROTO_TCP) {
		log(ERROR, "received non-TCP packet (0x%0hhx), drop it", ip->protocol);
		free(packet);
		return ;
	}

	do_translation(iface, packet, len, dir);
}

// nat timeout thread: find the finished flows, remove them and free port
// resource
void *nat_timeout()
{
	while (1) {
		sleep(1);

		time_t now = time(NULL);
		pthread_mutex_lock(&nat.lock);

		for (int i = 0; i < HASH_8BITS; i++) {
			struct list_head *head = &nat.nat_mapping_list[i];
			struct nat_mapping *entry, *q;
			list_for_each_entry_safe(entry, q, head, list) {
				int delta = now - entry->update_time;
				if (is_flow_finished(&entry->conn) || delta >= TCP_ESTABLISHED_TIMEOUT) {
					free_port(entry->external_port);
					list_delete_entry(&entry->list);
					free(entry);
				}
			}
		}

		pthread_mutex_unlock(&nat.lock);
	}

	return NULL;
}

#define MAX_STR_SIZE 100
int get_next_line(FILE *input, char (*strs)[MAX_STR_SIZE], int *num_strings)
{
	const char *delim = " \t\n";
	char buffer[120];
	int ret = 0;
	if (fgets(buffer, sizeof(buffer), input)) {
		char *token = strtok(buffer, delim);
		*num_strings = 0;
		while (token) {
			strcpy(strs[(*num_strings)++], token);
			token = strtok(NULL, delim);
		}

		ret = 1;
	}

	return ret;
}

int read_ip_port(const char *str, u32 *ip, u16 *port)
{
	int i1, i2, i3, i4;
	int ret = sscanf(str, "%d.%d.%d.%d:%hu", &i1, &i2, &i3, &i4, port);
	if (ret != 5) {
		log(ERROR, "parse ip-port string error: %s.", str);
		exit(1);
	}

	*ip = (i1 << 24) | (i2 << 16) | (i3 << 8) | i4;

	return 0;
}

int parse_config(const char *filename)
{
	FILE *input;
	char strings[10][MAX_STR_SIZE];
	int num_strings;

	input = fopen(filename, "r");
	if (input) {
		while (get_next_line(input, strings, &num_strings)) {
			if (num_strings == 0)
				continue;

			if (strcmp(strings[0], "internal-iface:") == 0) {
				nat.internal_iface = if_name_to_iface(strings[1]);
			}
			else if (strcmp(strings[0], "external-iface:") == 0) {
				nat.external_iface = if_name_to_iface(strings[1]);
			}
			else if (strcmp(strings[0], "dnat-rules:") == 0) {
				struct dnat_rule *rule = (struct dnat_rule*)malloc(sizeof(struct dnat_rule));
				read_ip_port(strings[1], &rule->external_ip, &rule->external_port);
				read_ip_port(strings[3], &rule->internal_ip, &rule->internal_port);
				
				list_add_tail(&rule->list, &nat.rules);
			}
			else {
				log(ERROR, "incorrect config file, exit.");
				exit(1);
			}
		}

		fclose(input);
	}
	else {
		log(ERROR, "could not find config file '%s', exit.", filename);
		exit(1);
	}
	
	if (!nat.internal_iface || !nat.external_iface) {
		log(ERROR, "could not find the desired interfaces for nat.");
		exit(1);
	}

	return 0;
}

// initialize
void nat_init(const char *config_file)
{
	memset(&nat, 0, sizeof(nat));

	for (int i = 0; i < HASH_8BITS; i++)
		init_list_head(&nat.nat_mapping_list[i]);

	init_list_head(&nat.rules);

	// seems unnecessary
	memset(nat.assigned_ports, 0, sizeof(nat.assigned_ports));

	parse_config(config_file);

	pthread_mutex_init(&nat.lock, NULL);

	pthread_create(&nat.thread, NULL, nat_timeout, NULL);
}

void nat_exit()
{
	pthread_mutex_lock(&nat.lock);

	for (int i = 0; i < HASH_8BITS; i++) {
		struct list_head *head = &nat.nat_mapping_list[i];
		struct nat_mapping *mapping_entry, *q;
		list_for_each_entry_safe(mapping_entry, q, head, list) {
			list_delete_entry(&mapping_entry->list);
			free(mapping_entry);
		}
	}

	pthread_kill(nat.thread, SIGTERM);

	pthread_mutex_unlock(&nat.lock);
}
