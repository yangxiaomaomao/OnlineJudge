TARGET = ip_lookup

all: $(TARGET)

cp /home/yangxiaomao/OnlineJudge/worker/judger/ip_lookup/project/main.c .

SRCS = tree.c util.c main.c

$(TARGET): $(SRCS)
	gcc -Wall -g $(SRCS) -o $(TARGET) -I./include

clean:
	@rm $(TARGET)
