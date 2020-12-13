import RPi.GPIO as GPIO
import datetime
import time
import serial
import pandas as pd
import numpy as np

init = False

GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme


def get_soil_moisture(data = [], seri='/dev/ttyACM2'):
	import serial

	ser = serial.Serial(seri, 9600)

	for i in range(100):

		print(int(ser.readline()))
		data.append(int(ser.readline()))

	return data

def sample_data(wet_or_dry, sample):
	import datetime

	time_now = datetime.datetime.now()

	if wet_or_dry=='wet':
#		df = pd.read_csv('wet.csv')
		df = pd.DataFrame({'water_moisture_reading': sample})
#		df = df.append(df_new)
		df.to_csv('wet.csv', index=False)
		print(df)
		return df
	elif wet_or_dry=='dry':
		df = pd.read_csv('dry.csv')
		df_new = pd.DataFrame({'dry_moisture_reading': sample})
		for i,r in df.iterrows():
			print(r)
		df = df.append(df_new)
		df.to_csv('dry.csv', index=False)
		return df

def calibrate_sensor():
	import statistics
	import datetime

	time_now = datetime.datetime.now()

	wet_readings = pd.read_csv('wet.csv')
	dry_readings = pd.read_csv('dry.csv')

	print(wet_readings)

	Q1_wet = wet_readings.quantile(q=.25)
	Q3_wet = wet_readings.quantile(q=.75)
	IQR_wet = Q3_wet - Q1_wet

	print(IQR_wet)

	Q1_dry = dry_readings.quantile(q=.25)
	Q3_dry = dry_readings.quantile(q=.75)
	IQR_dry = Q3_dry - Q1_dry

	print(IQR_dry)




def get_last_watered():
	try:
		f = open("last_watered.txt", "r")
		for line in f:
			pass
		print(line)
	except:
		print("Never watered")

def init_output(pin):
	GPIO.setup(pin, GPIO.OUT)


def auto_water(pump_pin = 8, water_sensor_pin = 8):
	import serial

	ser = serial.Serial('/dev/ttyACM2', 9600)


	water = 260
	air = 574
	percentage_unit = water - air
	init_output(pump_pin)
	place = 1

	try:
		while True:
			count = 0
			try:
				line = int(ser.readline())
				count += 1
			except:
				continue
			try:
				line += int(ser.readline())
				count += 1
			except:
				continue
			try:
				line += int(ser.readline())
				count += 1
			except:
				continue

			readings = (line/count * -1 + air)/(3.14)
			if readings > 0 and readings < 110:
				print('Moisture for plant 1: ', readings, '%')

				now = datetime.datetime.now()

				if ((now.hour == 11 or now.hour == 23) and (now.minute == 13)):
					print('Checking Water for Sensor 1')

					if readings < 50:
						pump_on(pump_pin=7, delay=1)
						print('Watered Space 1 at ', now.strftime('%Y-%m-%d %H:%M:%S'))

	except KeyboardInterrupt:
		GPIO.cleanup()


def pump_on(pump_pin = 7, delay = 1):
	init_output(pump_pin)
#	f = open("last_watered.csv", "a")
#	f.write('\n')
#	f.write(datetime.datetime.now().strftime("%b/%d/%Y %-I:%M:$S"))
#	f.save()
#	f.close()

	GPIO.output(pump_pin, GPIO.LOW)
	time.sleep(delay)
	GPIO.output(pump_pin, GPIO.HIGH)
	time.sleep(delay)


#print(get_soil_moisture())
# pump_on(pump_pin=10, delay=1)
auto_water()



#caliborate_sensor()
