import RPi.GPIO as GPIO
import datetime
import time


init = False

GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme

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
