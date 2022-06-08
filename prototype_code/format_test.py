from datetime import datetime, timezone

def format_and_send_data(t_ext=None, t_int=None, humidity=None, humidity_temp=None,
                         gps_package=None, utc=None, t_cpu = None, print_debug = False):
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
    [time][lat][long][altitude][nsats][groundspeed][quality_flag][itemp][etemp][cputemp][humidity]\n
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
    quality_flag (1): n
        refer to documentation for allowable values, these won't be enforced here
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
    Total characters: 72

    Non-numeric characters:
    E/W/N/S - directions for coordinates
    X - data missing
    G - data over upper bound
    L - data under lower bound
    F - float formatting error
    """

    # format time - get date from computer and time from satellite
    if utc is not None:
        cdt = datetime.now(timezone.utc)
        cyear = str(cdt.year)[-2:]
        out_datetime = f"{cyear}{cdt.month:02}{cdt.day:02}" + utc.replace(".", "")
    else:
        out_datetime = "XXXXXXXXXXXXXX"
    if print_debug:
        print("Datetime format test:", out_datetime)

    # format coordinates
    if gps_package is not None:
        # latitude
        if gps_package[0] not in ["", None]:
            out_lat = gps_package[0].replace(".", "") + gps_package[1]
        else:
            out_lat = "XXXXXXX"
        # longitude
        if gps_package[2] != "":
            out_long = gps_package[2].replace(".", "") + gps_package[3]
        else:
            out_long = "XXXXXXXX"
        # Altitude
        if gps_package[7] not in ["", None]:
            f_alt = round(float(gps_package[7]), 2)
            # check bounds
            if f_alt > 99999.99:
                out_alt = "GGGGGGG"
            elif f_alt < 0:
                out_alt = "LLLLLLL"
            else:
                out_alt = force_format_float(f_alt, 5, 2)
        else:
            out_alt = "XXXXXXX"
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
                out_gs = "GGGGGGG"
            elif f_gs < 0:
                out_gs = "LLLLLLL"
            else:
                out_gs = force_format_float(f_gs, 3, 2)
        else:
            out_gs = "XXXXX"
        # quality flag
        if gps_package[6] not in ["", None]:
            out_qf = gps_package[6]
        else:
            out_qf = "X"
    else:
        out_lat = "XXXXXXX"
        out_long = "XXXXXXXX"
        out_alt = "XXXXXXX"
        out_nsats = "XX"
        out_gs = "XXXXX"
        out_qf = "X"
    if print_debug:
        print(f"out_lat = {out_lat}, out_long = {out_long}, out_alt = {out_alt}, out_nsats = {out_nsats}, out_gs = {out_gs}, out_qf = {out_qf}")

    #  internal temperature
    if t_int is not None:
        r_t_int = round(t_int, 2)
        if r_t_int > 999.99:
            out_t_int = "+GGGGG"
        elif r_t_int < -999.99:
            out_t_int = "-LLLLL"
        elif r_t_int < 0:
            out_t_int = force_format_float(r_t_int, 3, 2)
        else:
            out_t_int = "+" + force_format_float(r_t_int, 3, 2)
    else:
        out_t_int = "XXXXXX"

    if print_debug:
        print(f"Formatted int temperature is: {out_t_int}")

    # external temperature
    if t_ext is not None:
        r_t_ext = round(t_ext, 2)
        if r_t_ext > 999.99:
            out_t_ext = "+GGGGG"
        elif r_t_ext < -999.99:
            out_t_ext = "-LLLLL"
        elif r_t_ext < 0:
            out_t_ext = force_format_float(r_t_ext, 3, 2)
        else:
            out_t_ext = "+" + force_format_float(r_t_ext, 3, 2)
    else:
        out_t_ext = "XXXXXX"

    if print_debug:
        print(f"Formatted ext temperature is: {out_t_ext}")

    # cpu temperature
    if t_cpu is not None:
        r_t_cpu = round(t_cpu, 2)
        if r_t_cpu > 999.99:
            out_t_cpu = "+GGGGG"
        elif r_t_cpu < -999.99:
            out_t_cpu = "-LLLLL"
        elif r_t_cpu < 0:
            out_t_cpu = force_format_float(r_t_cpu, 3, 2)
        else:
            out_t_cpu = "+" + force_format_float(r_t_cpu, 3, 2)
    else:
        out_t_cpu = "XXXXXX"

    if print_debug:
        print(f"Formatted cpu temperature is: {out_t_cpu}")

    if humidity is not None:
        r_humidity = round(humidity, 8)
        if r_humidity > 99.99999999:
            out_humidity = "+GGGGG"
        elif r_humidity < 0:
            out_humidity = "-LLLLL"
        else:
            out_humidity = force_format_float(r_humidity, 2, 8)
    else:
        out_t_cpu = "XXXXXX"

    if print_debug:
        print(f"Formatted humidity is: {out_humidity}")

        # [time][lat][long][altitude][nsats][groundspeed][quality_flag][itemp][etemp][cputemp][humidity]\n
        print("Lengths:")
        print(f"time: {len(out_datetime)}, lat: {len(out_lat)}, long: {len(out_long)}, alt: {len(out_alt)},"
          f"nsats: {len(out_nsats)}, gs: {len(out_gs)}, qf: {len(out_qf)}, t_i: {len(out_t_int)},"
          f"t_e: {len(out_t_ext)}, t_cpu: {len(out_t_cpu)}, humidity: {len(out_humidity)}")

    string_to_send =\
        f"{out_datetime}{out_lat}{out_long}{out_alt}" \
        f"{out_nsats}{out_gs}{out_qf}{out_t_int}{out_t_ext}{out_t_cpu}{out_humidity}"

    if print_debug:
        print("String to send:", string_to_send)
        print("String length:", len(string_to_send))

def force_format_float(f, n1, n2):
    if n2 ==0:
        return int(round(f,0))
    len_int = len(str(int(f)))
    decimal_component = str(round(f, n2)).split(".")[1]
    n_trailing_zeros = n2 - len(decimal_component)
    if f < 0:  # accounting for negative sign
        len_int -=1
    n_leading_zeros = n1 - len_int

    # handle issues - instead of confusing truncation behavior
    # when n1 < the number of lhs decimal places of f, just output
    if n_leading_zeros < 0:
        return "F" * (n1+n2)

    if not f<0:
        return n_leading_zeros*"0" + f"{int(f)}" + decimal_component + n_trailing_zeros * "0"
    else:
        return "-" + n_leading_zeros*"0" + f"{int(f)}"[1:] + decimal_component + n_trailing_zeros * "0"




print("Force format float test:", force_format_float(-1.0234341, 3, 1))

format_and_send_data(t_ext=-10000, t_int = 123.12, humidity = 30.34,
                     humidity_temp = 25.00000000, t_cpu=100.00, gps_package=[
        "4545.02", "N", "13759.89", "W", "14", "132.2149493020", "7", "4500.133939"
    ], utc = "125925.33")
