import RPi.GPIO as GPIO #para usar GPIO en Raspberry
import telepot #para usar telegram en Raspberry
from telepot.loop import MessageLoop #para crear ciclo de comandos del Telegram bot

#import sys
import os #para controlar sistema operativo
#import time time.sleep()
from time import sleep


GPIO.setmode(GPIO.BOARD) #Usar pins de board, no #s GPIO

#--------------- BOTON PRESIONADO --------------------
on = 0 #If boton presionado
yellow=29 #Pin 29 / GPIO_05
GPIO.setup(yellow, GPIO.IN) #Input Rpi pregunta conexion 

#-------------- DISPOSITIVO RESPONDIO ----------------------
reply = 0 #Si dispositivo respondio
green=31 #Pin 31 / GPIO_06
GPIO.setup(green, GPIO.OUT) #Output respuesta de dispositivo

stop = 0 #Para terminar el programa

message = "no_reply" #no hubo respuesta del dispositivo


#------------- ACCIONES DE TELEGRAM BOT --------------------
def action(msg):
    global message, stop

    #La "direccion" donde el Telegram bot responde
    chat_id = msg['chat']['id'] #Para que bot pueda responder
    command = msg['text'] #comando recibido
    print('\n\nComando recibido: %s' %command)

    if on==0: #Boton no ha sido presionado en Raspberry
        message = "Raspberry no ha solicitado conexion. Aprete el boton en Raspberry."

    elif 'si' in command: #Dispositivo acepto conexion
        message = "Conectado al Raspberry Pi :D"
        print("\n\nDispositivo conectado :D")

        if(GPIO.output(green)==False):
            GPIO.output(green,True) # Prende LED verde
        
        
    elif 'no' in command: #Dispositivo nego conexion
        message = "Usted nego la conexion"
        print("\n\nDispositivo nego conexion :(")

        for x in range(0, 3): # 0,1,2 / 3 veces
            if(GPIO.output(green)==True):
                GPIO.output(green,False) # Apaga LED verde
                sleep(1) # Pausa de 1 seg
                GPIO.output(green,True) # Prende LED verde
                sleep(1) # Pausa de 1 seg
                GPIO.output(green,False) # Apaga LED verde
                sleep(1) # Pausa de 1 seg
            else:
                GPIO.output(green,True) # Prende LED verde
                sleep(1) # Pausa de 1 seg
                GPIO.output(green,False) # Apaga LED verde
                sleep(1) # Pausa de 1 seg
            

    elif 'stop' in command: #Terminar programa
        stop = 1
        message = "Usted termino el programa"
        print("\n\nDispositivo terminando programa...")

        for x in range(0, 3): # 0,1,2 / 3 veces
            if(GPIO.output(green)==True):
                GPIO.output(green,False) # Apaga LED verde
                GPIO.output(green,True) # Prende LED verde
                GPIO.output(green,False) # Apaga LED verde
            else:
                GPIO.output(green,True) # Prende LED verde
                GPIO.output(green,False) # Apaga LED verde

    else: #Comando invalido
        message = ("\nIntroduzca (en minuscula): "
        "\n\t\"si\" - para permitir conexion "
        "\n\t\"no\" - para negar conexion "
        "\n\t\"stop\" - para apagar programa "
        "\n\n")
    
        
    telegram_bot.sendMessage(chat_id,message) #Bot manda mensaje
        

# ---------------------- PROGRAMA MAIN ---------------------------

print("Presiona boton para solicitar conexion\n\n")

while(on==0): #Mientras boton no ha sido presionado

    if(GPIO.input(yellow)==True): #Si boton presionado
        os.system('clear') #Limpiar pantalla
        on=1   #Boton fue presionado
        print("Boton presionado\n\n")
        sleep(1)

        os.system('clear')

        #telegram_id = input("Introduzca ID de Telegram del Dispositivo: ") # Introducir id de usuario Telegram
        telegram_id = 123456789 # id de usuario Telegram (Pon el tuyo)

        #telegram_bot = sys.argv[1] #Para adquerir bot token del terminal como argumento
        telegram_bot = telepot.Bot('Aqui va token de Telegram bot') #HTTP API para Telegram Bot
        
        sleep(1)
        if(telegram_bot.getMe() is None):
            stop = 1
            print("Error con bot")
        else:
            print(telegram_bot.getMe()) #Enseñar info de bot
            sleep(1)

    
#Si no hubo error con Telegram bot
if(stop == 0):
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
    
    sleep(10)

    #Timeout
    if(message == "no_reply"): #Si dispositivo no respondio despues de 10 segundos
        print("\n\n * *No hubo respuesta del dispositivo* *"
        "\n\nTerminando programa\n\n")
        stop = 1


while (stop==0): #Minetras no se le ha dicho al programa que termine
    #haz algo
    sleep(10)

GPIO.cleanup() #Limpia puertos GPIO
print("\n\nPrograma terminado")

