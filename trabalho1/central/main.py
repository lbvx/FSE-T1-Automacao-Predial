import sys
from time import sleep
import socket
import json
from Conexao import ConexaoCentral

def main():
    end = sys.argv[1], int(sys.argv[2])
    ct = ConexaoCentral(end)
    ct.start()
    ct.join()

if __name__ == '__main__':
    main()
