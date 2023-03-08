TARGET = http-server
all: $(TARGET)

http-server: *.c
	gcc -Wall -g *.c -o $(TARGET) -lssl -lcrypto -lpthread

clean:
	@rm $(TARGET)
