import RPi.GPIO as GPIO
import datetime
import time
import pandas as pd
import numpy as np

init = False

GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme

def get_soil_moisture(channel, interval_for_readings=0.0001, number_of_intervals = 10):
	import spidev
	import time

	spi = spidev.SpiDev()
	spi.open(0,0)

	if channel > 7 or channel < 0:
		return 'check ADC Channel'
	r = spi.xfer([1, 8 + channel << 4, 0])
	data = ((r[1] & 3) << 8 + r[2])


	time.sleep(interval_for_readings)

	return data

def sample_data(wet_or_dry, sample):
	import datetime

	time_now = datetime.datetime.now()

	if wet_or_dry=='wet':
		df = pd.read_csv('wet.csv').iloc[:,0]
		index = df.index
		df = df.append(pd.Series(sample, index=[time_now]))
#		print(df)
		return df
	elif wet_or_dry=='dry':
		df = pd.read_csv('dry.csv').iloc[:,0]
		index = df.index
		df = df.append(pd.Series(sample, index=[time_now]))
		return df

def calibrate_sensor():
	import statistics
	import datetime

	time_now = datetime.datetime.now()

	wet_readings = pd.read_csv('wet.csv').iloc[:,0]
	dry_readings = pd.read_csv('dry.csv').iloc[:,0]

	Q1_wet = wet_readings.quantile(q=.25)
	Q3_wet = wet_readings.quantile(q=.75)
	IQR_wet = Q3_wet - Q1_wet

	wet_readings = wet_readings[~((wet_readings < (Q1_wet-1.5*IQR_wet)) | (wet_readings > (Q3_wet+1.5*IQR_wet)))]

	wet_readings_mean = statistics.mean(wet_readings)
	print('wet average', wet_readings_mean)
	wet_readings_std = statistics.stdev(wet_readings)
	wet_readings_skew = wet_readings.skew(axis = 0)

	dry_readings_mean = statistics.mean(dry_readings)
	print('dry average', dry_readings_mean)
	dry_readings_std = statistics.stdev(dry_readings)
	dry_readings_skew = dry_readings.skew(axis = 0)

	print('wet std', wet_readings_std)
	print('dry std', dry_readings_std)

	print('wet skew', wet_readings_skew)
	print('dry skew', dry_readings_skew)


def get_last_watered():
	try:
		f = open("last_watered.txt", "r")
		for line in f:
			pass
		print(line)
	except:
		print("Never watered")

def get_status(pin = 8):
	try:
		GPIO.setup(pin, GPIO.IN)
		print("moisture reading: ",GPIO.input(pin))
		return GPIO.input(pin)
	except:
		print('Check Moisture Sensor')

def init_output(pin):
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.LOW)
	GPIO.output(pin, GPIO.HIGH)

def auto_water(delay = 5, pump_pin = 8, water_sensor_pin = 8):
	consecutive_water_count = 0
	init_output(pump_pin)
	print("Here we go! Press CTRL + C to exit")
	try:
		while True and consecutive_water_count < 10:
			time.sleep(delay)
			wet = get_status(pin = water_sensor_pin) == 0
			if not wet:
				if consecutive_water_count < 5:
					pass #	pump_on(pump_pin, 1)
				consecutive_water_count += 1
			else:
				consecutive_water_count = 0
	except KeyboardInterrupt:
		GPIO.cleanup()


def pump_on(pump_pin = 7, delay = 1):
	init_output(pump_pin)
	f = open("last_watered.csv", "a")
	f.write('\n')
	f.write(datetime.datetime.now())
	f.save()
	f.close()

	BPIO.output(pump_pin, GPIO.LOW)
	time.sleep(delay)
	GPIO.output(pump_pin, GPIO.HIGH)

#moisture = 0

#for i in range(1000):
#	moisture -= get_soil_moisture(0)

#reading = moisture/1000
#reading = reading*10**-10
#print(reading)

#data = sample_data('dry', reading)
#data.to_csv('dry.csv', index=False)
#time.sleep(1)


calibrate_sensor()
