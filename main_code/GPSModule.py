"""Class module for GPS
Author: Erik Stacey
Date: 2022/06/06"""

from BModule import BModule
import serial


class GPSModule(BModule):
    """Class module for temperature sensor.
       Attributes:
           :var serial: serial connection
           :type serial: Serial

           :var utc: time
           :type utc string

           :var lat: latitude
           :type lat string
           :var latd: latitude direction
           :type latd string

           :var long: longitude
           :type long string
           :var longd: longitude direction
           :type string

       Methods:
            update(self): retrieves and parses gps data
                :returns None
            parse_raw(self, raw_data):
                reads raw GPS data and assigns appropriate attributes
                :param raw_data: is the object from serial.readline() - this is binary and needs to be decoded
                :returns True if data read successful, else False
            read_gpgga(self, s_data):
                reads the split data and assigns the appropriate attributes in this object - requires GPVTG format
                :param s_data: a list of strings split about commas, corresponding to GPGGA formatted GPS data
                :returns  None
            read_gpvtg(self, s_Data):
                reads the split data and assigns the appropriate attributes in this object - requires GPVTG format
                :param s_data: a list of strings split about commas, corresponding to GPVTG formatted GPS data
                :returns None
           """
    serial = None
    utc = None

    def __init__(self):
        self.name = "CopernicusII-GPS"
        self.serial = serial.Serial("/dev/serial0", 4800, timeout=1)
        self.serial.reset_input_buffer()

    def update(self):
        for i in range(2):  # reads gpgga and gpvtg
            raw_data = self.serial.readline()
            s = self.parse_raw(raw_data)

    def parse_raw(self, raw_data):
        # convert from bytecode to utf-8
        try:
            ddata = raw_data.decode('utf-8')
        except UnicodeDecodeError:
            return False

        # GPGGA lines handled here
        if ddata[0:6] == "$GPGGA":
            # print('data is GGA')
            s_data = ddata.split(",")
            if s_data[2] == 'V':
                print("no satellite data available")
                return False
            else:
                try:
                    self.read_gpgga(s_data)
                    return True
                except IndexError:
                    return False


        # GPVTG lines handled here
        if ddata[0:6] == "$GPVTG":
            s_data = ddata.split(",")
            try:
                self.read_gpvtg(s_data)
                return True
            except IndexError:
                return False


    def read_gpgga(self, s_data):
        print(s_data)
        self.utc = s_data[1]
        lat = s_data[2]
        latd = s_data[3]
        long = s_data[4]
        longd = s_data[5]
        quality_flag = s_data[6]
        nsat = s_data[7]
        hdop = s_data[8] # horizontal dilution of precision
        alt = s_data[9]
        alt_units = s_data[10]
        und = s_data[11]  # undulation
        und_units = s_data[12]
        checksum = s_data[13]

    def read_gpvtg(self, s_data):
        # I don't know what most of these things are
        tracktrue = s_data[1]
        trackindicator = s_data[2]
        track_mag = s_data[3]
        track_mag_indicator = s_data[4]
        speed_knots = s_data[5]
        speed_knots_indicator = s_data[6]
        speed_kmh = s_data[7]
        speed_kmh_indicator = s_data[7]
        mode_indicator = s_data[8]
        checksum = s_data[9]


