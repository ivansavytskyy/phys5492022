"""Class module for temperature sensor
Author: Erik Stacey
Date: 2022/06/06"""

from BModule import BModule
import os
import board
import digitalio
import adafruit_max31865

class TemperatureModule(BModule):
    """Class module for temperature sensor. Set names to MAX31865-E for external and MAX31865-I for internal
    Attributes:
        :var ct: current temperature measurement to be updated when update is called by controller
        :type ct: string

        :var spi: serial connection
        :var cs: something associated with serial connection
        :var sensor: object from which temperature can be read
    Methods:
        update: retrieves temperature from sensor
            :returns void
        """
    ct = None
    spi = None
    cs = None
    sensor = None
    def activate(self, name, board_pin):
        # board pin is D5 or D6
        self.name=name
        self.spi = board.SPI()
        if board_pin == "D5":
            self.cs = digitalio.DigitalInOut(board.D5)
        elif board_pin == "D6":
            self.cs = digitalio.DigitalInOut(board.D6)
        self.sensor = adafruit_max31865.MAX31865(self.spi, self.cs)

        self.filepath = self.basefilepath + self.name + '/'
        self.filename = f"{self.filepath}{self.name}0.csv"
        if not os.path.isdir(self.filepath):
            os.makedirs(self.filepath)
        self._update_filename()

    def update(self):
        self.ct = self.sensor.temperature

    def write_to_file(self, time):
        # time is in utc
        # append to the file
        with open(self.filename, "a") as myfile:
            myfile.write(str(time) + "," + str(self.ct) + "\n")
            self.line_counter += 1

        if self.line_counter >= self.num_lines:
            self._update_filename()
            self.line_counter = 0

    def _update_filename(self):
        while os.path.exists(self.filename):
            self.file_counter +=1
            self.filename = f"{self.filepath}{self.name}{self.file_counter}.csv"

    def print_diagnostic_data(self):
        print(f"Temperature for sensor {self.name}: {self.ct}")