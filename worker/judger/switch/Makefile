TARGET = switch

all : $(TARGET)

CC = gcc
LD = gcc

CFLAGS = -g -std=gnu99 -Wall -Iinclude
LDFLAGS = 

LIBS = -lpthread

SRCS = $(wildcard *.c)

OBJS = $(patsubst %.c,%.o,$(SRCS))

$(OBJS) : %.o : %.c include/*.h
	$(CC) -c $(CFLAGS) $< -o $@

$(TARGET): $(OBJS)
	$(LD) $(LDFLAGS) $(OBJS) -o $(TARGET) $(LIBS) 

clean:
	rm -f *.o $(TARGET)

tags: *.c include/*.h
	ctags *.c include/*.h
