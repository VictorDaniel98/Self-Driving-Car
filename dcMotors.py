import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD)
gpio.setup(13, gpio.OUT)
gpio.setup(15, gpio.OUT)

for i in range(5):
    gpio.output(13, gpio.LOW)
    gpio.output(15, gpio.HIGH)
    time.sleep(1)
    
gpio.cleanup()