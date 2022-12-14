import threading
import json
from time import sleep
import socket
from Sala import SalaThread

class ConexaoThread(threading.Thread):
    def __init__(self, st:SalaThread) -> None:
        super().__init__()
        self.st = st
        self.sockCentral = None

    def conectaCentral(self):
        self.sockCentral = socket.create_connection(self.st.sala.endCentral, timeout=5.0)

    def run(self):
        self.conectaCentral()
        print('asd:')
        print(self.sockCentral)
        sleep(2)
        self.sockCentral.send(b'{"joao":false, "marcos":14.921}')
        self.st.encerra()
        self.st.join()

    def envia(self, out:str, est:bool) -> None:
        if est:
            self.st.sala.liga(out)
        else:
            self.st.sala.desliga(out)
