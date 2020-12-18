
import RPi.GPIO as GPIO
import datetime
import time
from nanpy import (ArduinoApi, SerialManager)
from time import sleep


GPIO.setmode(GPIO.BOARD)

def water_read_moisture(pin='A0'):

	air = 580
	water = 277

	connection = SerialManager()
	a = ArduinoApi(connection = connection)

	a.pinMode(pin, 'INPUT')
	moisture_read = ((a.analogRead(pin) * -1) + air)/3.05

	return moisture_read


def pump_on(pump_pin = 7, delay = 1):
	GPIO.setup(pump_pin, GPIO.OUT)
	GPIO.output(pump_pin, GPIO.LOW)
	time.sleep(delay)
	GPIO.output(pump_pin, GPIO.HIGH)


def auto_water():

	reading = water_read_moisture()

	print('Plant1 Moisture is: ', reading, '     Time is: ', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '\n')

	now = datetime.datetime.now()

	if ((reading > -5) and (reading < 110) and (now.hour == 10) and (now.minute == 59)):

		if reading < 45:
			pump_on()
			print('Watered Space 1') 

#		pin2 = 'A5'
#		connection = SerialManager()
#		a = ArduinoApi(connection = connection)
#		a.pinMode(pin2, 'INPUT')
#
#		moisture_read2 = a.analogRead(pin2)
#		print('Plant2 Moisture is: ', moisture_read2, '\n')


count = 0

while count < 27:

	auto_water()

	print(count)

	count += 1

#pump_on()
