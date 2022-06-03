import time
import board
import digitalio
import adafruit_max31865
import serial

ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
ser.reset_input_buffer()

spi = board.SPI()
cs = digitalio.DigitalInOut(board.D5)
sensor = adafruit_max31865.MAX31865(spi, cs)

while True:
    temp = sensor.temperature
    print(temp)
    ser.write(f"{temp:2.2f}\n".encode("utf-8"))
    line = ser.readline().decode("utf-8").rstrip()
    print(f"Received from feather: {line}")
    time.sleep(1)