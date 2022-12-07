import RPi.GPIO as GPIO
from time import sleep

# Define o padrao de numeracao das portas como BCM
# A outra opcap e GPIO.BOARD para usar o numero dos pinos fisicos da placa
GPIO.setmode(GPIO.BCM) 

# Configuracao dos pinos do botao e dos LEDs
botao = 3 # (GPIO 3) - Pino 5
leds = [13, 19, 26] # (GPIO 13, 19, 26) - Pinos 33, 35, 37

# Configuracao dos Pinos como Entradas / Saidas
GPIO.setup(botao, GPIO.IN)
GPIO.setup(leds, GPIO.OUT)

# Funcao para tratar o botao
def trataBotao():
    while not GPIO.input(botao):
        GPIO.output(leds, GPIO.HIGH)
        print("Aguarda botao ser solto")
        sleep(0.1)
    estadoInicialLEDS()


def estadoInicialLEDS():
    global counter
    GPIO.output(leds, GPIO.LOW)
    counter = 0
    print("Contador iniciado")
    
    
# Configura deteccao de acao do Botao
GPIO.add_event_detect(botao, GPIO.FALLING) # GPIO.RISING

# conta de 0 a 7
while True:
    estadoInicialLEDS()
    while counter < 8:
        if GPIO.event_detected(botao):
            trataBotao()
        GPIO.output(leds, (
            GPIO.HIGH if counter & 0b0100 else GPIO.LOW,
            GPIO.HIGH if counter & 0b0010 else GPIO.LOW,
            GPIO.HIGH if counter & 0b0001 else GPIO.LOW,
            )
        )
        counter += 1
        sleep(1)
