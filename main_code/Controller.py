"""
Controller module for RMC 549 Balloon mission.
Author: Erik Stacey
Date:
"""
import time
from BModule import BModule
from TemperatureModule import TemperatureModule
from HumidityModule import HumidityModule

class Controller():
    """Attributes:
    modules: list of classes extending TModule. This will store sensors and objects with behaviour
    (e.g. reading, writing, transmitting)"""
    modules = []

    def run(self):
        for module in self.modules:
            module.update()
            module.print_diagnostic_data()

        time.sleep(1)

    def __init__(self):
        self.modules.append(HumidityModule())