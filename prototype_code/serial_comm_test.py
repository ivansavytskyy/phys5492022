import serial
import time

ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
ser.reset_input_buffer()

while True:
    ser.write(b"Hello from Raspberry Pi! ")
    ser.write(b"I have sent you two lines.\n")
    line = ser.readline().decode("utf-8").rstrip()
    print(line)
    time.sleep(1)
    break

ser.write()