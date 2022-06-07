"""
Controller module for RMC 549 Balloon mission.
Author: Erik Stacey
Date:
"""
import time
from BModule import BModule
from TemperatureModule import TemperatureModule
from GPSModule import GPSModule
from HumidityModule import HumidityModule
from CameraModule import CameraModule
from CommunicationsModule import CommunicationsModule
from datetime import datetime
from datetime import timezone
class Controller():
    """Attributes:
        :var modules: list of classes extending TModule. This will store sensors and objects with behaviour
        (e.g. reading, writing, transmitting)
        :type modules: list

        :var mod_name_map: a dictionary with keys named as the module names mapped to integers of their index in modules
        :type mod_name_map: dict

        :var last_time: stores the time at the end of the previous cycle such that we can ensure steady cycle time.
        format = hhmmss.ss
        :type last_time: string.
        :var current_time: stores the retrieved time from the GPS. format = hhmmss.ss
        :type current_time: string
        :var cycle_time: length in seconds for each refresh cycle
        :type cycle_time: float"""


    modules = []
    mod_name_map = {}

    last_time = None
    current_time = None

    cycle_time = 1.0  # second



    def run(self):
        for module in self.modules:
            if module.active:
                module.update()
                module.print_diagnostic_data()

        self.update_time()

        # if cycle length is longer than 60 seconds this breaks
        if self.current_time is not None and self.last_time is not None:
            last_cycle_delay_true = float(self.current_time[-5:]) - float(self.last_time[-5:])
        else:
            last_cycle_delay_true = 0

        time.sleep(self.cycle_time * (1-last_cycle_delay_true))

    def __init__(self):
        self.modules.append(TemperatureModule(name="MAX31865-E", board_pin = "D5"))
        self.modules.append(GPSModule())
        self.modules.append(HumidityModule())
        self.modules.append(CameraModule())
        self.modules.append(CommunicationsModule())

        for i in range(len(self.modules)):
            self.mod_name_map[self.modules[i].name] = i
        print("module name map:",self.mod_name_map)

    def update_time(self):
        # if the gps is active and has a time measurement, read it
        # otherwise use system time
        if self.modules[self.mod_name_map["CopernicusII-GPS"]].active == True and self.modules[self.mod_name_map["CopernicusII-GPS"]].utc not in [None, ""]:
            self.last_time = self.current_time
            self.current_time == self.modules[self.mod_name_map["CopernicusII-GPS"]].utc
        else:
            # gets time and formats it like hhmmss.ss to match gps output
            time_object = datetime.now(timezone.utc)
            self.last_time = self.current_time
            base_time = f"{time_object.hour:02}{time_object.minute:02}{time_object.second:02}"
            decimal_time = f"{time_object.microsecond/1e6:.2}"
            self.current_time = base_time + decimal_time[-3:]

