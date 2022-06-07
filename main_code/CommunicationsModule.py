from BModule import BModule
import serial
from datetime import datetime, timezone

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

    def format_and_send_data(self, t_ext = None, t_int = None, humidity = None, humidity_temp = None,
                             gps_package = None, utc=None):
        """
        Args:
            t_ext: float
            t_int: float
            humidity: float
            humidity_temp: float
            utc: "hhmmss.ss"
            gps_package: [lat, latd, long, longd, nsats, groundspeed, qualityflag, alt]
                lat: DDmm.mm
                latd: O
                long: DDDmm.mm
                longd: O
                nsats: nn
                groundspeed: x.x
                qualityflag: n
                alt: x.x


        Format information
        [time][lat][long][altitude][nsats][groundspeed][itemp][etemp][cputemp][humidity]\n
        time (14): YYMMDDhhmmss.ss
            min/max: 000101000000.00 / 991231235959.99 - 00:00:00.00 Jan 1, 2000 / 23:59:59.99 Dec 31, 2099
            YY = Year, MM = month, DD = day, hh = hour, mm = minute, ss.ss = seconds
        lat (7): DDmm.mmO
            min/max: 0000.00N / 9000.00N
            DD = degrees, mm.mm = minutes of arc, O = orientation N/S
        long (8): DDDmm.mmO
            min/max: 00000.00E / 18000.00E
            DDD = degrees, mm.mm = minutes of arc, O = orientation E/W
        altitude (7): aaaaa.aa
            min/max: 00000.00 / 99999.99
        nsats (2): nn
            min/max 00 / 99
        groundspeed (5): kkk.kk
            min/max 000.00 / 999.99
        itemp (6): sttt.tt
            min/max -999.99 / 999.99
            s = sign, ttt.tt = temp
        etemp (6): sttt.tt
            min/max -999.99 / 999.99
            s = sign, ttt.tt = temp
        cputemp (6): sttt.tt
            min/max -999.99 / 999.99
            s = sign, ttt.tt = temp
        humidity (10): hh.hhhhhhhh
            min/max 00.00000000 / 99.99999999
        Total characters: 71
        """

        string_to_send = ""
        # format time - get date from computer and time from satellite
        cdt = datetime.now(timezone.utc)
        cyear = str(cdt.year)[-2:]
        out_datetime = f"{cyear}{cdt.month:02}{cdt.day:02}" + utc.replace(".", "")



if __name__ == "__main__":
    import time
    test_mod = CommunicationsModule()
    while True:
        print("Trying to send message...")
        test_mod.send("11.22\n")
        time.sleep(1)
