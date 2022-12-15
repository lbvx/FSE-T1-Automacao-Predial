import sys
from time import sleep
import socket
import json

def main():
    end = sys.argv[1], int(sys.argv[2])
    a = socket.create_server(end)
    b = a.accept()[0]
    c = b.recv(1024)
    print(json.loads(c))

if __name__ == '__main__':
    main()
