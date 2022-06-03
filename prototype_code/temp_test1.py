import time
import board
import digitalio
import adafruit_max31865

spi = board.SPI()
cs = digitalio.DigitalInOut(board.D5)
sensor = adafruit_max31865.MAX31865(spi, cs)

while True:
    temp = sensor.temperature
    print(f"Temperature: {temp:.3f}")
    time.sleep(1.0)