import json
import RPi.GPIO as GPIO
import threading
from time import sleep
import Adafruit_DHT as DHT

class Sala:
    input : dict
    output : dict
    estado : dict
    pessoasQtd : int
    temp : float
    umid : float

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

        self.estado = {k: False for k in self.output}
        self.dht22 = cfg['sensor_temperatura'][0]['gpio']
        self.pessoasQtd = 0

        GPIO.setmode(GPIO.BCM) 
        for c in self.output.values():
            GPIO.setup(c, GPIO.OUT)

        for c in self.input.values():
            GPIO.setup(c, GPIO.IN)

        GPIO.add_event_detect(self.input['SC_IN'], GPIO.RISING)
        GPIO.add_event_detect(self.input['SC_OUT'], GPIO.RISING)

    def reset(self) -> None:
        for o in self.output:
            self.desliga(o)

    def liga(self, out:str) -> None:
        GPIO.output(self.output[out], GPIO.HIGH)
        self.estado[out] = True

    def desliga(self, out:str) -> None:
        GPIO.output(self.output[out], GPIO.LOW)
        self.estado[out] = False

    def detectaEntrada(self) -> None:
        if GPIO.event_detected(self.input['SC_IN']):
            self.pessoasQtd += 1
        if GPIO.event_detected(self.input['SC_OUT']) and self.pessoasQtd > 0:
            self.pessoasQtd -= 1

    def detectaTemp(self) -> None:
        d = DHT.read(DHT.DHT22, self.dht22)
        self.umid = d[0]
        self.temp = d[1]

class SalaThread(threading.Thread):
    def __init__(self, sala:Sala) -> None:
        super().__init__()
        self.sala = sala

    # def ligaLuzes(self):
    #     self.sala.liga('L_01')
    #     self.sala.liga('L_02')

    def run(self):
        while True:
            self.sala.detectaEntrada()
            self.sala.detectaTemp()
            sleep(0.01)
