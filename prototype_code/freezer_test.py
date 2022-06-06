# freezer_test
# import libraries
import os
import time
import board
import digitalio
import adafruit_max31865
import serial
from datetime import datetime

# connect to MAX31865
spi = board.SPI()
cs = digitalio.DigitalInOut(board.D5)
sensor = adafruit_max31865.MAX31865(spi, cs)

baseFileStr = "/home/phys5492022/Documents/code/freezer_test_file"
filecounter = 0
fileStr = f"{baseFileStr}{filecounter}.txt"

while os.path.exists(fileStr):
    filecounter += 1
    fileStr=f"{baseFileStr}{filecounter}.txt"
    

# open text file
with open(fileStr, "w") as f:
    f.write("Freezer test file 2022-06-06\nStart of file\n")
    
# Initialize the result
counter = 0
tempCPU = 0.0

while(True):
    # The first line in this file holds the CPU temperature as an integer times 1000.
    # Read the first line and remove the newline character at the end of the string.
    if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            line = f.readline().strip()
        # Test if the string is an integer as expected.
        if line.isdigit():
            # Convert the string with the CPU temperature to a float in degrees Celsius.
            tempCPU = float(line) / 1000
    # Give the result back to the caller.
    print(f'\nTemperature RPi CPU   [deg C]: {tempCPU:2.2f}')
    tempRTD = sensor.temperature
    print(f'Temperature PT100 RTD [deg C]: {tempRTD:2.2f}')
    time.sleep(1)
    
    currentTime = datetime.utcnow().strftime('%Y-%m-%d, %H:%M:%S')
    with open(fileStr, "a") as f:
        
        f.write(f'\n[{currentTime}] Temperature RPi CPU   [deg C]: {tempCPU:2.2f}')
        f.write(f'\n[{currentTime}] Temperature PT100 RTD [deg C]: {tempRTD:2.2f}')
        

