import RPi.GPIO as GPIO
import datetime
import time


init = False

GPIO.setmode(GPIO.BOARD)


def light_on(light_pin = 8, delay = 18):
	now = datetime.datetime.now()

	GPIO.setup(light_pin, GPIO.OUT)
	GPIO.output(light_pin, GPIO.LOW)

	try:
		while True:
			if ((now.hour >= 6) and (now.hour < 18)):
				GPIO.output(light_pin, GPIO.HIGH)
				GPIO.output(light_pin, GPIO.LOW)
				print('Light is on: ', datetime.datetime.now())
			else:
				GPIO.output(light_pin, GPIO.HIGH)
				print('Not time for light')
			time.sleep(2)
			now = datetime.datetime.now()

	except KeyboardInterrupt:
		GPIO.cleanup()


light_on()
