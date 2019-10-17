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
mac_enciende_PC_magic_packet = "FF:FF:FF:FF:FF:FF"

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
				#El numero entre corchetes es nuestro ID unico para el chat
				print "[" + str(cid) + "]: " + m.text

	#Así, le decimos al bot que utilice como función escuchadora nuestra función 'listener' declarada arriba.
	bot.set_update_listener(listener)

	
#############################################
#Funciones
#---------------------------------------------- Básicos ----------------------------------------------
	@bot.message_handler(commands=['start'])
	def command_hola(m):
	        cid = m.chat.id
	        bot.send_message(cid, "Bot iniciado!")
	
	@bot.message_handler(commands=['cmd'])
	def command_ayuda(m):
		cid = m.chat.id
		bot.send_message(cid, [ "Comandos disponibles:" +
					"\n/temp" +
					"\n/public_ip" +
					"\n/servicio_vsftpd" +
					"\n/servicio_smbd" +
			                "\n/servicio_ssh" +
        			        "\n/servicio_vnc" +
					"\n/log" +
					"\n/nota_rapida" +
					"\n/enciende_PC_magic_packet" +
					"\n/reiniciar" +
					"\n/apagar" +
					"\n/apagado_programado" +
					"\n/cancelar_apagado" +
					"\n/temp_except"])

	@bot.message_handler(commands=['temp'])
	def command_temp(m):
		cid = m.chat.id
		temp = commands.getoutput('sudo /opt/vc/bin/vcgencmd measure_temp | cut -f2 -d=')
		bot.send_message(cid, temp)

	@bot.message_handler(commands=['public_ip'])
	def command_publicip(m):
		publicip = commands.getoutput('wget -qO- ifconfig.co/ip')
		bot.send_message(cid, "Direccion publica: " + publicip)
		
	@bot.message_handler(commands=['log'])
	def command_log(m):
		cid = m.chat.id
		log = open('/var/log/syslog', 'rb')
		bot.send_document(cid, log)
		
	@bot.message_handler(commands=['enciende_PC_magic_packet'])
	def command_enciende_PC_magic_packet(m):
		cid = m.chat.id
		command = 'sudo wakeonlan ' + mac_enciende_PC_magic_packet
		os.system(command)
		bot.send_message(cid, "Encendiendo PC...")
		
	@bot.message_handler(commands=['reiniciar'])
	def command_reiniciar(m):
		cid = m.chat.id
		bot.send_message(cid, "Reiniciando...")
		time.sleep(4)
		commands.getoutput('sudo reboot')
	
	@bot.message_handler(commands=['apagar'])
	def command_apagar(m):
		cid = m.chat.id

		markup = types.ReplyKeyboardMarkup(row_width=2)
		yesbtn = types.KeyboardButton('Si')
		nobtn = types.KeyboardButton('No')
		markup.add(yesbtn, nobtn)

		bot.send_message(cid, "¿De verdad deseas apagar el servidor?", reply_markup=markup)

		@bot.message_handler(regexp = 'Si')
		def command_apagar_yes(m):
			#Llamamos a un metodo para quitar el teclado y lo guardamos en la variable
			markup = types.ReplyKeyboardRemove(selective=False)
			#Enviamos un mensaje y sustituimos el teclado por removeteclado. Ya no hay teclado
			bot.send_message(cid, "Apagando...", reply_markup=markup)
			time.sleep(4)
			os.system('sudo shutdown now')
		
		@bot.message_handler(regexp = 'No')
		def command_apagar_no(m):
			cid = m.chat.id
			#Llamamos a un metodo para quitar el teclado y lo guardamos en la variable
			markup = types.ReplyKeyboardRemove(selective=False)
			#Enviamos un mensaje y sustituimos el teclado por removeteclado. Ya no hay teclado
			bot.send_message(cid, "Operación cancelada", reply_markup=markup)

	@bot.message_handler(commands=['temp_except'])
	def excepcion(m):
		os.system('sudo python /home/pi/scripts/TelegramBot_temp_except.py &')
	
	@bot.message_handler(commands=['apagado_programado'])
	def command_apagado_programado(m):
		cid = m.chat.id

		markup = types.ReplyKeyboardMarkup(row_width=3)
		itembtn1 = types.KeyboardButton('10 min')
		itembtn2 = types.KeyboardButton('20 min')
		itembtn3 = types.KeyboardButton('30 min')
	        itembtn4 = types.KeyboardButton('45 min')
	        itembtn5 = types.KeyboardButton('1 h')
	        itembtn6 = types.KeyboardButton('1 h 30 min')
	        itembtn7 = types.KeyboardButton('2 h')
	        itembtn8 = types.KeyboardButton('2 h 30 min')
		itembtn9 = types.KeyboardButton('3 h')
		markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8, itembtn9)

		bot.send_message(cid, "Elije el tiempo en el que desea que se apague el servidor:", reply_markup=markup)

	        @bot.message_handler(regexp = '10 min')
	        def command_apagar_en(m):
	        	#Llamamos a un metodo para quitar el teclado y lo guardamos en la variable
	        	markup = types.ReplyKeyboardRemove(selective=False)
	        	#Enviamos un mensaje y sustituimos el teclado por removeteclado. Ya no hay teclado
	                bot.send_message(cid, "Apagado programado en 10 minutos", reply_markup=markup)
		        #Ejecuta el comando para apagar la raspberry en 10 minutos
			commands.getoutput('sudo shutdown -h +10')

		#El resto de instruciones de mas abajo hacen exactamente lo mismo, pero cambiando el tiempo en el que se
		#apagrá el servidor

	        @bot.message_handler(regexp = '20 min')
	        def command_apagar_en(m):
	        	markup = types.ReplyKeyboardRemove(selective=False)
	                bot.send_message(cid, "Apagado programado en 20 minutos", reply_markup=markup)
	                commands.getoutput('sudo shutdown -h +20')

	        @bot.message_handler(regexp = '30 min')
	        def command_apagar_en(m):
	        	markup = types.ReplyKeyboardRemove(selective=False)
	                bot.send_message(cid, "Apagado programado en 30 minutos", reply_markup=markup)
	                commands.getoutput('sudo shutdown -h +30')

	        @bot.message_handler(regexp = '45 min')
	        def command_apagar_en(m):
	        	markup = types.ReplyKeyboardRemove(selective=False)
	                bot.send_message(cid, "Apagado programado en 45 minutos", reply_markup=markup)
	                commands.getoutput('sudo shutdown -h +45')

	        @bot.message_handler(regexp = '1 h')
	        def command_apagar_en(m):
	        	markup = types.ReplyKeyboardRemove(selective=False)
	                bot.send_message(cid, "Apagado programado en 1 hora", reply_markup=markup)
	                commands.getoutput('sudo shutdown -h +60')

	        @bot.message_handler(regexp = '1 h 30 min')
	        def command_apagar_en(m):
	        	markup = types.ReplyKeyboardRemove(selective=False)
	                bot.send_message(cid, "Apagado programado en 1 hora y 30 minutos", reply_markup=markup)
	                commands.getoutput('sudo shutdown -h +90')

	        @bot.message_handler(regexp = '2 h')
	        def command_apagar_en(m):
	        	markup = types.ReplyKeyboardRemove(selective=False)
	                bot.send_message(cid, "Apagado programado en 2 horas", reply_markup=markup)
	                commands.getoutput('sudo shutdown -h +120')

	        @bot.message_handler(regexp = '2 h 30 min')
	        def command_apagar_en(m):
	        	markup = types.ReplyKeyboardRemove(selective=False)
	                bot.send_message(cid, "Apagado programado en 2 horas y 30 minutos", reply_markup=markup)
	                commands.getoutput('sudo shutdown -h +150')

	        @bot.message_handler(regexp = '3 h')
	        def command_apagar_en(m):
	        	markup = types.ReplyKeyboardRemove(selective=False)
	                bot.send_message(cid, "Apagado programado en 3 horas", reply_markup=markup)
	                commands.getoutput('sudo shutdown -h +180')

	@bot.message_handler(commands=['cancelar_apagado'])
	def command_cancelar_apagado(m):
		cid = m.chat.id
		commands.getoutput('sudo shutdown -c')
		bot.send_message(cid, "El apagado programado se ha cancelado")
		
