import serial
ser = serial.Serial('/dev/ttyS0', 115200)

while True:
    leerSerial = ser.read_until(b'\n')
    print(leerSerial)
    
