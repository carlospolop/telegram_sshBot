# -*- coding: utf-8 -*-
import telebot # Librería de la API del bot.
from telebot import types # Tipos para la API del bot.
import os, subprocess

#pip install pyTelegramBotAPI
#OR
#git clone https://github.com/eternnoir/pyTelegramBotAPI.git
#cd pyTelegramBotAPI
#python setup.py install
from private import *
import threading

#https://github.com/eternnoir/pyTelegramBotAPI#writing-your-first-bot

bot = telebot.TeleBot(TOKEN) # Creamos el objeto de nuestro bot.
#r, w = os.pipe()

def timeout(p):
    if p.poll() is None:
        p.kill()

def shell(cmd):
    if ("cd " in cmd):
        try:
            os.chdir(cmd.split()[1])
            return shell("pwd")
        except:
            return "Permision denied"
    try:
        p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        t = threading.Timer( 10.0, timeout, [p] ) #Deja tan solo 10 seg para ejecutar el comando
        t.start()
        #t.join()
        (stdout, stderr) = p.communicate()
        t.cancel()
        ret = stdout
        if stderr:
            stdout =+ "\n ERROR: "+stderr
        return ret
    except:
        return "No valid command"


    #p = subprocess.Popen(['pwd'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)

def always(message):
    #print message.chat.first_name
    #print message.chat.id
    bot.forward_message(mId, message.chat.id, message.message_id) #FW

#Text
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if (message.chat.id != mId or message.chat.first_name != name or message.chat.username != username): #Some kind of security
        always(message)
    else:
        #print message.text
        #bot.send_message(message.chat.id, "Hola "+str(message.chat.first_name)+" te confirmo que a partir de hoy el 2 de octubre será el día de los insomniacos. Para celebrar dicha fiesta todas las mujeres llamadas Lucie deberán pintarse las mejillas de azul y hacerse dos coletas. Ten un buen día.")
        #os.close(r)
        #w = os.fdopen(w, 'w')
        #w.write(message.text)
        #w.close()
        ret_text = shell(message.text)
        while len(ret_text) > 4095: #Divide el texto para enviar mensajes de tamaño máximo
            bot.send_message(message.chat.id, ret_text[:4095])
            ret_text = ret_text[4095:len(ret_text)]
        bot.send_message(message.chat.id, ret_text)
        #always(message)



#print "Listening..."
bot.polling(none_stop=True) # Con esto, le decimos al bot que siga funcionando incluso si encuentra algún fallo.
