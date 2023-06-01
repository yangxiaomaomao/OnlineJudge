#include "utils.h"

#include <stdlib.h>

double time_now()
{
	struct timeval tv;
	gettimeofday(&tv, NULL);
	double now = 0.0;
	now += tv.tv_sec;
	now += 0.000001 * tv.tv_usec;

	return now;
}


