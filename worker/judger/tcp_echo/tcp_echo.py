import sys
import string
import socket
from time import sleep

data = string.digits + string.ascii_lowercase + string.ascii_uppercase

def server(port):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    s.bind(('0.0.0.0', int(port)))
    s.listen(3)
    
    cs, addr = s.accept()
    print(addr)
    
    while True:
        data = cs.recv(1000)
        
        if data:
            data = "server echoes: " + data.decode()
            cs.send(data.encode())
        else:
            break
    
    s.close()


def client(ip, port):
    s = socket.socket()
    s.connect((ip, int(port)))
    
    for i in range(3):
        new_data = data[i:] + data[:i+1]
        s.send(new_data.encode())
        print(s.recv(1000).decode())
        sleep(1)
    
    s.close()

if __name__ == '__main__':
    if sys.argv[1] == 'server':
        server(sys.argv[2])
    elif sys.argv[1] == 'client':
        client(sys.argv[2], sys.argv[3])

