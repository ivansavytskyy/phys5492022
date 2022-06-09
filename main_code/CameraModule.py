"""Class module for PiCamera
Author: Cara Remai
Date: 2022/06/07"""

from BModule import BModule
from picamera import PiCamera
from multiprocessing import Process
import time
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
    video_length = 10 # seconds

    def activate(self):
        self.name="PiCamera"

        self.active = False
        time.sleep(2) # TODO: neeed delay to let camera warm up the first time?
        self.filepath = self.basefilepath + self.name + '/'
        self.filename = f"{self.filepath}{self.name}0.h264"
        if not os.path.isdir(self.filepath):
            os.makedirs(self.filepath)
        self._update_filename()

    def start_video(self):
        # creates process to start camera_video
        p = Process(target=self._camera_video())
        p.start()

    def _camera_video(self):
        # how we want it to run
        self.sensor = PiCamera()
        while True:
            # self.sensor.start_preview()
            # start video, record for video length, then stop
            self.sensor.start_recording(self.filename)
            self.sensor.wait_recording(self.video_length)
            self.sensor.stop_recording()

            # self.sensor.stop_preview()
            # need to update the filename
            self._update_filename()

    def _update_filename(self):
        while os.path.exists(self.filename):
            self.file_counter +=1
            self.filename = f"{self.filepath}{self.name}{self.file_counter}.h264"

    def print_diagnostic_data(self):
        val = os.path.isfile(self.filename)
        if val:
            print(self.filename + " saved!")
        else:
            print(self.filename + " didn't save")
