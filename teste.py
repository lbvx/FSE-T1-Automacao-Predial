import RPi.GPIO as GPIO
from pigpio_dht import DHT22
from time import sleep

GPIO.setmode(GPIO.BCM) 

lampada1 = 26
sensorFumaca = 11
sensorTemp = 18
GPIO.setup(lampada1, GPIO.OUT)
GPIO.setup(sensorFumaca, GPIO.IN)
GPIO.setup(sensorTemp, GPIO.IN)

while True:
    sleep(1)
    GPIO.output(lampada1, GPIO.HIGH if GPIO.input(sensorFumaca) else GPIO.LOW)
    temp = DHT22(sensorTemp).read()
    print(temp)
