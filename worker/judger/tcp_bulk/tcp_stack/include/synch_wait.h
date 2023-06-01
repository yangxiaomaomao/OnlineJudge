#ifndef __SYNCH_WAIT_H__
#define __SYNCH_WAIT_H__

#include <pthread.h>
#include <stdlib.h>

struct synch_wait {
	pthread_mutex_t *tsk_lock;	// lock of tcp sock
	pthread_cond_t cond;		// condition variable to synch
	int notified;				// whether ready to read/write
	int dead;					// whether dead
	int sleep;					// whether others are waiting
};

// initialize all the variables
static inline void wait_init(struct synch_wait *wait, pthread_mutex_t *lock)
{
	wait->tsk_lock = lock;
	pthread_cond_init(&wait->cond, NULL);
	wait->dead = 0;
	wait->notified = 0;
	wait->sleep = 0;
}

// exit and notify all others
static inline void wait_exit(struct synch_wait *wait)
{
	if (wait->dead)
		return ;
	wait->dead = 1;
	if (wait->sleep)
		pthread_cond_broadcast(&wait->cond);
}

// sleep on waiting for notification
static inline int sleep_on(struct synch_wait *wait)
{
	if (wait->dead)
		goto end;
	wait->sleep = 1;
	if (!wait->notified)
		pthread_cond_wait(&wait->cond, wait->tsk_lock);
	wait->notified = 0;
	wait->sleep = 0;
end:

	return -(wait->dead);
}

// notify others
static inline int wake_up(struct synch_wait *wait)
{
	if (wait->dead)
		return -(wait->dead);

	if (!wait->notified) {
		wait->notified = 1;
		if (wait->sleep)
			pthread_cond_signal(&wait->cond);
	}

	return -(wait->dead);
}

// allocate a wait struct 
static inline struct synch_wait *alloc_wait_struct(pthread_mutex_t *lock)
{
	struct synch_wait *wait = malloc(sizeof(*wait));
	wait_init(wait, lock);

	return wait;
}

// free the wait struct
static inline void free_wait_struct(struct synch_wait *wait)
{
	free(wait);
}

#endif
