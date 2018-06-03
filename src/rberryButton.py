import RPi.GPIO as GPIO
import os
#import time
from time import sleep

GPIO.setmode(GPIO.BOARD) #Usar pins de board, no #s GPIO
on = 0 #If boton presionado
yellow=29 #Pin 29 / GPIO_05
GPIO.setup(yellow, GPIO.IN) #Input Rpi pregunta conexion 

out = 0 #If dispositivo respondio
green=31 #Pin 31 / GPIO_06
GPIO.setup(green, GPIO.OUT) #Output respuesta de dispositivo

print("Presiona boton para solicitar conexion")

while(on==0):

    if(GPIO.input(yellow)==True): #If button pressed
        os.system('clear') #Limpiar pantalla
        on=1   #Boton fue presionado
        print("Boton presionado\n\n")
        sleep(2)

        os.system('clear')
        device = input("Introduzca ID del dispositivo al que se quiere conectar: ")

os.system('clear')
print("Esperando respuesta de dispositivo")

#Ask if device wants to connect
while (out==0 and on==1):

    if(GPIO.output(green)==True):
        os.system('clear') #Limpiar pantalla
        out=1 #Hubo respuesta de dispositivo
        print("Dispositivo respondio\n\n")

        #Dispositivo nego conexion
        for x in range(0, 3): # 0,1,2 / 3 veces
            GPIO.output(green,True) # Prende LED verde
            sleep(1) # Pausa de 1 seg
            GPIO.output(green,False) # Apaga LED verde
            sleep(1) # Pausa de 1 seg

        #Dispositivo acepto conexion
        GPIO.output(green,True) # Prende LED verde

while (out==1 and on==1):
    #haz algo

    #termina programa
    break


GPIO.cleanup() #Limpia puertos GPIO
print("\n\nPrograma terminado")

