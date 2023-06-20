#include "tcp.h"
#include "tcp_sock.h"
#include "tcp_timer.h"

#include "log.h"
#include "ring_buffer.h"

#include <stdlib.h>

// handling incoming packet for TCP_LISTEN state
//
// 1. malloc a child tcp sock to serve this connection request; 
// 2. send TCP_SYN | TCP_ACK by child tcp sock;
// 3. hash the child tcp sock into established_table (because the 4-tuple 
//    is determined).
static void tcp_state_listen(struct tcp_sock *tsk, struct tcp_cb *cb, char *packet)
{
	log(DEBUG, "in tcp_state_listen function.");

	if ((cb->flags & TCP_RST) || !(cb->flags & TCP_SYN))
		goto drop;

	if (cb->flags & TCP_ACK) {
		tcp_send_reset(cb);
		goto drop;
	}

	struct tcp_sock *child_tsk = alloc_tcp_sock();
	if (!child_tsk) {
		log(ERROR, "malloc tcp child sock failed.");
		goto drop;
	}

	tcp_set_state(child_tsk, TCP_SYN_RECV);
	child_tsk->sk_sip = cb->daddr;
	child_tsk->sk_dip = cb->saddr;
	child_tsk->sk_sport = cb->dport;
	child_tsk->sk_dport = cb->sport;

	if (tcp_hash(child_tsk) < 0) {
		free(child_tsk);
		goto drop;
	}

	child_tsk->parent = tsk;
	list_add_head(&child_tsk->list, &tsk->listen_queue);

	child_tsk->iss = tcp_new_iss();
	child_tsk->rcv_nxt = cb->seq_end;

	child_tsk->snd_una = child_tsk->iss;
	child_tsk->snd_nxt = child_tsk->iss;

	tcp_send_control_packet(child_tsk, TCP_SYN|TCP_ACK);

drop:
	return ;
}

// handling incoming packet for TCP_CLOSED state, by replying TCP_RST
static void tcp_state_closed(struct tcp_sock *tsk, struct tcp_cb *cb, char *packet)
{
	tcp_send_reset(cb);
}

// handling incoming packet for TCP_SYN_SENT state
//
// If everything goes well (the incoming packet is TCP_SYN|TCP_ACK), reply with 
// TCP_ACK, and enter TCP_ESTABLISHED state, notify tcp_sock_connect; otherwise, 
// reply with TCP_RST.
static void tcp_state_syn_sent(struct tcp_sock *tsk, struct tcp_cb *cb, char *packet)
{
	if (cb->flags & TCP_ACK) {
		if (less_or_equal_32b(cb->ack, tsk->iss) || greater_than_32b(cb->ack, tsk->snd_nxt)) {
			tcp_send_reset(cb);
			goto drop;
		}
	}

	if (cb->flags & TCP_RST) {
		tcp_set_state(tsk, TCP_CLOSED);

		wake_up(tsk->wait_connect);

		goto drop;
	}

	if (cb->flags & TCP_SYN) {
		tsk->rcv_nxt = cb->seq_end;
		if (cb->flags & TCP_ACK) 
			tsk->snd_una = cb->ack;
		if (greater_than_32b(tsk->snd_una, tsk->iss)) {
			tcp_set_state(tsk, TCP_ESTABLISHED);

			tsk->snd_wnd = cb->rwnd;

			tcp_send_control_packet(tsk, TCP_ACK);
			wake_up(tsk->wait_connect);
		}
		else {
			// TODO: remove the following three lines
			tcp_set_state(tsk, TCP_SYN_RECV);
			tcp_send_control_packet(tsk, TCP_SYN|TCP_ACK);

			tcp_start_timer(&tsk->retrans_timer, TCP_RETRANS_TIMER, TCP_RETRANS_TIMEOUT);

			return ;
		}
	}

drop:
	return ;
}

// update the snd_wnd of tcp_sock
//
// if the snd_wnd before updating is zero, notify tcp_sock_send (wait_send)
static inline void tcp_update_window(struct tcp_sock *tsk, struct tcp_cb *cb)
{
	u16 old_snd_wnd = tsk->snd_wnd;
	tsk->snd_wnd = cb->rwnd;
	if (old_snd_wnd == 0)
		wake_up(tsk->wait_send);
}

// update the snd_wnd safely: cb->ack should be between snd_una and snd_nxt
static inline void tcp_update_window_safe(struct tcp_sock *tsk, struct tcp_cb *cb)
{
	if (less_or_equal_32b(tsk->snd_una, cb->ack) && less_or_equal_32b(cb->ack, tsk->snd_nxt))
		tcp_update_window(tsk, cb);
}

// handling incoming ack packet for tcp sock in TCP_SYN_RECV state
//
// 1. remove itself from parent's listen queue;
// 2. add itself to parent's accept queue;
// 3. wake up parent (wait_accept) since there is established connection in the
//    queue.
static void tcp_state_syn_recv(struct tcp_sock *tsk, struct tcp_cb *cb, char *packet)
{
	if (!(less_or_equal_32b(tsk->snd_una, cb->ack) && less_or_equal_32b(cb->ack, tsk->snd_nxt))) {
		tcp_send_reset(cb);
		goto drop;
	}

	if (!list_empty(&tsk->list)) {
		list_delete_entry(&tsk->list);
	}

	if (tsk->parent->state != TCP_LISTEN)
		goto drop;

	if (tcp_sock_accept_queue_full(tsk->parent))
		goto drop;

	tsk->snd_una = cb->ack;
	tcp_update_window(tsk, cb);
	tcp_set_state(tsk, TCP_ESTABLISHED);

	tcp_sock_accept_enqueue(tsk);

	wake_up(tsk->parent->wait_accept);

drop:
	return ;
}

#ifndef max
#	define max(x,y) ((x)>(y) ? (x) : (y))
#endif

// check whether the sequence number of the incoming packet is in the receiving
// window
static inline int is_tcp_seq_valid(struct tcp_sock *tsk, struct tcp_cb *cb)
{
	u32 rcv_end = tsk->rcv_nxt + max(tsk->rcv_wnd, 1);
	if (less_than_32b(cb->seq, rcv_end) && less_or_equal_32b(tsk->rcv_nxt, cb->seq_end)) {
		return 1;
	}
	else {
		log(ERROR, "received packet with invalid seq rcv_nxt = %u, "
				"seq = %u, seq_end = %u, drop it.", tsk->rcv_nxt, cb->seq, cb->seq_end);
		return 0;
	}
}

// put the payload of the incoming packet into rcv_buf, and notify the
// tcp_sock_read (wait_recv)
int tcp_recv_data(struct tcp_sock *tsk, struct tcp_cb *cb, char *packet)
{
	if (!tsk->rcv_wnd) {
		log(ERROR, "receive data when receiving window is zero.");
		return 0;
	}

	// we have received part of the data in this packet.
	if (greater_than_32b(tsk->rcv_nxt, cb->seq)) {
		log(ERROR, "tsk->rcv_nxt is greater than cb->seq.");
		if (greater_or_equal_32b(tsk->rcv_nxt, cb->seq + cb->pl_len)) {
			log(ERROR, "received packet which has already been ACKed.");
			return 0;
		}

		int adv = (tsk->rcv_nxt - cb->seq);
		cb->seq += adv;
		cb->payload += adv;
		cb->pl_len -= adv; 
	}

	int len = cb->pl_len;
	if (tsk->rcv_nxt == cb->seq && ring_buffer_free(tsk->rcv_buf) >= len) {
		write_ring_buffer(tsk->rcv_buf, cb->payload, len);
		tsk->rcv_nxt += len;
		tsk->rcv_wnd -= len;

		wake_up(tsk->wait_recv);
	}
	else {
		log(ERROR, "could not put the data into ring buffer." 
				"rcv_nxt = %u, cb->seq = %u, buf_size = %d, pl_len = %d.", \
				tsk->rcv_nxt, cb->seq, ring_buffer_free(tsk->rcv_buf), len);
	}

	return 1;
}

// Process an incoming packet as follows:
// 	 1. if the state is TCP_CLOSED, hand the packet over to tcp_state_closed;
// 	 2. if the state is TCP_LISTEN, hand it over to tcp_state_listen;
// 	 3. if the state is TCP_SYN_SENT, hand it to tcp_state_syn_sent;
// 	 4. check whether the sequence number of the packet is valid, if not, drop
// 	    it;
// 	 5. if the TCP_RST bit of the packet is set, close this connection, and
// 	    release the resources of this tcp sock;
// 	 6. if the TCP_SYN bit is set, reply with TCP_RST and close this connection,
// 	    as valid TCP_SYN has been processed in step 2 & 3;
// 	 7. check if the TCP_ACK bit is set, since every packet (except the first 
//      SYN) should set this bit;
//   8. process the ack of the packet: if it ACKs the outgoing SYN packet, 
//      establish the connection; if it ACKs new data, update the window;
//      if it ACKs the outgoing FIN packet, switch to correpsonding state;
//   9. process the payload of the packet: call tcp_recv_data to receive data;
//  10. if the TCP_FIN bit is set, update the TCP_STATE accordingly;
//  11. at last, do not forget to reply with TCP_ACK if the connection is alive.
void tcp_process(struct tcp_sock *tsk, struct tcp_cb *cb, char *packet)
{
	char buf[32];
	tcp_copy_flags_to_str(cb->flags, buf);
	// log(DEBUG, "received tcp packet %s.", buf);

	int send_ack = 0;

	if (!tsk)
		return tcp_state_closed(tsk, cb, packet);

	pthread_mutex_lock(&tsk->lock);

	if (tsk->state == TCP_CLOSED) {
		tcp_state_closed(tsk, cb, packet);
		goto end;
	}

	if (tsk->state == TCP_LISTEN) {
		tcp_state_listen(tsk, cb, packet);
		goto end;
	}

	if (tsk->state == TCP_SYN_SENT) {
		tcp_state_syn_sent(tsk, cb, packet);
		goto end;
	}

	if (tsk->state == TCP_SYN_RECV) {
		tcp_state_syn_recv(tsk, cb, packet);
		goto end;
	}

	if (!is_tcp_seq_valid(tsk, cb)) 
		goto end;

	if (cb->flags & TCP_RST) {
		switch (tsk->state) {
			case TCP_SYN_RECV:
				if (! tsk->parent) {
					if (tsk->wait_connect)
						wake_up(tsk->wait_connect);
				}
				break;
			default:
				break;
		}

		tcp_set_state(tsk, TCP_CLOSED);
		tcp_unhash(tsk);
		goto end;
	}

	if (cb->flags & TCP_SYN) {
		// not in LISTEN or SYN_SENT state
		tcp_send_reset(cb);

		if (tsk->state == TCP_SYN_RECV && tsk->parent)
			tcp_unhash(tsk);
		tcp_set_state(tsk, TCP_CLOSED);
		free_tcp_sock(tsk);

		goto end;
	}

	if (!(cb->flags & TCP_ACK)) {
		// each ``normal'' packet should set TCP_ACK bit
		goto end;
	}

	switch (tsk->state) {

		case TCP_ESTABLISHED:
		case TCP_CLOSE_WAIT:
		case TCP_LAST_ACK:
		case TCP_FIN_WAIT_1:
		case TCP_CLOSING:
			if (less_than_32b(tsk->snd_una, cb->ack) && less_or_equal_32b(cb->ack, tsk->snd_nxt)) {
				tsk->snd_una = cb->ack;

				if (tsk->state == TCP_FIN_WAIT_1) {
					tcp_set_state(tsk, TCP_FIN_WAIT_2);
				}
				else if (tsk->state == TCP_CLOSING) {
					tcp_set_state(tsk, TCP_TIME_WAIT);
					tcp_start_timer(&tsk->timewait, TCP_TIMEWAIT_TIMER, TCP_TIMEWAIT_TIMEOUT);
					goto end;
				}
				else if (tsk->state == TCP_LAST_ACK) {
					tcp_set_state(tsk, TCP_CLOSED);
					tcp_unhash(tsk);
					goto end;
				}
			}
			else if (greater_than_32b(cb->ack, tsk->snd_nxt)) {
				log(ERROR, "received tcp packet with ack (%x) greater than snd_nxt (%x).", \
						cb->ack, tsk->snd_nxt);
				goto end;
			}
			else if (cb->ack <= tsk->snd_una) {
				// ignore this duplicate ACK, and do not drop the packet
			}
			tcp_update_window_safe(tsk, cb);
			break;

		default:
			// case TCP_FIN_WAIT_2 and TCP_TIME_WAIT
			break;
	}

	if (cb->flags & TCP_URG) {
		log(WARNING, "received tcp packet with TCP_URG flag, to be implemented.");
	}

	switch (tsk->state) {
		case TCP_ESTABLISHED:
		case TCP_FIN_WAIT_1:
		case TCP_FIN_WAIT_2:
			if (cb->pl_len > 0) {
				send_ack = tcp_recv_data(tsk, cb, packet);
			}

			break;
	}

	if (cb->flags & TCP_FIN) {
		switch (tsk->state) {
			case TCP_SYN_RECV:
			case TCP_ESTABLISHED:
				tcp_set_state(tsk, TCP_CLOSE_WAIT);
				wake_up(tsk->wait_recv);
				break;
			case TCP_FIN_WAIT_1:
				tcp_set_state(tsk, TCP_CLOSING);
				break;
			case TCP_CLOSE_WAIT:
			case TCP_CLOSING:
			case TCP_LAST_ACK:
				break;
			case TCP_TIME_WAIT:
				tsk->timewait.timeout = TCP_TIMEWAIT_TIMEOUT;
				break;
			case TCP_FIN_WAIT_2:
				tcp_start_timer(&tsk->timewait, TCP_TIMEWAIT_TIMER, TCP_TIMEWAIT_TIMEOUT);
				break;
		}

		send_ack = 1;
	}

	tsk->rcv_nxt = cb->seq_end;

end:
	if (send_ack)
		tcp_send_control_packet(tsk, TCP_ACK);

	pthread_mutex_unlock(&tsk->lock);
}
