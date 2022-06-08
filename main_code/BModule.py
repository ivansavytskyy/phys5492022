"""A template module for the modular systems integrated with the controller. The empty functions
should be included in the modules when relevant and their individual documentation will indicate
when and why they are called.
Author: Erik Stacey
Date:
"""

class BModule():
    name = "UndefinedModule"
    active = False  # set this to true at the end of init
    basefilepath = f'/home/phys5492022/Desktop/instrument_data/'
    file_counter = 0
    line_counter = 0
    num_lines = 600

    update_failure_counter = 0

    # when the object is created just call the activate function. This means we can re-initialize the object without
    # destroying it (if we want)
    def __init__(self, *params):
        self.activate(self, *params)

    def update(self):
        """Called every n seconds for all modules in the controller module. The update rate is
        set in the controller module."""
        print(f"Undefined update called on {self.name}")
        pass

    def print_diagnostic_data(self):
        pass

    def write_to_file(self, time):
        pass


    def activate(self):
        pass
    def deactivate(self):
        pass