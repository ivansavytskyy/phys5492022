"""
Controller module for RMC 549 Balloon mission.
Author: Erik Stacey
Date:
"""
import time
from TModule import TModule

class Controller():
    """Attributes:
    modules: list of classes extending TModule. This will store sensors and objects with behaviour
    (e.g. reading, writing, transmitting)"""
    modules = []

    def run(self):
        for module in self.modules:
            module.update()

        time.sleep(1)

    def __init__(self):
        testmodule = TModule()
        self.modules.append(testmodule)