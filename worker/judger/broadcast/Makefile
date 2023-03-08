TARGET := hub

all: TARGET
SOURCES := $(wildcard *.c)
TARGET: $(SOURCES)
	gcc -Iinclude/ -Wall -g $(SOURCES) -o $(TARGET)

clean:
	@rm -f hub
