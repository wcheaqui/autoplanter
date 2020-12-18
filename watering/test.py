from nanpy import SerialManager
from nanpy import ArduinoApi


conn = SerialManager(device='/dev/ttyACM0')
print(conn)

a = ArduinoApi(connection=conn)
print('test')

a.analogRead('A0')

print(a)
