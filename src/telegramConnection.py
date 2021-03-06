import RPi.GPIO as GPIO #para usar GPIO en Raspberry
import telepot #para usar telegram en Raspberry
from telepot.loop import MessageLoop #para crear ciclo de comandos del Telegram bot

#import sys
import os #para controlar sistema operativo
#import time time.sleep()
from time import sleep #Para poder ponerle pausa al programa


GPIO.setmode(GPIO.BOARD) #Usar pins de board, no #s GPIO

#--------------- BOTON PRESIONADO --------------------
#Input Rpi pregunta conexion
on = 0 #If boton presionado
yellow=29 #Pin 29 / GPIO_05
GPIO.setup(yellow, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Pin de entrada con resistencia pull-up 

#-------------- DISPOSITIVO RESPONDIO ----------------------
reply = 0 #Si dispositivo respondio
green=31 #Pin 31 / GPIO_06
GPIO.setup(green, GPIO.OUT) #Output respuesta de dispositivo

#------------ PARAR PROGRAMA ----------------------------------
stop = 0 #Para terminar el programa

message = "no_reply" #no hubo respuesta del dispositivo


#------------- ACCIONES DE TELEGRAM BOT --------------------
def action(msg):
    global message, reply, stop

    #La "direccion" donde el Telegram bot responde
    chat_id = msg['chat']['id'] #Para que bot pueda responder
    command = msg['text'] #comando recibido
    print('\n\nComando recibido: %s' %command)

    if on==0: #Boton no ha sido presionado en Raspberry
        message = "\n\nRaspberry no ha solicitado conexion. Aprete el boton en Raspberry."

    elif ('si' in command and reply==0 and stop==0): #Dispositivo acepto conexion
        reply = 1
        message = "Conectado al Raspberry Pi :D"
        print("\n\nDispositivo conectado :D")

        GPIO.output(green,True) # Prende LED verde
             
    elif ('no' in command and reply==0 and stop==0): #Dispositivo nego conexion
        stop = 1
        message = "Usted nego la conexion"
        print("\n\nDispositivo nego conexion :(")

        for x in range(0, 10): # 0,1,2..,9 / 10 veces
            if(GPIO.output(green,True)):
                GPIO.output(green,False) # Apaga LED verde
                sleep(.3) # Pausa
                GPIO.output(green,True) # Prende LED verde
                sleep(.3) # Pausa
                GPIO.output(green,False) # Apaga LED verde
                sleep(.3) # Pausa
            else:
                GPIO.output(green,True) # Prende LED verde
                sleep(.3) # Pausa
                GPIO.output(green,False) # Apaga LED verde
                sleep(.3) # Pausa
            
    elif 'stop' in command: #Terminar programa
        stop = 1
        message = "Usted termino el programa"
        print("\n\nDispositivo terminando programa...")

        for x in range(0, 5): # 0,1,2,3,4 / 5 veces
            if(GPIO.output(green,True)):
                GPIO.output(green,False) # Apaga LED verde
                sleep(1) #Pausa programa
                GPIO.output(green,True) # Prende LED verde
                sleep(1) #Pausa programa
                GPIO.output(green,False) # Apaga LED verde
                sleep(1) #Pausa programa
            else:
                GPIO.output(green,True) # Prende LED verde
                sleep(1) #Pausa programa
                GPIO.output(green,False) # Apaga LED verde
                sleep(1) #Pausa programa

    elif (reply==0 and stop==0): #Comando invalido
        message = ("\nIntroduzca (en minuscula): "
        "\n\t\"si\" - para permitir conexion "
        "\n\t\"no\" - para negar conexion "
        "\n\n")
    else: #Comando invalido despues de conexion
        message = ("\nIntroduzca (en minuscula): "
        "\n\t\"stop\" - para apagar programa "
        "\n\n")
    
    telegram_bot.sendMessage(chat_id,message) #Bot manda mensaje
        


# ---------------------- PROGRAMA MAIN ---------------------------
try: #Por si acaso hay exceptio
    print("Presiona boton para solicitar conexion\n\n")

    timeo = GPIO.wait_for_edge(yellow, GPIO.RISING, timeout=10000) #Para interrupcion de boton

    if(timeo is None): #Si el tiempo de espera (timeout:10 segundos) se acaba
        print("\n\nTimeout\n\n")

    else: #Boton apretado antes que termine tiempo de espera

        os.system('clear') #Limpiar pantalla
        on=1   #Boton fue presionado
        print("Boton presionado\n\n")
        sleep(1) #Pausa programa

        os.system('clear') #Limpiar pantalla

        #telegram_id = input("Introduzca ID de Telegram del Dispositivo: ") # Introducir id de usuario Telegram
        telegram_id =  # id de usuario Telegram (Pon el tuyo)

        #telegram_bot = sys.argv[1] #Para adquerir bot token del terminal como argumento
        telegram_bot = telepot.Bot('Tu Telegram Bot API key') #HTTP API para Telegram Bot

        if(telegram_bot.getMe() is None): #Si error con Telegram Bot
            print("\n\n * *Error con bot* *\n\n")

        else: #Telegram Bot exitoso
            print(telegram_bot.getMe()) #Enseñar info de bot
            sleep(1)

            #----------- Si no hubo error con Telegram bot -------------------------------
        
            #Mensaje de inicio
            message = ("Raspberry solicita conexion. Permitir conexion? "
            "\n\n\"si\" para permitir conexion "
            "\n\n\"no\" para negar conexion ")

            #Bot manda mensaje de inicio
            telegram_bot.sendMessage(telegram_id,message)

            os.system('clear')
            message = "no_reply" #Para revisar si dispositivo responde
            
            print("Esperando respuesta de dispositivo")
            MessageLoop(telegram_bot, action).run_as_thread() #Esperar mensaje de dispositivo en background
            
            #Pausa hasta que se acaba Tiempo de Espera
            sleep(5) #Pausa 5 seg
            i=1
            while(reply==0 and stop==0 and i<=10): #Total pausa de 55 seg
                sleep(i) # 1+2+3+4+5+6+7+8+9+10 = 55 seg
                ++i

            #Timeout
            if(message == "no_reply"): #Si dispositivo no respondio despues de 10 segundos
                print("\n\n * *No hubo respuesta del dispositivo* *"
                "\n\nTerminando programa\n\n")
            else:
                while (stop==0): #Minetras no se le ha dicho al programa que termine
                    #haz algo
                    sleep(10)

    sleep(7)
    print("\n\nPrograma terminado")

except: #Hubo excepcion
    print("\n\n * *Hubo excepcion* *\n\n")

finally: #Limpia puertos GPIO aun si hubo excepcion
    GPIO.cleanup() #Limpia puertos GPIO
    

