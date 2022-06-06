"""Class module for GPS
Author: Erik Stacey
Date: 2022/06/06"""

from BModule import BModule
import serial


class GPSModule(BModule):
    """Class module for temperature sensor.
       Attributes:
           :var serial: serial connection
           :type serial: Serial

           :var lat
           :type lat string
           :var latd
           :type latd string

           :var long
           :type long string
           :var longd
           :type string

       Methods:
           update(): retrieves and parses gps data
                :returns void
           """
    serial = None

    def __init__(self):
        self.name = "CopernicusII-GPS"
        self.serial = serial.Serial("/dev/serial0", 4800, timeout=1)
        self.serial.reset_input_buffer()

    def update(self):
        raw_data = self.serial.readline()