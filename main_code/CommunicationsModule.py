from BModule import BModule
import serial
from datetime import datetime, timezone


def force_format_float(f, n1, n2):
    """
    Formats a float f with a fixed n1 and n2 places on the lhs/rhs of the decimal point respectively. Yields a string.
    Args:
        f: float to be formatted
        n1: number of digits on lhs of decimal point
        n2: number of digits on rhs of decimal point

    Returns:
        string containing formatted number, with a leading +/-
    """
    prefix = "+"
    if f < 0:
        rfstr = str(round(f, n2)).replace("-", "")
        prefix = "-"
    else:
        rfstr = str(round(f, n2)).replace("-", "")

    if "." not in rfstr:
        rfstr = rfstr + "."

    splitnum = rfstr.split(".")
    len_lhs = len(splitnum[0])
    if len(splitnum) == 1:
        len_rhs = 0
    else:
        len_rhs = len(splitnum[1])
    if n1 < len_lhs:
        return "F" * (n1 + n2 + 1)
    else:
        return prefix + "0" * (n1 - len_lhs) + rfstr + "0" * (n2 - len_rhs)

class CommunicationsModule(BModule):
    """Class module for communications.
    Attributes:
        :var serial: serial connection
        :type serial: Serial
    Methods:
        update(self): nothing
            :returns None
        send(self, data):
        format_and_send_data: see documentation below
            :returns None
        is_it_time_to_transmit(self): decides if it's time to transmit
            :returns bool
        """

    communication_interval = 5  # controller cycles
    communication_interval_counter = 0

    def activate(self, serial_port = "/dev/ttyACM0"):
        self.name="Antenna"
        self.ser = serial.Serial(serial_port, 9600, timeout=1)

    def update(self):
        self.communication_interval_counter += 1

    def send(self, data):
        self.ser.write(data.encode("utf-8"))
        line = self.ser.readline().decode("utf-8").rstrip()
        print(f"Received from feather: {line}")

    def format_and_send_data(self, t_ext=None, t_int=None, humidity=None, humidity_temp=None,
                             gps_package=None, utc=None, t_cpu=None, print_debug=False):
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
            all gps package information in strings. They will be empty if there is no data.

        Format information
        [time],[lat],[long],[altitude],[nsats],[groundspeed],[quality_flag],[itemp],[etemp],[cputemp],[humidity]\n
        time (15): YYMMDDhhmmss.ss
            min/max: 000101000000.00 / 991231235959.99 - 00:00:00.00 Jan 1, 2000 / 23:59:59.99 Dec 31, 2099
            YY = Year, MM = month, DD = day, hh = hour, mm = minute, ss.ss = seconds
        lat (8): DDmm.mmO
            min/max: 0000.00N / 9000.00N
            DD = degrees, mm.mm = minutes of arc, O = orientation N/S
        long (9): DDDmm.mmO
            min/max: 00000.00E / 18000.00E
            DDD = degrees, mm.mm = minutes of arc, O = orientation E/W
        altitude (8): aaaaa.aa
            min/max: 00000.00 / 99999.99
        nsats (2): nn
            min/max 00 / 99
        groundspeed (6): kkk.kk
            min/max 000.00 / 999.99
        quality_flag (1): n
            refer to documentation for allowable values, these won't be enforced here
        itemp (7): sttt.tt
            min/max -999.99 / 999.99
            s = sign, ttt.tt = temp
        etemp (7): sttt.tt
            min/max -999.99 / 999.99
            s = sign, ttt.tt = temp
        cputemp (7): sttt.tt
            min/max -999.99 / 999.99
            s = sign, ttt.tt = temp
        humidity (11): hh.hhhhhhhh
            min/max 00.00000000 / 99.99999999

        Delimiters: 10
        newline:1
        Total characters: 92

        Non-numeric characters:
        E/W/N/S - directions for coordinates
        X - data missing
        G - data over upper bound
        L - data under lower bound
        F - float formatting error
        """

        # format time - get date from computer and time from satellite
        if utc is not None and type(utc) == str:
            cdt = datetime.now(timezone.utc)
            cyear = str(cdt.year)[-2:]
            out_datetime = f"{cyear}{cdt.month:02}{cdt.day:02}" + utc
        else:
            out_datetime = "XXXXXXXXXXXX.XX"
        if print_debug:
            print("Datetime format test:", out_datetime)

        # format coordinates
        if gps_package is not None and type(gps_package) == list:
            # latitude
            if gps_package[0] not in ["", None]:
                # todo: fix formatting here such that if it rounds up at
                #  50 deg 59.999 minutes it doesn't report 50 deg 60 minutes
                out_lat = str(round(float(gps_package[0]), 2)) + gps_package[1]
            else:
                out_lat = "XXXXX.XX"
            # longitude
            if gps_package[2] not in ["", None]:
                out_long = str(round(float(gps_package[2]), 2)) + gps_package[3]
            else:
                out_long = "XXXXXX.XX"
            # Altitude
            if gps_package[7] not in ["", None]:
                f_alt = round(float(gps_package[7]), 2)
                # check bounds
                if f_alt > 99999.99:
                    out_alt = "GGGGG.GG"
                elif f_alt < 0:
                    out_alt = "LLLLL.LL"
                else:
                    out_alt = force_format_float(f_alt, 5, 2)[1:]
            else:
                out_alt = "XXXXX.XX"
            # nsats
            if gps_package[4] not in ["", None]:
                out_nsats = gps_package[4]
            else:
                out_nsats = "XX"
            # ground speed
            if gps_package[5] not in ["", None]:
                f_gs = round(float(gps_package[5]), 2)
                # check bounds
                if f_gs > 999.99:
                    out_gs = "GGG.GG"
                elif f_gs < 0:
                    out_gs = "LLL.LL"
                else:
                    out_gs = force_format_float(f_gs, 3, 2)[1:]
            else:
                out_gs = "XXX.XX"
            # quality flag
            if gps_package[6] not in ["", None]:
                out_qf = gps_package[6]
            else:
                out_qf = "X"
        else:
            out_lat = "XXXXX.XX"
            out_long = "XXXXXX.XX"
            out_alt = "XXXXX.XX"
            out_nsats = "XX"
            out_gs = "XXX.XX"
            out_qf = "X"
        if print_debug:
            print(
                f"out_lat = {out_lat}, out_long = {out_long}, out_alt = {out_alt}, out_nsats = {out_nsats}, out_gs = {out_gs}, out_qf = {out_qf}")

        #  internal temperature
        if t_int is not None and type(t_int) == float:
            r_t_int = round(t_int, 2)
            if r_t_int > 999.99:
                out_t_int = "+GGG.GG"
            elif r_t_int < -999.99:
                out_t_int = "-LLL.LL"
            elif r_t_int < 0:
                out_t_int = force_format_float(r_t_int, 3, 2)
            else:
                out_t_int = force_format_float(r_t_int, 3, 2)
        else:
            out_t_int = "+XXX.XX"

        if print_debug:
            print(f"Formatted int temperature is: {out_t_int}")

        # external temperature
        if t_ext is not None and type(t_ext) == float:
            r_t_ext = round(t_ext, 2)
            if r_t_ext > 999.99:
                out_t_ext = "+GGG.GG"
            elif r_t_ext < -999.99:
                out_t_ext = "-LLL.LL"
            elif r_t_ext < 0:
                out_t_ext = force_format_float(r_t_ext, 3, 2)
            else:
                out_t_ext = force_format_float(r_t_ext, 3, 2)
        else:
            out_t_ext = "+XXX.XX"

        if print_debug:
            print(f"Formatted ext temperature is: {out_t_ext}")

        # cpu temperature
        if t_cpu is not None and type(t_cpu) == float:
            r_t_cpu = round(t_cpu, 2)
            if r_t_cpu > 999.99:
                out_t_cpu = "+GGG.GG"
            elif r_t_cpu < -999.99:
                out_t_cpu = "-LLL.LL"
            else:
                out_t_cpu = force_format_float(r_t_cpu, 3, 2)
        else:
            out_t_cpu = "+XXX.XX"

        if print_debug:
            print(f"Formatted cpu temperature is: {out_t_cpu}")

        if humidity is not None and type(humidity) == float:
            r_humidity = round(humidity, 8)
            if r_humidity > 99.99999999:
                out_humidity = "GG.GGGGGGGG"
            elif r_humidity < 0:
                out_humidity = "LL.LLLLLLLL"
            else:
                out_humidity = force_format_float(r_humidity, 2, 8)[1:]
        else:
            out_humidity = "XX.XXXXXXXX"

        if print_debug:
            print(f"Formatted humidity is: {out_humidity}")

            # [time][lat][long][altitude][nsats][groundspeed][quality_flag][itemp][etemp][cputemp][humidity]\n
            print("Lengths:")
            print(
                f"time: {len(out_datetime) == 15}, lat: {len(out_lat) == 8}, long: {len(out_long) == 9}, alt: {len(out_alt) == 8},"
                f"nsats: {len(out_nsats) == 2}, gs: {len(out_gs) == 6}, qf: {len(out_qf) == 1}, t_i: {len(out_t_int) == 7},"
                f"t_e: {len(out_t_ext) == 7}, t_cpu: {len(out_t_cpu) == 7}, humidity: {len(out_humidity) == 11}")

        string_to_send = \
            f"{out_datetime},{out_lat},{out_long},{out_alt}," \
            f"{out_nsats},{out_gs},{out_qf},{out_t_int},{out_t_ext},{out_t_cpu},{out_humidity}\n"

        if print_debug:
            print("String to send:", string_to_send)
            print("String length:", len(string_to_send))

        self.send(string_to_send)

    def is_it_time_to_transmit(self):
        if self.communication_interval_counter >= self.communication_interval:
            self.communication_interval_counter = 0
            return True
        else:
            return False

if __name__ == "__main__":
    import time
    test_mod = CommunicationsModule()
    while True:
        print("Trying to send message...")
        test_mod.send("11.22\n")
        time.sleep(1)
