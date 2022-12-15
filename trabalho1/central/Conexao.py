import threading
import json
from time import sleep
import socket

class AcceptThread(threading.Thread):
    def __init__(self, sock:socket.socket, listaConexoes:list):
        super().__init__()
        self.socket = sock
        self.conexoes = listaConexoes

    def run(self):
        while True:
            nc = self.socket.accept()
            novodict = json.loads(nc[0].recv(1024))
            novo = {'nome': novodict['nome'], 'socket': nc[0], 'end': nc[1]}
            self.conexoes.append(novo)

class ConexaoCentral(threading.Thread):
    end : tuple
    conexoes : list
    _rodando : bool

    def __init__(self, end) -> None:
        super().__init__()
        self.end = end
        self.conexoes = []
        self._rodando = None

    def criaServer(self):
        self.socket = socket.create_server(self.end)
        self.at = AcceptThread(self.socket, self.conexoes)
        self.at.start()
        self._rodando = True

        while self._rodando:
            for c in self.conexoes.copy():
                print(c['nome'], end=' ')
            print()
            sleep(1.0)

    def run(self):
        self.criaServer()
