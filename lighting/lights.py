import RPi.GPIO as GPIO
import datetime
import time


init = False

GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme

pins = [8, 10, 12, 16]

def light_on(light_pin = pins, delay = 10):

	now = datetime.datetime.now()

	GPIO.setup(light_pin[0], GPIO.OUT)
	GPIO.output(light_pin[0], GPIO.LOW)


	try:

		while True:
			if ((now.hour >= 6) and (now.hour < 20)):

				GPIO.output(light_pin[0], GPIO.HIGH)
				GPIO.output(light_pin[0], GPIO.LOW)
				print('Light is on: ', datetime.datetime.now())
			else:
				GPIO.output(light_pin[0], GPIO.HIGH)
				print('Not time for light')
			time.sleep(2)
			now = datetime.datetime.now()

	except KeyboardInterrupt:
		GPIO.cleanup()


light_on()
