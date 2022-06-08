"""Class module for GPS
Author: Erik Stacey
Date: 2022/06/06"""

from BModule import BModule
import serial
import os


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

           :var nsats: number of satellites
           :type nsats: string

           :var ground_speed: groundspeed in km/h
           :type ground_speed: string

           :var quality_flag: see gpgga documentation - indicates gps data quality
           :type quality_flag: string

           :var alt: altitude in meters
           :type alt: string

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
    ser = None
    utc = None
    lat = None
    latd=None
    long = None
    longd = None
    nsats = None
    ground_speed = None
    quality_flag = None
    alt = None



    def activate(self, serial_port = "/dev/serial0"):
        self.name = "CopernicusII-GPS"
        self.ser = serial.Serial(serial_port, 4800, timeout=1)
        self.ser.reset_input_buffer()

        self.filepath = self.basefilepath + self.name + '/'
        self.filename = f"{self.filepath}{self.name}0.csv"
        if not os.path.isdir(self.filepath):
            os.makedirs(self.filepath)
        self._update_filename()

    def update(self):
        # todo: make this read until the buffer is empty
        for i in range(2):  # reads gpgga and gpvtg
            raw_data = self.ser.readline()
            s = self.parse_raw(raw_data)

    def write_to_file(self, time):
        # time is in utc
        # append to the file
        data_to_write = self.lat + "," + self.latd + "," + self.long + "," + self.longd + "," + self.nsats + "," \
                        + self.ground_speed + "," + self.quality_flag + "," + self.alt

        with open(self.filename, "a") as myfile:
            myfile.write(str(time) + "," + data_to_write + "\n")
            self.line_counter +=1

        if self.line_counter >= self.num_lines:
            self._update_filename()
            self.line_counter = 0

    def _update_filename(self):
        while os.path.exists(self.filename):
            self.file_counter +=1
            self.filename = f"{self.filepath}{self.name}{self.file_counter}.csv"

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
        self.utc = s_data[1]
        self.lat = s_data[2]
        self.latd = s_data[3]
        self.long = s_data[4]
        self.longd = s_data[5]
        self.quality_flag = s_data[6]
        self.nsats = s_data[7]
        hdop = s_data[8] # horizontal dilution of precision
        self.alt = s_data[9]
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
        self.ground_speed = s_data[7]
        speed_kmh_indicator = s_data[7]
        mode_indicator = s_data[8]
        checksum = s_data[9]


