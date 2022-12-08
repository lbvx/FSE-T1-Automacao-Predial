import threading
import json
import RPi.GPIO as GPIO
from time import sleep
# import adafruit_dht

with open('config.json', 'r') as f:
    CFG = json.load(f)

def setupGPIO():
    GPIO.setmode(GPIO.BCM) 
    for c in CFG['OUT'].values():
        GPIO.setup(c, GPIO.OUT)

    for c in CFG['IN'].values():
        GPIO.setup(c, GPIO.IN)

class Lampada(threading.Thread):
    def ativa(self):
        if not self.is_alive():
            self.run() # BIG NO NO 

    def run(self):
        GPIO.output((CFG['OUT']['L_01'], CFG['OUT']['L_02']), GPIO.HIGH)
        sleep(15)
        GPIO.output((CFG['OUT']['L_01'], CFG['OUT']['L_02']), GPIO.LOW)

def main():
    setupGPIO()
    l = Lampada()
    l.
    while True:
        if (GPIO.input(CFG['IN']['SPres'])):
            l.ativa()

if __name__ == '__main__':
    main()
