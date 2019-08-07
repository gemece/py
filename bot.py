import telebot
import time
import prueba
import aemet
import canciones
TOKEN = "801717901:AAE7f2lehXmP19B0EklfSnclw3DfAs5e8iY"

bot = telebot.TeleBot(TOKEN)


# Con esto, estamos definiendo una función llamada 'listener', que recibe como parámetro un dato llamado 'messages'.
def listener(messages):

	for m in messages:  # Por cada dato 'm' en el dato 'messages'

		cid = m.chat.id  # El Cid es el identificador del chat los negativos son grupos y positivos los usuarios

		if cid > 0:

			# Si 'cid' es positivo, usaremos 'm.chat.first_name' para el nombre.
			mensaje = str(m.chat.first_name) + " [" + str(cid) + "]: " + m.text

		else:

			# Si 'cid' es negativo, usaremos 'm.from_user.first_name' para el nombre.
			mensaje = str(m.from_user.first_name) + \
				"[" + str(cid) + "]: " + m.text

		# Abrimos nuestro fichero log en modo 'Añadir'.
		f = open('log.txt', 'a')

		f.write(mensaje + "\n")  # Escribimos la linea de log en el fichero.

		f.close()  # Cerramos el fichero para que se guarde.

		print(mensaje)


# Así, le decimos al bot que utilice como función escuchadora nuestra función 'listener' declarada arriba.
bot.set_update_listener(listener)


# Indicamos que lo siguiente va a controlar el comando '/ayuda'
@bot.message_handler(commands=['ayuda'])
def command_ayuda(m):  # Definimos una función que resuleva lo que necesitemos.

	cid = m.chat.id  # Guardamos el ID de la conversación para poder responder.

	bot.send_chat_action(cid, 'typing')  # Enviando ...

	time.sleep(1)  # La respuesta del bot tarda 1 segundo en ejecutarse

	# Con la función 'send_message()' del bot, enviamos al ID almacenado el texto que queremos.
	bot.send_message(cid, "AYUDA")


# Comando para la prediccion del tiempo
@bot.message_handler(commands=['tiempo'])
def command_tiempo(t):

	cid = t.chat.id
	ciudad = t.text.split('/tiempo')[1].strip()

	if ciudad is not '':
		resultado = prueba.tiempo(ciudad)
		if resultado["cod"] != "404":
			for i in resultado["list"]:
				# store the value of "main"
				# key in variable y
				y = i['main']
				# store the value corresponding
				# to the "temp" key of y
				current_temperature = y["temp"]
				current_temperature -= 273.15
				# store the value corresponding
				# to the "pressure" key of y
				current_pressure = y["pressure"]
				# store the value corresponding
				# to the "humidity" key of y
				current_humidiy = y["humidity"]
				temp_min = y["temp_min"]
				temp_min -= 273.15
				temp_max = y["temp_max"]
				temp_max -= 273.15
				# store the value of "weather"
				# key in variable z
				z = i["weather"]
				# store the value corresponding
				# to the "description" key at
				# the 0th index of z
				weather_description = z[0]["description"]
				fecha = i["dt_txt"]
				text = "Fecha y hora: " + str(fecha) + "\n"
				bot.send_message(cid, text)
				# print following values
				text = " Temperature ºC = " + str(round(current_temperature, 2)) + "\n presion atmosférica (hPa) = " + str(current_pressure) + "\n humedad % = " + str(
					current_humidiy) + "\n descripcion = " + str(weather_description) + "\n temperatura Max = " + str(round(temp_max, 2)) + "\n temperatura Min = " + str(round(temp_min, 2))
				bot.send_message(cid, text+"\n")

		else:
			bot.send_message(cid, " Ciudad no encontrada ")
	else:
		bot.send_message(cid, " Ciudad no encontrada ")


@bot.message_handler(commands=['aemet'])
def command_aemet(t):
	cid = t.chat.id
	ciudad = t.text.split('/aemet')[1].strip()
	print(ciudad)
	if ciudad is not '':
		x = aemet.tiempo(ciudad)
		if x is not None:
			for i in x['prediccion']['dia']:
				fecha = i['fecha']
				res = "Dia " + fecha
				probPrecipitacion = i['probPrecipitacion'][0]
				if(len(probPrecipitacion) > 1):
					res1 = "{} H ---> Probabilidad de precipitacion {} %".format(probPrecipitacion['periodo'], probPrecipitacion['value'])
				else:
					res1 = "00-24 H ---> Probabilidad de precipitacion {} %".format(probPrecipitacion['value'])

				estadoCielo = i['estadoCielo'][0]
				if(len(estadoCielo) > 2):
					res2 = "{} ---> {}".format(estadoCielo['periodo'], estadoCielo['descripcion'])
				else:
					res2 = "00-24 H ---> {}".format(estadoCielo['descripcion'])

				temperatura = i['temperatura']
				res3 = "Temperatura Maxima {}\nTemperatura Minima {}".format(temperatura['maxima'], temperatura['minima'])

				sensTermica = i['sensTermica']
				res4 = "Sensacion Termica Maxima {}\nSensacion Termica Minima {}".format(sensTermica['maxima'], sensTermica['minima'])

				humedadRelativa = i['humedadRelativa']
				res5 = "Humedad Maxima {} %\nHumedad Minima {} %\n".format(humedadRelativa['maxima'], humedadRelativa['minima'])
				
				bot.send_message(cid, res + "\n" + res1 + "\n" + res2 + "\n" + res3 + "\n" + res4 + "\n" + res5 + "\n")
		else:
			bot.send_message(cid, " Ciudad no encontrada ")
	else:
		bot.send_message(cid, " Ciudad no encontrada ")


bot.polling()
#@bot.message_handler(commands=['spotify'])
#def command_spotify(s):
#
#	cid = s.chat.id
#	playlist = s.text.split('/aemet')[1].strip()
#	canciones.tracks(playlist)







