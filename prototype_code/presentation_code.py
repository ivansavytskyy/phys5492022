# activate USB port for Feather M0
serFeather = serial.Serial("/dev/ttyACM0", 9600, timeout=1)

# activate SPI protocol for MAX31865
spi = board.SPI()
cs  = digitalio.DigitalInOut(board.D5)

# activate UART protocol for Copernicus II
serGPS = serial.Serial("/dev/serial0", 4800, timeout=1)

# read MAX31865 and GPS outputs
dataMAX    = adafruit_max31865.MAX31865(spi, cs)
temp       = sensor.dataMAX
dataGPSIn  = serGPS.readline()
dataGPSOut = parseGPS(dataGPSIn)

# transmit temperature to Feather
serFeather.write(f"{temp:2.2f}".encode("utf-8"))