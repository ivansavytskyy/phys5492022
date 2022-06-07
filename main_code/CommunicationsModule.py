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
        self.name="Antenna"
        self.ser = serial.Serial(serial_port, 9600, timeout=1)
        self.active = True

    def send(self, data):
        self.ser.write(data.encode("utf-8"))
        line = self.ser.readline().decode("utf-8").rstrip()
        print(f"Received from feather: {line}")

if __name__ == "__main__":
    import time
    test_mod = CommunicationsModule()
    while True:
        print("Trying to send message...")
        test_mod.send("11.22\n")
        time.sleep(1)
