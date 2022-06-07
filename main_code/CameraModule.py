"""Class module for PiCamera
Author: Cara Remai
Date: 2022/06/07"""

from BModule import BModule
from picamera import PiCamera
from Threading import Thread, Lock
import os

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
        self.num_dirs = 0
        self.lock = Lock()
        self.recent_photo = None

        self.active = False
        time.sleep(2) # delay to let camera warm up the first time

    def update(self):
        # start the thread to take a picture
        Thread(target=self._update_helper())
        # save_str = self.save_path + str(self.num_pics) + '.jpg'
        #
        # self.sensor.start_preview()
        # self.sensor.capture(save_str)
        # self.sensor.stop_preview()
        # self.num_pics += 1

    def _update_helper(self):
        self.lock.acquire()

        # check if directory exists yet
        if not os.path.exists(self.save_path + str (self.num_dirs)):
            os.makedirs(self.save_path + str (self.num_dirs))

        save_str = self.save_path + str (self.num_dirs) + '/image_' + str (self.num_dirs) + '_' + str(self.num_pics) + '.jpg'
        self.sensor.capture(save_str)
        self.recent_photo  = save_str
        self.num_pics += 1

        # check conditions
        if self.num_pics == 99:
            # need a new folder
            self.num_pics = 0
            self.num_dirs +=1

        self.lock.release()
        # new thread can now run to take picture

    def print_diagnostic_data(self):
        val = os.path.isfile(self.recent_photo)
        if val:
            print(self.recent_photo + " saved!")
        else:
            print(self.recent_photo + " didn't save")
