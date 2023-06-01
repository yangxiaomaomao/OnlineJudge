TARGET = ip_lookup

all: $(TARGET)

MAIN_SRC = /home/yangxiaomao/worker/judger/ip_lookup/project/main.c

FUNC_SRCS = tree.c util.c

$(TARGET): $(SRCS)
	gcc -Wall -g $(MAIN_SRC) $(FUNC_SRCS) -o $(TARGET) -I./include

clean:
	@rm $(TARGET)
