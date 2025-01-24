# -*-coding:utf-8
#Se importan las librerías
import RPi.GPIO as GPIO
import time
import signal
from mfrc522 import SimpleMFRC522
import max30102_1
import numpy as np
import paho.mqtt.publish as publish
import psutil
import string
import serial
from mfrc522 import SimpleMFRC522
import os
import sys
import paho.mqtt.client as mqtt
import json
import random
from datetime import datetime

global continue_reading
continue_reading = True 


# Configuración del canal y MQTT
channel_ID = "2295945"
mqtt_host = "mqtt3.thingspeak.com"
mqtt_client_ID = "HjkiJyQcGSsoDDkmKQAeGTU"
mqtt_username = "HjkiJyQcGSsoDDkmKQAeGTU"
mqtt_password = "YC7UcKeGEzyJK7gNUoayvk9u"
t_transport = "TCP"
t_port = 1883

# Crear el tema MQTT
topic = "channels/{}/publish".format(channel_ID)

#Credenciales para enviar datos a Thingsboard
THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 'naVYbRYRc4FRL8NG2fBG'

# Configuración del intervalo de tiempo de generacion de datos y subida a TB
INTERVAL=2

sensor_data = {'SPo2': 0, 'Hr': 0, 'Fecha_envio': 0, 'Duracion_minutos':0, 'Duracion_segundos':0}
next_reading = time.time() 
client = mqtt.Client()

# Configuracion del username (en el caso de TB es el ACCESS TOKEN)
client.username_pw_set(ACCESS_TOKEN)

# Conexion a ThingsBoard usando MQTT con 60 segundos de duracion de la sesion (keepalive interval)
client.connect(THINGSBOARD_HOST, 1883, 60)
client.loop_start()


#Declaración de variables de lectura RFID
GPIO.cleanup()

# Configurar el modo de los pines GPIO
GPIO.setmode(GPIO.BCM)

# Configurar el pin del buzzer
buzzer_pin = 17  # Puedes ajustar esto según el pin que estés utilizando
GPIO.setup(buzzer_pin, GPIO.OUT)

reader = SimpleMFRC522()

archivo = open("datos_rfid.txt","w")

#Lectura valor Spo2 y Hr por serial
ser = serial.Serial('/dev/ttyUSB0', 115200)
ser.flushInput()
data = ser.readline().decode('utf-8').rstrip()

#Declaración variables
cont=0
band_al = 0
band_previa = 0
time_al= 0
time_tar=0
flag_tarj=0
time_final_h=0
time_final_m=0
time_final_s=0
#Lectura de variables
print("Esperando por tarjetas RFID...")

try:
    
    while True:    
        value1=0
        value2=0    
        id = None
        
        flag_tarj=0
        
        #Lectura RFID
        if id is None:  # Esperar hasta que se detecte una tarjeta
            id, text = reader.read_no_block()  # Intentar leer la tarjeta sin bloquear
            time.sleep(0.01)  # Pequeño retardo antes de intentar nuevamente
            # Lectura de spo y hr
            if ser.inWaiting()>0:
                data = ser.readline().decode('utf-8').rstrip()
                print("Datos recibidos:", data)
                #Separación datos de entrada Spo2 Hr
                values = data.split(',')
                if len(values) ==2:
                    value1, value2 = map (float, values)
                else: 
                    print("Error: Data format incorrect")
            
        
        # Si se detecta una tarjeta
        if id is not None:
            flag_tarj=1
            band_al=0
            print("ID de la tarjeta: {}".format(id))
            time_tar= datetime.now()
            time_tar_h=int(datetime.strftime(fechaActual, '%H'))
            time_tar_m=int(datetime.strftime(fechaActual, '%M'))
            time_tar_s=int(datetime.strftime(fechaActual, '%S'))
            
            time_final_h=time_tar_h-time_al_h
            time_final_m=time_tar_m-time_al_m
            time_final_s=time_tar_s-time_al_s
            
            # Lectura de spo y hr
            if ser.inWaiting()>0:
                data = ser.readline().decode('utf-8').rstrip()
                print("Datos recibidos:", data)
                #Separación datos de entrada Spo2 Hr
                values = data.split(',')
                
                if len(values) ==2:
                    value1, value2 = map (float, values)
                else: 
                    print("Error: Data format incorrect")

        time.sleep(0.05)  # Esperar antes de intentar leer otra tarjeta
        
        #Activación Buzzer
        if 50 <= value1 <= 200: #Limita el valor de value
            value2 = 160
            if value2 > 150:
                cont+=1
                if cont>3:
                    print("Activando el buzzer")
                    band_al=1
                    GPIO.output(buzzer_pin, GPIO.HIGH)

                    # Activar el buzzer durante 10 segundos
                    time.sleep(10)

                    # Desactivar el buzzer después de 10 segundos
                    print("Desactivando el buzzer")
                    GPIO.output(buzzer_pin, GPIO.LOW)
                    
                    cont=0
            else:
                # Si value2 no es mayor a 150, asegurarse de que el buzzer esté apagado
                GPIO.output(buzzer_pin, GPIO.LOW)
                cont=0
                
            if band_al == 1 and band_previa == 0:
                time_al_h=int(datetime.strftime(fechaActual, '%H'))
                time_al_m=int(datetime.strftime(fechaActual, '%M'))
                time_al_s=int(datetime.strftime(fechaActual, '%S'))
            
            band_previa=band_al
            
            #Envío tiempo actual
            fechaActual=datetime.now()
            Fecha_envio=datetime.strftime(fechaActual, '%d/%m/%Y,%H:%M:%S')
            
            # Construir la carga útil
            payload = "field1={:.2f}&field2={:.2f}".format(value1, value2)

            try:
                print("Escribiendo Payload =", payload, "a host:", mqtt_host, "clientID =", mqtt_client_ID)
                publish.single(topic, payload, hostname=mqtt_host, transport=t_transport, port=t_port, client_id=mqtt_client_ID, auth={'username': mqtt_username, 'password': mqtt_password})
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(e)

            #Esperar antes de enviar el siguiente conjunto de datos (por ejemplo, cada 20 segundos)
            time.sleep(0.5)
                  
            print("SPo2", value1, "Hr: ", value2)
            sensor_data['SPo2'] = value1
            sensor_data['Hr'] = value2
            sensor_data['Fecha_envio']=Fecha_envio
            sensor_data['Duracion_minutos'] = time_final_m
            sensor_data['Duracion_segundos']= time_final_s

            # Enviando los datos a ThingsBoard
            client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
            print("Entre a TB y revise el campo LATEST TELEMETRY en su dispositivo")
            print(sensor_data)
            next_reading += INTERVAL
            sleep_time = next_reading-time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)
        else:
            print("Adquiriendo datos")

except KeyboardInterrupt:
    continue_reading = False
    client.loop_stop()
    client.disconnect()
    archivo.close()
    GPIO.cleanup()
    pass
