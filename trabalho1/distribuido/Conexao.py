import threading
import json
from time import sleep
import socket
from Sala import Sala

class ConexaoDistribuido(threading.Thread):
    sala : Sala
    socketCentral : socket.socket
    _rodando : bool

    def __init__(self, sala:Sala) -> None:
        super().__init__()
        self.sala = sala
        self.socketCentral = None

    def conectaCentral(self) -> None:
        self.socketCentral = socket.create_connection(self.sala.endCentral, timeout=5.0)
        msg = {"nome": self.sala.nome,\
               "ip_servidor_distribuido": self.sala.end[0],\
               "porta_servidor_distribuido": self.sala.end[1]}
        self.socketCentral.send(json.dumps(msg).encode('utf-8'))

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
