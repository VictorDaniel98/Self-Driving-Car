import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD)
gpio.setup(13, gpio.OUT)
gpio.setup(15, gpio.OUT)

p = gpio.PWM(13, 50)
q = gpio.PWM(15, 50)

p.start(0)
q.start(0)

try:
    while True:
        #foward
        for i in range(100):
        p.ChangeDutyCycle(i)
        time.sleep(0.02)
        for i in range(100):
        p.ChangeDutyCycle(100-i)
        time.sleep(0.02)
        
        p.ChangeDutyCycle(0)
        
        #Backward
        for i in range(100):
        q.ChangeDutyCycle(i)
        time.sleep(0.02)
        for i in range(100):
        q.ChangeDutyCycle(i)
        time.sleep(0.02)
        q.ChangeDutyCycle(0)
except KeyboardInterrupt:
    pass
p.stop()

    
gpio.cleanup()