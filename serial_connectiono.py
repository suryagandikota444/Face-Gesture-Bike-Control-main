import serial
import time
arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1)

def write_read(x):
    arduino.write(bytes(str(x), 'utf-8'))
    time.sleep(1)
    data = arduino.readline()
    return data

while True:
    num = 1
    value = write_read(num)
    print(value)