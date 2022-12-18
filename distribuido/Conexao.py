import threading
import json
from time import sleep
import socket
from Sala import Sala
from select import select

class ConexaoDistribuido(threading.Thread):
    sala : Sala
    socketCentral : socket.socket
    _rodando : bool

    def __init__(self, sala:Sala) -> None:
        super().__init__()
        self.sala = sala
        self.socketCentral = None

    def conectaCentral(self) -> None:
        while True:
            try:
                self.socketCentral = socket.create_connection(self.sala.endCentral, timeout=5.0)
                msg = {"nome": self.sala.nome,                          \
                    "ip_servidor_distribuido": self.sala.end[0],     \
                    "porta_servidor_distribuido": self.sala.end[1]}
                self.socketCentral.send(json.dumps(msg).encode('utf-8'))
                return
            except ConnectionRefusedError:
                print('falhou em conectar, tentando de novo em 1 seg')
                sleep(1)

    def enviaEstados(self) -> None:
        msg = {}
        msg['nome'] = self.sala.nome
        est = {}
        est['output'] = {}
        est['input'] = {}
        for n, e in self.sala.estado.items():
            est['output'][n] = e

        for n in self.sala.input:
            est['input'][n] = self.sala.ler(n)

        est['umid'] = self.sala.umid
        est['temp'] = self.sala.temp
        est['pessoas'] = self.sala.pessoasQtd
        est['alarme'] = self.sala.sistemaAlarme
        msg['estados'] = est

        self.socketCentral.send(json.dumps(msg).encode('utf-8'))
        print('enviado')

    def executaComando(self, cmd:dict) -> None:
        if 'alarme' in cmd:
            self.sala.sistemaAlarme = cmd['alarme']

        if 'tudo' in cmd:
            e = cmd['tudo']
            for out in self.sala.output:
                if out != 'AL_BZ':
                    if e:
                        self.sala.liga(out)
                    else:
                        self.sala.desliga(out)
            return
        
        for o in cmd:
            if cmd[o]:
                self.sala.liga(o)
            else:
                self.sala.desliga(o)

    def recebeComando(self) -> None:
        while True:
            select([self.socketCentral,], [], [self.socketCentral,])
            cmd = json.loads(self.socketCentral.recv(2048))
            print('comando recebido')
            # print(cmd)
            self.executaComando(cmd)
            
    def run(self):
        self._rodando = True
        self.conectaCentral()
        rt = threading.Thread(target=self.recebeComando)
        rt.start()
        while self._rodando:
            self.enviaEstados()
            sleep(2.0)

    def alteraSinal(self, out:str, est:bool) -> None:
        if est:
            self.sala.liga(out)
        else:
            self.sala.desliga(out)

    def encerra(self) -> None:
        self._rodando = False
