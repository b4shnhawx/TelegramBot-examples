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
		
	@bot.message_handler(commands = ['servicio_smbd'])
	def command_servicio_smbd(m):
		cid = m.chat.id

		markup = types.ReplyKeyboardMarkup(row_width=1)
	      	status = types.KeyboardButton('Status SMB')
	        start = types.KeyboardButton('Start SMB')
	        restart = types.KeyboardButton('Restart SMB')
	        stop = types.KeyboardButton('Stop SMB')

		markup.add(status, start, restart, stop)

	        bot.send_message (cid, "Que deseas hacer?", reply_markup=markup)

		@bot.message_handler(regexp = 'Status SMB')
		def command_servicio_smbd_status(m):
			state = commands.getoutput('sudo service smbd status')

			if 'active (running)' in state:
				bot.send_message(cid, "Estado del servicio SMB: Active (running)")
			elif 'inactive (dead)' in state:
				bot.send_message(cid, "Estado del servicio SMB: Inactive (dead)")

		@bot.message_handler(regexp = 'Start SMB')
	        def command_servicio_smbd_start(m):
	        	commands.getoutput('sudo service smbd start')
			bot.send_message(cid, "Activando servicio")
			time.sleep(25)
			command_servicio_smbd_status(m)

	       	@bot.message_handler(regexp = 'Restart SMB')
	       	def command_servicio_smbd_restart(m):
	        	commands.getoutput('sudo service smbd restart')
	        	bot.send_message(cid, "Reiniciando servicio")
	        	time.sleep(2)
	        	command_servicio_smbd_status(m)

	        @bot.message_handler(regexp = 'Stop SMB')
	        def command_servicio_smbd_stop(m):
	        	commands.getoutput('sudo service smbd stop')
	        	bot.send_message(cid, "Desactivando servicio")
	        	time.sleep(2)
	        	command_servicio_smbd_status(m)

	@bot.message_handler(commands = ['servicio_vsftpd'])
	def command_servicio_vsftpd(m):
	        cid = m.chat.id

		markup = types.ReplyKeyboardMarkup(row_width=1)
		status = types.KeyboardButton('Status FTP')
		start = types.KeyboardButton('Start FTP')
		restart = types.KeyboardButton('Restart FTP')
		stop = types.KeyboardButton('Stop FTP')

		markup.add(status, start, restart, stop)

		bot.send_message (cid, "Que deseas hacer?", reply_markup=markup)

		@bot.message_handler(regexp = 'Status FTP')
		def command_servicio_vsftpd_status(m):
			state = commands.getoutput('sudo service vsftpd status')

			if 'active (running)' in state:
				bot.send_message(cid, "Estado del servicio FTP: Active (running)")
			elif 'inactive (dead)' in state:
				bot.send_message(cid, "Estado del servicio FTP: Inactive (dead)")

		@bot.message_handler(regexp = 'Start FTP')
		def command_servicio_vsftpd_start(m):
			commands.getoutput('sudo service vsftpd start')
			bot.send_message(cid, "Activando servicio")
			time.sleep(5)
			command_servicio_vsftpd_status(m)

		@bot.message_handler(regexp = 'Restart FTP')
		def command_servicio_vsftpd_restart(m):
			commands.getoutput('sudo service vsftpd restart')
			bot.send_message(cid, "Reiniciando servicio")
			time.sleep(2)
			command_servicio_vsftpd_status(m)

		@bot.message_handler(regexp = 'Stop FTP')
		def command_servicio_vsftpd_stop(m):
			commands.getoutput('sudo service vsftpd stop')
			bot.send_message(cid, "Desactivando servicio")
			time.sleep(2)
			command_servicio_vsftpd_status(m)


	@bot.message_handler(commands = ['servicio_ssh'])
	def command_servicio_ssh(m):
		cid = m.chat.id

		markup = types.ReplyKeyboardMarkup(row_width=1)
	 	status = types.KeyboardButton('Status SSH')
	 	start = types.KeyboardButton('Start SSH')
	 	restart = types.KeyboardButton('Restart ssh')
	 	stop = types.KeyboardButton('Stop SSH')

	 	markup.add(status, start, restart, stop)

	 	bot.send_message (cid, "Que deseas hacer?", reply_markup=markup)

	 	@bot.message_handler(regexp = "Status SSH")
	 	def command_servicio_ssh_status(m):
			cid = m.chat.id
	 		state = commands.getoutput('sudo service ssh status')

	 		if 'active (running)' in state:
	 			bot.send_message(cid, "Estado del servicio SSH: Active (running)")
	                elif 'inactive (dead)' in state:
        	        	bot.send_message(cid, "Estado del servicio SSH: Inactive (dead)")

	                @bot.message_handler(regexp = 'Start SSH')
	                def command_servicio_ssh_start(m):
	                        commands.getoutput('sudo service ssh start')
	                        bot.send_message(cid, "Activando servicio")
	                        time.sleep(5)
	                        command_servicio_ssh_status(m)

	                @bot.message_handler(regexp = 'Restart SSH')
	                def command_servicio_ssh_restart(m):
	                        commands.getoutput('sudo service ssh restart')
	                        bot.send_message(cid, "Reiniciando servicio")
	                        time.sleep(2)
	                        command_servicio_ssh_status(m)

	                @bot.message_handler(regexp = 'Stop SSH')
	                def command_servicio_ssh_stop(m):
	                        commands.getoutput('sudo service ssh stop')
	                        bot.send_message(cid, "Desactivando servicio")
	                        time.sleep(2)
	                        command_servicio_ssh_status(m)

        @bot.message_handler(commands = ['servicio_vnc'])
        def command_servicio_vnc(m):
                cid = m.chat.id

                markup = types.ReplyKeyboardMarkup(row_width=1)
                status = types.KeyboardButton('Status VNC')
                start = types.KeyboardButton('Start VNC')
                restart = types.KeyboardButton('Restart VNC')
                stop = types.KeyboardButton('Stop VNC')

                markup.add(status, start, restart, stop)

                bot.send_message (cid, "Que deseas hacer?", reply_markup=markup)

                @bot.message_handler(regexp = 'Status VNC')
                def command_servicio_vnc_status(m):
                        state = commands.getoutput('sudo service vncserver-x11-serviced status')

                        if 'active (running)' in state:
                                bot.send_message(cid, "Estado del servicio VNC: Active (running)")
                        elif 'inactive (dead)' in state:
                                bot.send_message(cid, "Estado del servicio VNC: Inactive (dead)")

                @bot.message_handler(regexp = 'Start VNC')
                def command_servicio_vnc_start(m):
                        commands.getoutput('sudo service vncserver-x11-serviced start')
                        bot.send_message(cid, "Activando servicio")
                        time.sleep(5)
                        command_servicio_vnc_status(m)

                @bot.message_handler(regexp = 'Restart VNC')
                def command_servicio_vnc_restart(m):
                        commands.getoutput('sudo service vncserver-x11-serviced restart')
                        bot.send_message(cid, "Reiniciando servicio")
                        time.sleep(2)
                        command_servicio_vnc_status(m)

                @bot.message_handler(regexp = 'Stop VNC')
                def command_servicio_vnc_stop(m):
                        commands.getoutput('sudo service vncserver-x11-serviced stop')
                        bot.send_message(cid, "Desactivando servicio")
                        time.sleep(2)
                        command_servicio_vnc_status(m)
			
	@bot.message_handler(commands=['log'])
	def command_log(m):
		cid = m.chat.id
		log = open('/var/log/syslog', 'rb')
		bot.send_document(cid, log)
		
	@bot.message_handler(commands=['nota_rapida'])
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
#			print 'message.photo =', message.photo
			fileID = message.photo[-1].file_id
#			print 'fileID =', fileID
			file = bot.get_file(fileID)
#			print 'file.file_path =', file.file_path
			#https://api.telegram.org/file/bot364258304:AAEzlAMF9AFoTwLWrKyiVaASLhxXJF5qn90/photos/file_53.jpg
			#https://api.telegram.org/file/botTOKEN/rutadelafoto.jpg
			url = "https://api.telegram.org/file/bot" + TOKEN + "/" + file.file_path
#			print url

			notesNum = commands.getoutput('ls /media/pi/NAS/3-\ Quicknotes | cut -f1 -d. | sort -n | tail -n1')
			if notesNum == "":
				notesNum = 1
			else:
				notesNum = int(notesNum)
				notesNum = notesNum + 1
			notesNum = str(notesNum)

			outPath = '/media/pi/NAS/3- Quicknotes/' + notesNum + '.jpg'
			print outPath
			
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
		
	@bot.message_handler(commands=['temp_except'])
	def excepcion(m):
		os.system('sudo python /home/pi/scripts/TelegramBot_temp_except.py &')
		
