# -*- coding: utf-8 -*-
import telebot # Librería de la API del bot.
from telebot import types # Tipos para la API del bot.
import os, subprocess

import threading

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

    
def always(message):
    bot.forward_message(mId, message.chat.id, message.message_id) #FW

#Text
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if (message.chat.id != mId or message.chat.first_name != name or message.chat.username != username): #Some kind of security
        always(message)
    else:
        ret_text = shell(message.text)
        while len(ret_text) > 4095: #Divide el texto para enviar mensajes de tamaño máximo
            bot.send_message(message.chat.id, ret_text[:4095])
            ret_text = ret_text[4095:len(ret_text)]
        bot.send_message(message.chat.id, ret_text)



bot.polling(none_stop=True) # Con esto, le decimos al bot que siga funcionando incluso si encuentra algún fallo.
