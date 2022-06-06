from BModule import BModule
import board
import digitalio
import adafruit_max31865

class TemperatureModule(BModule):
    """Class module for temperature sensor.
    Attributes:
        float ct: current temperature measurement to be updated when update is called by controller

        spi: serial connection
        cs: something associated with serial connection
        sensor: object from which temperature can be read
    Methods:
        void update: retrieves temperature from sensor
        """
    def __init__(self):
        self.name="MAX31865"
        spi = board.SPI()
        cs = digitalio.DigitalInOut(board.D5)
        sensor = adafruit_max31865.MAX31865(spi, cs)

    def update(self):
        ct = self.sensor.temperature