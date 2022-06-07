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

class Controller():
    """Attributes:
    :var modules: list of classes extending TModule. This will store sensors and objects with behaviour
    (e.g. reading, writing, transmitting)
    :type modules: list

    :var mod_name_map: a dictionary with keys named as the module names mapped to integers of their index in modules
    :type mod_name_map: dict"""

    modules = []
    mod_name_map = {}

    def run(self):
        for module in self.modules:
            module.update()
            module.print_diagnostic_data()

        print(self.modules[self.mod_name_map["CopernicusII-GPS"]].utc)

        time.sleep(1)

    def __init__(self):
        self.modules.append(TemperatureModule(name="MAX31865-E", board_pin = "D5"))
        self.modules.append(GPSModule())
        self.modules.append(HumidityModule())
        self.modules.append(CameraModule())

        for i in range(len(self.modules)):
            self.mod_name_map[self.modules[i].name] = i