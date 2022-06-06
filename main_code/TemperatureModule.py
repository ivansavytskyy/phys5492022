"""Class module for temperature sensor
Author: Erik Stacey
Date: 2022/06/06"""

from BModule import BModule
import board
import digitalio
import adafruit_max31865

class TemperatureModule(BModule):
    """Class module for temperature sensor.
    Attributes:
        float ct: current temperature measurement to be updated when update is called by controller

        spi: serial connection
        cs: something associated with serial connection
        sensor: object from which temperature can be read
    Methods:
        update: retrieves temperature from sensor
            :returns void
        """
    ct = None
    spi = None
    cs = None
    sensor = None
    def __init__(self):
        self.name="MAX31865"
        self.spi = board.SPI()
        self.cs = digitalio.DigitalInOut(board.D5)
        self.sensor = adafruit_max31865.MAX31865(self.spi, self.cs)

    def update(self):
        self.ct = self.sensor.temperature

    def print_diagnostic_data(self):
        print(self.ct)