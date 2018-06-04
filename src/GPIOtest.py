import RPi.GPIO as GPIO #para usar GPIO en Raspberry

import os #para controlar sistema operativo

from time import sleep


GPIO.setmode(GPIO.BOARD) #Usar pins de board, no #s GPIO


#--------------- BOTON PRESIONADO / LED AMARILLO --------------------
on = 0 #If boton presionado
yellow=29 #Pin 29 / GPIO_05
GPIO.setup(yellow, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Input Rpi pregunta conexion 


#-------------- LED VERDE ----------------------
green=31 #Pin 31 / GPIO_06
GPIO.setup(green, GPIO.OUT) #Output respuesta de dispositivo
GPIO.output(green, False) #Inicalmente apagado


# ---------------------- PROGRAMA MAIN ---------------------------

try: #Por si acaso hay exception

    print("Presiona boton para prender LED Amarillo\n\n")

    timeo = GPIO.wait_for_edge(yellow, GPIO.RISING, timeout=5000) #Para interrupcion de boton

    if(timeo is None): #Si el tiempo de espera (timeout) se acaba
        print("Timeout")
    else: #Boton apretado antes que termine tiempo de espera
        on=1   #Boton fue presionado
        print("\n\nBoton presionado\n\n")
        sleep(1)

        print("\n\nPrendiendo LED Verde\n\n")
        sleep(2)
        
        GPIO.output(green,True) # Prende LED verde
        print("\n\nLED Verde prendido :D\n\n")

        print("\n\nApagando LED Verde\n\n")
        sleep(3)
        if(on==1):
            for x in range(0, 3): # 0,1,2 / 3 veces
                GPIO.output(green,False) # Apaga LED verde
                sleep(1) # Pausa de 1 seg
                GPIO.output(green,True) # Prende LED verde
                sleep(1) # Pausa de 1 seg
                GPIO.output(green,False) # Apaga LED verde
                sleep(1) # Pausa de 1 seg

    #GPIO.cleanup() #Limpia puertos GPIO
    print("\n\nPrograma terminado")
except: #Excepcion
    print("\n\nException")
finally: #Aun con exception se limpian los puertos GPIO
    GPIO.cleanup()
