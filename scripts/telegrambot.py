# -*- coding: utf-8 -*-

import telebot #Librería de la API del bot.
from telebot import types #Tipos para la API del bot.
import time #Librería para esperar delays. Sirve para hacer que el programa que controla el bot no se acabe.
#import random #Librería para crear numeros random
import token
import os #Librería para ejecutar comandos de shell
import commands #Librería para ejecutar comandos de shell
import re
#import requests #Librería para realizar peticiones y solicitudes a urls
import wget #Liberria para descargar archivos de links y urls
from subprocess import call

#Nuestro token del bot. Se obtiene desde @BotFather dentro de telegram
TOKEN = '123456789:ahabsufOA29Uaohsf289724ahrAEGasmfgp680q'
#Creamos el objeto de nuestro bot.
bot = telebot.TeleBot(TOKEN)


#############################################
#Listener
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
