"""Class module for humidity/temperature sensor
Author: Cara Remai
Date: 2022/06/06"""

from BModule import BModule
import board
import os
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
    ct = None
    hum = None


    def activate(self):
        self.name = "Si7021-Humidity"
        self.sensor = adafruit_si7021.SI7021(board.I2C())
        self.filepath = self.basefilepath + self.name + '/'
        self.filename = f"{self.filepath}{self.name}0.csv"
        if not os.path.isdir(self.filepath):
            os.makedirs(self.filepath)
        self._update_filename()

    def update(self):
        self.ct = self.sensor.temperature
        self.hum = self.sensor.relative_humidity

    def write_to_file(self, time):
        # time is in utc
        # append to the file
        with open(self.filename, "a") as myfile:
            myfile.write(str(time) + "," + str (self.hum)+ "," + str(self.ct)+ "\n" )
            self.line_counter += 1

        if self.line_counter >= self.num_lines:
            self._update_filename()
            self.line_counter = 0

    def _update_filename(self):
        while os.path.exists(self.filename):
            self.file_counter += 1
            self.filename = f"{self.filepath}{self.name}{self.file_counter}.csv"

    def print_diagnostic_data(self):

        print("Temperature for sensor Si7021-Humidity: " + str(self.ct) + " deg C")
        print("Humidity for sensor Si7021-Humidity: " + str(self.hum) + "%")
