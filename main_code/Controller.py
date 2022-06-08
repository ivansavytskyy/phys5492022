"""
Controller module for RMC 549 Balloon mission.
Author: Erik Stacey
Date:
"""
import time
import os
from BModule import BModule
from TemperatureModule import TemperatureModule
from TemperatureCPU import TemperatureCPUModule
from GPSModule import GPSModule
from HumidityModule import HumidityModule
from CameraModule import CameraModule
from CommunicationsModule import CommunicationsModule
from datetime import datetime
from datetime import timezone

class Controller():
    """Attributes:
        :var modules: dict of classes extending BModule. This will store sensors and objects with behaviour
        (e.g. reading, writing, transmitting)
        :type modules: dict

        :var mod_name_map: a dictionary with keys named as the module names mapped to integers of their index in modules
        :type mod_name_map: dict

        :var last_time: stores the time at the end of the previous cycle such that we can ensure steady cycle time.
        format = hhmmss.ss
        :type last_time: string.
        :var current_time: stores the retrieved time from the GPS. format = hhmmss.ss
        :type current_time: string
        :var cycle_time: length in seconds for each refresh cycle
        :type cycle_time: float"""

    mod_list = []
    modules = {}

    last_time = None
    current_time = None

    cycle_time = 1.0  # second

    def run(self):
        for module in self.mod_list:
            if module.active:
                module.update()
                module.print_diagnostic_data()

        self.update_time()

        # writing it to file
        for module in self.mod_list:
            module.write_to_file(self.current_time)

        print(self.modules["MAX31865-E"].ct)

        # if cycle length is longer than 60 seconds this breaks
        if self.current_time is not None and self.last_time is not None:
            last_cycle_delay_true = float(self.current_time[-5:]) - float(self.last_time[-5:])
        else:
            last_cycle_delay_true = 0
        last_cycle_delay_true = 0
        time.sleep(self.cycle_time * (1-last_cycle_delay_true))

    def __init__(self):

        self.mod_list.append(TemperatureModule(name="MAX31865-E", board_pin = "D5"))
        self.mod_list.append(TemperatureModule(name="MAX31865-I", board_pin="D6"))
        self.mod_list.append(TemperatureCPUModule())
        self.mod_list.append(GPSModule())
        # self.mod_list.append(CameraModule())
        # self.mod_list.append(CommunicationsModule())
        self.mod_list.append(HumidityModule())

        for module in self.mod_list:
            self.modules[module.name] = module

        # create the directory for instrument data
        if not os.path.isdir(f'/home/phys5492022/Desktop/instrument_data/'):
            os.makedirs(f'/home/phys5492022/Desktop/instrument_data/')

    def update_time(self):
        # if the gps is active and has a time measurement, read it
        # otherwise use system time
        if self.modules["CopernicusII-GPS"].active == True and self.modules["CopernicusII-GPS"].utc not in [None, ""]:
            self.last_time = self.current_time
            self.current_time == self.modules["CopernicusII-GPS"].utc
            print(f"Updated current time to {self.current_time}")
        else:
            # gets time and formats it like hhmmss.ss to match gps output
            time_object = datetime.now(timezone.utc)
            self.last_time = self.current_time
            base_time = f"{time_object.hour:02}{time_object.minute:02}{time_object.second:02}"
            decimal_time = f"{time_object.microsecond/1e6:.2}"
            self.current_time = base_time + decimal_time[-3:]
            print(f"Updated current time to {self.current_time}")

    def get_t_ext(self):
        # External temperature
        if "MAX31865-E" in self.modules.keys() and self.modules["MAX31865-E"].active:
            out = self.modules["MAX31865-E"].ct
        else:
            out = None
        return out

    def get_t_int(self):
        # internal temperature
        if "MAX31865-I" in self.modules.keys() and self.modules["MAX31865-I"].active:
            out = self.modules["MAX31865-I"].ct
        else:
            out = None
        return out

    def get_t_CPU(self):
        # CPU temperature
        if "TemperatureCPU" in self.modules.keys() and self.modules["TemperatureCPU"].active:
            out = self.modules["TemperatureCPU"].tempCPU
        else:
            out = None
        return out

    def get_humidity(self):
        if "Si7021-Humidity" in self.modules.keys() and self.modules["Si7021-Humidity"].active:
            out = self.modules["Si7021-Humidity"].ct
        else:
            out = None
        return out

    def get_gps(self):
        if "CopernicusII-GPS" in self.modules.keys() and self.modules["CopernicusII-GPS"].active:
            out = [self.modules["CopernicusII-GPS"].lat,
            self.modules["CopernicusII-GPS"].latd,
            self.modules["CopernicusII-GPS"].long,
            self.modules["CopernicusII-GPS"].longd,
            self.modules["CopernicusII-GPS"].nsats,
            self.modules["CopernicusII-GPS"].ground_speed,
            self.modules["CopernicusII-GPS"].quality_flag,
            self.modules["CopernicusII-GPS"].alt]

