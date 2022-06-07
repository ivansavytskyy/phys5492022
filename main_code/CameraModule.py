"""Class module for PiCamera
Author: Cara Remai
Date: 2022/06/07"""

from BModule import BModule
from picamera import PiCamera

class CameraModule(BModule):
    """Class module for PiCamera.
    Attributes:
        sensor: object from which pictures can be taken
    Methods:
        update: takes a picture from PiCamera
            :returns void
        """
    sensor = None

    def __init__(self):
        self.name="PiCamera"
        self.sensor = PiCamera()
        self.save_path = f'/home/phys5492022/Desktop/test_images'
        self.num_pics = 0

        self.active = True

    def update(self):
        # taking a picture of it
        save_str = self.save_path + str(self.num_pics) + '.jpg'

        self.sensor.start_preview()
        self.sensor.capture(save_str)
        self.sensor.stop_preview()
        self.num_pics += 1

    def print_diagnostic_data(self):
        print("Hope the camera is working")
