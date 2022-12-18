import threading
import json
from time import sleep
import socket
from datetime import datetime

class AcceptThread(threading.Thread):
    def __init__(self, sock:socket.socket, listaConexoes:list) -> None:
        super().__init__()
        self.socket = sock
        self.conexoes = listaConexoes

    def run(self):
        while True:
            nc = self.socket.accept()
            novodict = json.loads(nc[0].recv(1024))
            novo = {'nome': novodict['nome'], 'socket': nc[0], 'end': nc[1]}
            self.conexoes.append(novo)
            print('Nova conexão:', novodict['nome'])

class ConexaoCentral(threading.Thread):
    end : tuple
    conexoes : list
    estados : dict

    def __init__(self, end) -> None:
        super().__init__()
        self.end = end
        self.conexoes = []
        self.estados = {}

    def criaServer(self) -> None:
        self.socket = socket.create_server(self.end)

    def recebeEstados(self) -> None:
        for c in self.conexoes.copy():
            msg = c['socket'].recv(2048)
            self.estados[c['nome']] = json.loads(msg)['estados']

    def logAlarme(self) -> None:
        listaAlarme = [i for i, e in self.estados.items() if e['output']['AL_BZ']]
        horario = datetime.now()
        while True:
            try:
                with open('log.csv', 'a') as f:
                    for a in listaAlarme:
                        f.write('%d-%d-%d %d:%d:%d,%s,Alarme (Buzzer) Ligado\n' %
                            (horario.year, horario.month, horario.day,
                             horario.hour, horario.minute, horario.second,
                             a))
                return
            except FileNotFoundError:
                with open('log.csv', 'w'): pass


    def run(self):
        self.criaServer()
        self.at = AcceptThread(self.socket, self.conexoes)
        self.at.start()

        while True:
            self.recebeEstados()
            self.logAlarme()
            # print(*[i['nome'] for i in self.conexoes], sep=' ')
            # print('\n', self.estados, sep='')
            sleep(2.0)
