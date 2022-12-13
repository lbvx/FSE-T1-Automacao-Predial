import threading
import json
from time import sleep
import socket
from Sala import SalaThread

class ConexaoThread(threading.Thread):
    def __init__(self, st:SalaThread) -> None:
        super().__init__()
        self.st = st

    def criaSocket(self):
        self.sock = socket.create_server(self.st.sala.end)

    def run(self):
        self.criaSocket()
        self.sockCentral = self.sock.accept()
        print('asd:')
        print(self.sockCentral)
        sleep(5)
        self.st.encerra()
        self.st.join()
