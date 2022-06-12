"""Class module for PiCamera
Author: Cara Remai
Date: 2022/06/07"""

from BModule import BModule
from picamera import PiCamera
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
    recording_counter = None
    video_length = 24  # controller cycles

    def activate(self):
        self.name="PiCamera"
        self.sensor = PiCamera()

        time.sleep(2) # TODO: neeed delay to let camera warm up the first time?
        self.filepath = self.basefilepath + self.name + '/'
        self.filename = f"{self.filepath}{self.name}0.h264"
        if not os.path.isdir(self.filepath):
            os.makedirs(self.filepath)
        self._update_filename()

        self.start_video()
        self.recording_counter = 0

    def update(self):
        self.recording_counter += 1

        if self.recording_counter >= self.video_length:
            self.stop_video()
            self._update_filename()
            self.start_video()
            self.recording_counter=0


    def start_video(self):
        self.sensor.start_recording(self.filename)

    def stop_video(self):
        self.sensor.stop_recording()

    def _update_filename(self):
        while os.path.exists(self.filename):
            self.file_counter +=1
            self.filename = f"{self.filepath}{self.name}{self.file_counter}.h264"

    def print_diagnostic_data(self):
        print(f"Camera has been recording for {self.recording_counter} cycles")
