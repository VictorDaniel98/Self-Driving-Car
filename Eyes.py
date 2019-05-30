import cv2
import numpy
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.output(40, GPIO.HIGH)

p = GPIO.PWM(3,50)
p.start(7.5)



cap = cv2.VideoCapture(0)
while True:
    _, Frame = cap.read()
    cv2.imshow("Frame", Frame)
    GPIO.output(15, GPIO.HIGH)
    GPIO.output(13, GPIO.LOW)
    
    #
    p.ChangeDutyCycle(7.5)
    time.sleep(1)
        
    p.ChangeDutyCycle(12.5)
    time.sleep(1)
    
    p.ChangeDutyCycle(7.5)
    time.sleep(1)
        
    p.ChangeDutyCycle(2.5)
    time.sleep(1)
    #
    
    key = cv2.waitKey(1)
    if key == 27:
        break
    
cap.release()
GPIO.output(40, GPIO.LOW)
GPIO.output(15, GPIO.LOW)
GPIO.output(13, GPIO.LOW)
p.stop()
GPIO.cleanup()
cv2.destroyAllWindows()