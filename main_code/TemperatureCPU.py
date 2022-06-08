"""Class module for CPU temperature sensor
Author: Ivan Savytskyy
Date: 2022/06/07"""

from BModule import BModule
import os

class TemperatureCPUModule(BModule):
    """Class module for CPU temperature module.
    Attributes:
        float tempCPU: current temperature measurement to be updated when update is called by controller
    Methods:
        update: retrieves temperature from CPU
            :returns void
    """
    tempCPU = None

    def __init__(self):
        self.name = "TemperatureCPU"
        self.active = True
        self.filepath = f'/home/phys5492022/Desktop/instrument_data/' + self.name
        self.file_counter = 0
        self.line_counter = 0
        self.filename = None
        if not os.path.isdir(self.filepath):
            os.makedirs(self.filepath)
        self._update_filename()
    
    def update(self):
        # The first line in this file holds the CPU temperature as an integer times 1000
        # Read the first line and remove the newline character at the end of the string.
        if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
            with open('/sys/class/thermal/thermal_zone0/temp') as f:
                line = f.readline().strip()
            # Test if the string is an integer as expected.
            if line.isdigit():
                # Convert the string with the CPU temperature to a float in degrees Celsius.
                self.tempCPU = float(line) / 1000

    def write_to_file(self, time):
        # time is in utc
        # while os.path.exists(self.filename):
        #     self.file_counter +=1
        #     self.filename = f"{self.filepath}{self.name}{self.file_counter}.csv"

        # append to the file
        with open(self.filename, "a") as myfile:
            myfile.write("\n" + str(time) + "," + str(self.tempCPU))
            self.line_counter +=1

        if self.line_counter >= 10:
            self._update_filename()

    def _update_filename(self):
        while os.path.exists(self.filename):
            self.file_counter +=1
            self.filename = f"{self.filepath}{self.name}{self.file_counter}.csv"


    def print_diagnostic_data(self):
        print(f"Temperature for {self.name}: {self.tempCPU}")

