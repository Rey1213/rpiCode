import RPi.GPIO as GPIO #para usar GPIO en Raspberry

import os #para controlar sistema operativo

from time import sleep


GPIO.setmode(GPIO.BOARD) #Usar pins de board, no #s GPIO

#--------------- BOTON PRESIONADO / LED AMARILLO --------------------
on = 0 #If boton presionado
yellow=29 #Pin 29 / GPIO_05
GPIO.setup(yellow, GPIO.IN) #Input Rpi pregunta conexion 

#-------------- LED VERDE ----------------------
green=31 #Pin 31 / GPIO_06
GPIO.setup(green, GPIO.OUT) #Output respuesta de dispositivo



# ---------------------- PROGRAMA MAIN ---------------------------

print("Presiona boton para prender LED Amarillo\n\n")

while(on==0): #Mientras boton no ha sido presionado

    if(GPIO.input(yellow)==True): #Si boton presionado
        on=1   #Boton fue presionado
        print("\n\nBoton presionado\n\n")
        sleep(1)

print("\n\nPrendiendo LED Verde\n\n")
sleep(2)
GPIO.output(green,True) # Prende LED verde
print("\n\nLED Verde prendido :D\n\n")

print("\n\nApagando LED Verde\n\n")
sleep(3)
for x in range(0, 3): # 0,1,2 / 3 veces
    GPIO.output(green,True) # Prende LED verde
    sleep(1) # Pausa de 1 seg
    GPIO.output(green,False) # Apaga LED verde
    sleep(1) # Pausa de 1 seg

GPIO.cleanup() #Limpia puertos GPIO
print("\n\nPrograma terminado")

