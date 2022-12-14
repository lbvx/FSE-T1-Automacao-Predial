import sys
from time import sleep
import socket
import json

def main():
    a = socket.create_server(('127.0.0.1', 10000))
    b = a.accept()[0]
    c = b.recv(1024)
    print(json.loads(c))

if __name__ == '__main__':
    main()
