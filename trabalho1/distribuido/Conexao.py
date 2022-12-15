import threading
import json
from time import sleep
import socket
from Sala import Sala

class ConexaoThread(threading.Thread):
    sala : Sala
    sockCentral : socket.socket
    _rodando : bool

    def __init__(self, sala:Sala) -> None:
        super().__init__()
        self.sala = sala
        self.sockCentral = None

    def conectaCentral(self):
        self.sockCentral = socket.create_connection(self.sala.endCentral, timeout=5.0)
        msg = {"nome": self.sala.nome,\
               "ip_servidor_distribuido": self.sala.end[0],\
               "porta_servidor_distribuido": self.sala.end[1]}
        self.sockCentral.send(json.dumps(msg).encode('utf-8'))

    def run(self):
        self._rodando = True
        self.conectaCentral()
        while self._rodando:
            pass

    def alteraSinal(self, out:str, est:bool) -> None:
        if est:
            self.sala.liga(out)
        else:
            self.sala.desliga(out)
