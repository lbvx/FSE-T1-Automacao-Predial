import json
import RPi.GPIO as GPIO
import threading
from time import sleep, time
import board
import adafruit_dht as DHT

class Sala:
    input : dict
    output : dict
    estado : dict
    pessoasQtd : int
    temp : float
    umid : float
    sistemaAlarme : bool
    end : tuple
    endCentral : tuple

    def __init__(self, config:str) -> None:
        with open(config) as f:
            cfg = json.load(f)

        out = cfg['outputs']
        self.output = {}
        for o in out:
            if o['tag'] == 'Lâmpada 01':
                self.output['L_01'] = o['gpio']
            elif o['tag'] == 'Lâmpada 02':
                self.output['L_02'] = o['gpio']
            elif o['tag'] == 'Projetor Multimidia':
                self.output['PR'] = o['gpio']
            elif o['tag'] == 'Ar-Condicionado (1º Andar)':
                self.output['AC'] = o['gpio']
            elif o['tag'] == 'Sirene do Alarme':
                self.output['AL_BZ'] = o['gpio']

        inp = cfg['inputs']
        self.input = {}
        for i in inp:
            if i['tag'] == 'Sensor de Presença':
                self.input['SPres'] = i['gpio']
            elif i['tag'] == 'Sensor de Fumaça':
                self.input['SFum'] = i['gpio']
            elif i['tag'] == 'Sensor de Janela':
                self.input['SJan'] = i['gpio']
            elif i['tag'] == 'Sensor de Porta':
                self.input['SPor'] = i['gpio']
            elif i['tag'] == 'Sensor de Contagem de Pessoas Entrada':
                self.input['SC_IN'] = i['gpio']
            elif i['tag'] == 'Sensor de Contagem de Pessoas Saída':
                self.input['SC_OUT'] = i['gpio']

        self.nome = cfg['nome']
        self.estado = {k: False for k in self.output}
        self.end = (cfg['ip_servidor_distribuido'], cfg['porta_servidor_distribuido'])
        self.endCentral = (cfg['ip_servidor_central'], cfg['porta_servidor_central'])
        self.pessoasQtd = 0
        self.sistemaAlarme = False
        self.umid = None
        self.temp = None

        dht22porta = cfg['sensor_temperatura'][0]['gpio']
        if dht22porta == 18:
            self.dhtDevice = DHT.DHT22(board.D18)
        elif dht22porta == 4:
            self.dhtDevice = DHT.DHT22(board.D4)

        GPIO.setmode(GPIO.BCM) 
        for c in self.output.values():
            GPIO.setup(c, GPIO.OUT)

        for c in self.input.values():
            GPIO.setup(c, GPIO.IN)

        GPIO.add_event_detect(self.input['SC_IN'], GPIO.RISING)
        GPIO.add_event_detect(self.input['SC_OUT'], GPIO.RISING)

        self.reset()

    def reset(self) -> None:
        for o in self.output:
            self.desliga(o)

    def liga(self, out:str) -> None:
        if not self.estado[out]:
            GPIO.output(self.output[out], GPIO.HIGH)
            self.estado[out] = True

    def desliga(self, out:str) -> None:
        if self.estado[out]:
            GPIO.output(self.output[out], GPIO.LOW)
            self.estado[out] = False

    def detectaEntrada(self) -> None:
        if GPIO.event_detected(self.input['SC_IN']):
            self.pessoasQtd += 1
        if GPIO.event_detected(self.input['SC_OUT']) and self.pessoasQtd > 0:
            self.pessoasQtd -= 1

    def detectaTemp(self) -> None:
        try:
            self.umid = self.dhtDevice.humidity
            self.temp = self.dhtDevice.temperature
        except RuntimeError:
            self.umid = None
            self.temp = None

class SalaThread(threading.Thread):
    _tempoLampada : float
    _spresRecente : bool
    _rodando : bool

    def __init__(self, sala:Sala) -> None:
        super().__init__()
        self.sala = sala
        self._tempoLampada = None
        self._spresRecente = False
        self._rodando = True

    def run(self):
        while self._rodando:
            self.sala.detectaEntrada()
            self.sala.detectaTemp()

            # sistema de alarme LIGADO
            if self.sala.sistemaAlarme:
                if GPIO.input(self.sala.input['SPres']) or\
                   GPIO.input(self.sala.input['SPor']) or\
                   GPIO.input(self.sala.input['SJan']) or\
                   GPIO.input(self.sala.input['SFum']):
                   self.sala.liga('AL_BZ')

                else:
                    self.sala.desliga('AL_BZ')

            # sistema de alarme DESLIGADO
            else:
                # sensor de presenca
                if GPIO.input(self.sala.input['SPres']):
                    self.ativaLampadas()

                # sensor de fumaca
                if GPIO.input(self.sala.input['SFum']):
                    self.sala.liga('AL_BZ')
                else:
                    self.sala.desliga('AL_BZ')
            
            if self._spresRecente:
                self.checaLampadas()
            sleep(0.1)

    def ativaLampadas(self) -> None:
        self.sala.liga('L_01')
        self.sala.liga('L_02')
        self._tempoLampada = time()
        self._spresRecente = True
    
    def checaLampadas(self) -> None:
        if time() - self._tempoLampada > 15.0:
            self.sala.desliga('L_01')
            self.sala.desliga('L_02')
            self._tempoLampada = None
            self._spresRecente = False

    def encerra(self) -> None:
        self._rodando = False
