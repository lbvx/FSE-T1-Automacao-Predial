import threading
from Conexao import ConexaoCentral
import json
from datetime import datetime

class Interface(threading.Thread):
    def __init__(self, cc:ConexaoCentral) -> None:
        super().__init__()
        self.cc = cc

    def menu(self):
        print('''
Comandos:
menu - exibe esse menu
salas - exibe salas conectadas
pessoas - exibe quantidade de pessoas no prédio
<nome da sala> - exibe estados de uma sala
ligar <sala> <outputs> - liga saídas de uma sala
desligar <sala> <outputs> - desliga saídas de uma sala
             ''')

    def enviaSinal(self, cmd:str, e:bool) -> bool:
        cmd = cmd.split()
        sala = cmd[0]
        out = cmd[1:]

        if out[0] == 'tudo':
            msg = {'tudo': e}
        else:
            msg = {k: e for k in out if k != 'tudo' and k != 'lampadas' and k != 'AL_BZ'}
            if 'lampadas' in out:
                msg['L_01'] = e
                msg['L_02'] = e

        msg = json.dumps(msg).encode('utf-8')

        if sala == 'tudo':
            for c in self.cc.conexoes:
                c['socket'].send(msg)
            return True

        for c in self.cc.conexoes:
            if c['nome'] == sala:
                c['socket'].send(msg)
                return True

        return False

    def exibeSalas(self):
        print('Salas conectadas: ', end='')
        print(*[s['nome'] for s in self.cc.conexoes], sep=', ')

    def exibePessoas(self):
        total = sum([e['pessoas'] for e in self.cc.estados.values()])
        print('Total: %d' % total, end=', ')
        print(*['%s: %d' % (c, self.cc.estados[c]['pessoas']) for c in self.cc.estados], sep=', ')

    def exibeInfo(self, nomesala):
        est = self.cc.estados[nomesala]
        # print(nomesala)
        print('\tPessoas:', est['pessoas'])
        print('\tTemperatura: %.1f°C' % est['temp'])
        print('\tUmidade: %.1f%%' % est['umid'])
        print('\tSistema de Alarme:', ('Ligado' if est['alarme'] else 'Desligado'))
        print('\tEntradas:')
        print(*[f'\t  {n}: {int(e)}' for n, e in est['input'].items()], sep='\n')
        print('\tSaídas:')
        print(*[f'\t  {n}: {int(e)}' for n, e in est['output'].items()], sep='\n')

    def logCmd(self, cmd, sala):
        horario = datetime.now()
        while True:
            try:
                with open('log.csv', 'a') as f:
                    f.write('%d-%d-%d %d:%d:%d,%s,Comando enviado: %s\n' %
                            (horario.year, horario.month, horario.day,
                                horario.hour, horario.minute, horario.second,
                                sala, cmd))
                return
            except FileNotFoundError:
                with open('log.csv', 'w'): pass

    def run(self):
        self.menu()
        while True:
            inp = input()
            cmd = inp.split(' ', maxsplit=1)
            if cmd[0] == 'menu' or cmd[0] == 'help':
                self.menu()
            elif cmd[0] == 'salas':
                self.exibeSalas()
            elif cmd[0] == 'ligar':
                self.enviaSinal(cmd[1], True)
                self.logCmd(inp, cmd[1].split()[0])
            elif cmd[0] == 'desligar':
                self.enviaSinal(cmd[1], False)
                self.logCmd(inp, cmd[1].split()[0])
            elif cmd[0] == 'pessoas':
                self.exibePessoas()
            elif cmd[0] in self.cc.estados:
                self.exibeInfo(cmd[0])
