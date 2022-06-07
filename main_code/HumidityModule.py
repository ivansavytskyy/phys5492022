"""Class module for humidity/temperature sensor
Author: Cara Remai
Date: 2022/06/06"""

from BModule import BModule
import board
import adafruit_si7021


class HumidityModule(BModule):
    """Class module for humidity sensor.
       Attributes:
           float temp: current temperature measurement to be updated when update is called by controller
           float hum: current humidity measurement to be updated when update is called by controller
           sensor: sensor from which temperature and humidity data can be read
       Methods:
           update(): retrieves humidity and temperature data
                :returns void
           """
    # serial = None

    def __init__(self):
        self.name = "Si7021-Humidity"
        self.active = True
        self.sensor = adafruit_si7021.SI7021(board.I2C())
        self.filename = f'/home/phys5492022/Desktop/instrument_data/' + self.name + '.txt'

    def update(self):
        self.temp = self.sensor.temperature
        self.hum = self.sensor.relative_humidity

    def write_to_file(self, time):
        # time is in utc
        # append to the file
        with open(self.filename, "a") as myfile:
            myfile.write("\n" + str(time) + "\t" + str (self.hum)+ "\t" + str(self.temp))

    def print_diagnostic_data(self):

        print("Current temperature: " + str(self.temp) + " deg C")
        print("Current relative humidity: " + str(self.hum) + "%")
