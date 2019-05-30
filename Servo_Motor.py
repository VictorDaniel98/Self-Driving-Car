import RPi.GPIO as gp
import time

gp.setmode(gp.BOARD)

gp.setup(3, gp.OUT)

p = gp.PWM(3,50)
p.start(7.5)

try:
    while True:
        p.ChangeDutyCycle(7.5)
        time.sleep(1)
        
        p.ChangeDutyCycle(12.5)
        time.sleep(1)
        
        p.ChangeDutyCycle(2.5)
        time.sleep(1)
except KeyboardInterrupt:
    p.stop()
    gp.cleanup()
