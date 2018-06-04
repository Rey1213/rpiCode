import telepot #para usar telegram en Raspberry
from telepot.loop import MessageLoop #para crear ciclo de comandos del Telegram bot

import os #para controlar sistema operativo
from time import sleep


reply = 0 #Si dispositivo respondio

stop = 0 #Para terminar el programa

message = "no_reply" #no hubo respuesta del dispositivo


#------------- ACCIONES DE TELEGRAM BOT --------------------
def action(msg):
    global message, stop

    #La "direccion" donde el Telegram bot responde
    chat_id = msg['chat']['id'] #Para que bot pueda responder
    command = msg['text'] #comando recibido
    print('\n\nComando recibido: %s' %command)

    
    if 'si' in command: #Dispositivo acepto conexion
        message = "Conectado al Raspberry Pi :D"
        print("\n\nDispositivo conectado :D")
        
    elif 'no' in command: #Dispositivo nego conexion
        message = "Usted nego la conexion"
        print("\n\nDispositivo nego conexion :(")

    elif 'stop' in command: #Terminar programa
        stop = 1
        message = "Usted termino el programa"
        print("\n\nDispositivo terminando programa...")

    else: #Comando invalido
        message = ("\nIntroduzca: "
        "\n\t\"si\" - para permitir conexion "
        "\n\t\"no\" - para negar conexion "
        "\n\t\"stop\" - para apagar programa "
        "\n\n")
    
        
    telegram_bot.sendMessage(chat_id,message) #Bot manda mensaje
        

# ---------------------- PROGRAMA MAIN ---------------------------

print("Test de Telegram Bot\n\n")

#telegram_id = input("Introduzca ID de Telegram del Dispositivo: ") # Introducir id de usuario Telegram
telegram_id = 123456789 # id de usuario Telegram (Pon el tuyo)

#telegram_bot = sys.argv[1] #Para adquerir bot token del terminal como argumento
telegram_bot = telepot.Bot('Aqui va token de Telegram bot') #HTTP API para Telegram Bot

sleep(1)
if(telegram_bot.getMe is None):
    stop = 1
    print("Error con bot")
else:
    print(telegram_bot.getMe()) #Enseñar info de bot
    sleep(1)

    
#Si no hubo error con Telegram bot
if(stop == 0):
    #Mensaje de inicio
    message = ("Test de Telegram Bot")

    #Bot manda mensaje de inicio
    telegram_bot.sendMessage(telegram_id,message)

    message = "no_reply" #Para revisar si dispositivo responde
    
    print("Esperando respuesta de dispositivo")
    MessageLoop(telegram_bot, action).run_as_thread #Esperar mensaje de dispositivo en background
    
    sleep(10)

    #Timeout
    if(message == "no_reply"): #Si dispositivo no respondio despues de 10 segundos
        print("\n\n * *No hubo respuesta del dispositivo* *"
        "\n\nTerminando programa\n\n")
        stop = 1


while (stop==0): #Minetras no se le ha dicho al programa que termine
    #haz algo
    sleep(10)
    
print("\n\nPrograma terminado")