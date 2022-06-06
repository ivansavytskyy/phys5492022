"""A template module for the modular systems integrated with the controller. The empty functions
should be included in the modules when relevant and their individual documentation will indicate
when and why they are called.
Author: Erik Stacey
Date:
"""

class TModule():
    name = "UndefinedModule"

    def update(self):
        """Called every n seconds for all modules in the controller module. The update rate is
        set in the controller module."""
        print(f"Undefined update called on {self.name}")
        pass