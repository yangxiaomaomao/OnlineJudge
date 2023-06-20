#ifndef __TCP_TIMER_H__
#define __TCP_TIMER_H__

#include "list.h"

#include <stddef.h>

#define TCP_TIMEWAIT_TIMER 0
#define TCP_RETRANS_TIMER 1

struct tcp_timer {
	int type;		// time-wait or retrans
	int timeout;	// in microsecond
	int elapsed;	// in microsecond
	struct list_head list;
};

struct tcp_sock;
#define timewait_to_tcp_sock(t) \
	(struct tcp_sock *)((char *)(t) - offsetof(struct tcp_sock, timewait))
#define retrans_timer_to_tcp_sock(t) \
	(struct tcp_sock *)((char *)(t) - offsetof(struct tcp_sock, retrans_timer))

#define TCP_TIMER_SCAN_INTERVAL 1000		// 1ms
#define TCP_MSL			1000000				// 1s
#define TCP_TIMEWAIT_TIMEOUT	(2 * TCP_MSL)
#define TCP_RETRANS_TIMEOUT		200000		// 200ms

// the thread that scans timer_list periodically
void *tcp_timer_thread(void *arg);
// add the timer of tcp sock to timer_list
void tcp_init_timer(struct tcp_timer *timer);
void tcp_start_timer(struct tcp_timer *timer, int type, int timeout);
void tcp_reset_timer(struct tcp_timer *timer, int timeout);
void tcp_stop_timer(struct tcp_timer *timer);

#endif
