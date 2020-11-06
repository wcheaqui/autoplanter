
import water
import datetime


if __name__ == "__main__":
	newline = datetime.datetime.now().strftime('%b %d %Y at %H:%M:%S %p')
	print(newline)
	with open('last_watered.txt', 'a') as f:
		f.write('\n')
		f.write(newline)
	water.auto_water()

