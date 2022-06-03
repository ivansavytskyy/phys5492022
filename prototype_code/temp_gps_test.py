import time
import board
import digitalio
import adafruit_max31865
import serial

def parseGPS(data):
#    print "raw:", data #prints raw data
    print(data[0:6])
    try:
        ddata = data.decode('utf-8')
    except UnicodeDecodeError:
        return
    if ddata[0:6] == "$GPGGA":
        #print('data is GGA')
        sdata = ddata.split(",")
        if sdata[2] == 'V':
            print("no satellite data available")
            return
        #print("---Parsing GPGGA---")
        print(sdata)
        return sdata
        
        
def decode(coord):
    #Converts DDDMM.MMMMM > DD deg MM.MMMMM min
    x = coord.split(".")
    head = x[0]
    tail = x[1]
    deg = head[0:-2]
    min = head[-2:]
    return deg + " deg " + min + "." + tail + " min"

spi = board.SPI()
cs = digitalio.DigitalInOut(board.D5)
tempSensor = adafruit_max31865.MAX31865(spi, cs)

print("Receiving GPS data")
ser = serial.Serial("/dev/serial0", 4800, timeout=1)
ser.reset_input_buffer()
#with open("test_gps_data.txt", "w") as f:
    #f.write("Start of file")
while True:
   data = ser.readline()
   #print(data)
   out_data = parseGPS(data)
   temp = tempSensor.temperature
   print(f"Temperature: {temp:.3f}")
   time.sleep(1.0)
   #if out_data is not None:
       #with open("test_gps_data.txt", "a") as f:
           #f.write("\n")
           #for element in out_data:
               #f.write(element)