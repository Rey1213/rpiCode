import RPi.GPIO as GPIO
import os
import time

GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False);

GPIO.setup(10, GPIO.IN)#Button to GPIO10

print("--------------")
print(" Button + GPIO ")
print("--------------")

print GPIO.input(10)

try:
    while True:
        if( GPIO.input(10) == False ):
            print('Button Pressed...')
            os.system('date')
            print GPIO.input(10)
            time.sleep(5)
        else:
            os.system('clear')
            print("Waiting for you to press button")          
except:
    GPIO.cleanup()
time.sleep(1)