from BModule import BModule
import serial

class CommunicationsModule(BModule):
    """Class module for communications.
    Attributes:
        :var serial: serial connection
        :type serial: Serial
    Methods:
        update(self): not defined yet
            :returns None"""

    def __init__(self, serial_port = "/dev/ttyACM0"):
        self.serial = serial.Serial(serial_port, 9600, timeout=1)

    def send(self, data):
        self.serial.write(data.encode("utf-8"))