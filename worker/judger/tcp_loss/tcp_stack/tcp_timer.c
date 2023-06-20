#include "tcp.h"
#include "tcp_timer.h"
#include "tcp_sock.h"

#include <unistd.h>
#include <stdio.h>

#include "utils.h"

static struct list_head timer_list;

extern int tcp_retrans_packet(struct tcp_sock *tsk);

void tcp_init_timer(struct tcp_timer *timer)
{
	init_list_head(&timer->list);
}

void tcp_start_timer(struct tcp_timer *timer, int type, int timeout)
{
	fprintf(stdout, "set timer, now: %.6lf, type = %d, timeout = %d.\n", time_now(), type, timeout);
	timer->type = type;
	timer->timeout = timeout;
	timer->elapsed = 0;
	list_add_tail(&timer->list, &timer_list);
}

void tcp_reset_timer(struct tcp_timer *timer, int timeout)
{
	struct list_head *list = &timer->list;
	assert(list->next != list);

	timer->timeout = timeout;
	timer->elapsed = 0;
}

void tcp_stop_timer(struct tcp_timer *timer)
{
	list_delete_entry(&timer->list);
}

void tcp_retrans_timer_fires(struct tcp_sock * tsk)
{
	fprintf(stdout, "retrans timer fires, now = %.6lf.\n", time_now());
	// if (tcp_retrans_packet(tsk) < 0) {
	// 	// TODO: terminate this flow
	// 	fprintf(stdout, "TODO: terminate this flow.\n");
	// }
}

// scan the timer_list, find the tcp sock which stays for at 2*MSL, release it
void tcp_scan_timer_list(int elapsed)
{
	struct tcp_sock *tsk;
	struct tcp_timer *t, *q;
	list_for_each_entry_safe(t, q, &timer_list, list) {
		t->elapsed += elapsed;
		if (t->timeout <= t->elapsed) {
			if (t->type == TCP_TIMEWAIT_TIMER) {
				tcp_stop_timer(t);

				tsk = timewait_to_tcp_sock(t);
				if (! tsk->parent)
					tcp_bind_unhash(tsk);
				tcp_set_state(tsk, TCP_CLOSED);
				free_tcp_sock(tsk);
			}
			else if (t->type == TCP_RETRANS_TIMER) {
				tcp_reset_timer(t, t->timeout * 2);

				tsk = retrans_timer_to_tcp_sock(t);

				tcp_retrans_timer_fires(tsk);
			}
		}
	}
}

#if 0
// set the timewait timer of a tcp sock, by adding the timer into timer_list
void tcp_set_timewait_timer(struct tcp_sock *tsk)
{
	struct tcp_timer *timer = &tsk->timewait;

	timer->type = TCP_TIMEWAIT_TIMER;
	timer->timeout = TCP_TIMEWAIT_TIMEOUT;
	list_add_tail(&timer->list, &timer_list);

	tcp_sock_inc_ref_cnt(tsk);
}

void tcp_set_retrans_timer(struct tcp_sock *tsk)
{
	struct tcp_timer *timer = &tsk->retrans_timer;
	timer->type = TCP_RETRANS_TIMER;
	timer->timeout = TCP_RETRANS_TIMEOUT;
	list_add_tail(&timer->list, &timer_list);

	tcp_sock_inc_ref_cnt(tsk);
}

void tcp_reset_retrans_timer(struct tcp_sock *tsk)
{
	struct tcp_timer *timer = &tsk->retrans_timer;
	timer->timeout = TCP_RETRANS_TIMEOUT;
}

void tcp_del_retrans_timer(struct tcp_sock *tsk)
{
	struct tcp_timer *timer = &tsk->retrans_timer;
	list_delete_entry(&timer->list);

	tcp_sock_dec_ref_cnt(tsk);
}
#endif

// scan the timer_list periodically by calling tcp_scan_timer_list
void *tcp_timer_thread(void *arg)
{
	init_list_head(&timer_list);
	while (1) {
		usleep(TCP_TIMER_SCAN_INTERVAL);
		tcp_scan_timer_list(TCP_TIMER_SCAN_INTERVAL);
	}

	return NULL;
}
