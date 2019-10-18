# -*- coding: utf-8 -*-


import telebot # Librería de la API del bot.
from telebot import types # Tipos para la API del bot.
import time # Librería para hacer que el programa que controla el bot no se acabe.
import random
from datetime import datetime, date, timedelta
import token
import os
import commands
import time
import re

TOKEN = '364258304:AAEzlAMF9AFoTwLWrKyiVaASLhxXJF5qn90' #Nuestro token del bot
bot = telebot.TeleBot(TOKEN) # Creamos el objeto de nuestro bot.

#Crea un bucle infinito para que el programa este en continua ejecución
while True:
	#Con esto, estamos definiendo una función llamada 'listener', que recibe como parámetro un dato llamado 'messages'.
	def listener(messages):
		#Por cada dato 'm' en el dato 'messages'
		for m in messages:
			#Almacenaremos el ID de la conversación.
			cid = m.chat.id
			#Y mientras que el mensaje sea texto
			if m.content_type == 'text':
				#Haremos que imprima algo parecido a esto -> [52033876]: /start
				print "[" + str(cid) + "]: " + m.text

	#Así, le decimos al bot que utilice como función escuchadora nuestra función 'listener' declarada arriba.
	bot.set_update_listener(listener)

#############################################
#Funciones

#---------------------------------------------- Básicos ----------------------------------------------
	@bot.message_handler(commands=['start'])
	def command_start(m):
	        cid = m.chat.id
	        bot.send_message(cid, "Bot iniciado!")

	@bot.message_handler(commands=['cmd'])
	def command_ayuda(m):
		cid = m.chat.id
		bot.send_message(cid, [ "Comandos disponibles:" +
					"\n/pic_saver"])


#---------------------------------------------- Almacenador de fotos ----------------------------------------------
	@bot.message_handler(commands=['pic_saver'])
	#Crea metodo con la información del mensaje (m)
	def nota_rapida(m):
		#Guarda en la variable la id del chat usando la informacion del mensaje recibido
		cid = m.chat.id
		#Envia el mensaje al usuario
		bot.send_message(cid, "Ahora las notas rápidas están activadas. Envia una foto y la guardare!")

		@bot.message_handler(content_types=['photo'])
		def photo(message):
			processPhotoMessage(message)

		def processPhotoMessage(message):
			#print 'message.photo =', message.photo
			fileID = message.photo[-1].file_id
			#print 'fileID =', fileID
			file = bot.get_file(fileID)
			#print 'file.file_path =', file.file_path
			#https://api.telegram.org/file/bot123456789:ahabsufOA29Uaohsf289724ahrAEGasmfgp680q/photos/file_53.jpg
			#https://api.telegram.org/file/botTOKEN/rutadelafoto.jpg
			url = "https://api.telegram.org/file/bot" + TOKEN + "/" + file.file_path
			#print url

			os.system('sudo mkdir /home/pi/quicknotes')
			notesNum = commands.getoutput('ls /home/pi/quicknotes | cut -f1 -d. | sort -n | tail -n1')
			if notesNum == "":
				notesNum = 1
			else:
				notesNum = int(notesNum)
				notesNum = notesNum + 1
				
			notesNum = str(notesNum)
			outPath = '/media/pi/NAS/3- Quicknotes/' + notesNum + '.jpg'
			#print outPath
			
			wget.download(url, out=outPath)

			bot.send_message(cid, notesNum + ".jpg recibida y guardada!"
