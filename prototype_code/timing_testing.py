from datetime import datetime, timezone
import time
import numpy as np


class GPSModule():
    utc = "135932.99903394995"

test_gps_module = GPSModule()

def update_time():
    # if the gps is active and has a time measurement, read it
    # otherwise use system time

    # gets time and formats it like hhmmss.ss to match gps output
    # gets date from system
    time_object = datetime.now(timezone.utc)
    year = str(time_object.year)[2:]
    month = str(time_object.month)
    if len(month) == 1:
        month = "0"+month

    day = str(time_object.day)
    if len(day) == 1:
        day = "0" + day
    try:
        rounded_utc = str(round(float(test_gps_module.utc), 2))
        split_time =  rounded_utc.split(".")
        second = split_time[0][4:6]

        if len(second) == 1:
            second = "0" + second

        if second == "60":
            second = "00"
            minute = str(int(split_time[0][2:4])+1)
        else:
            minute = split_time[0][2:4]

        if len(minute) == 1:
            minute = "0" + minute

        if minute == "60":
            minute = "00"
            hour = str(int(split_time[0][:2])+1)
        else:
            hour = split_time[0][:2]

        if len(hour) == 1:
            hour = "0" + hour

        if len(split_time[1]) == 1:
            fracsecond = split_time[1] + "0"
        else:
            fracsecond = split_time[1]
        return f"{year}{month}{day}{hour}{minute}{second}.{fracsecond}"
    except:
        split_fracsecond = str(round(time_object.microsecond / 1e6, 2)).split(".")
        fracsecond = split_fracsecond[1]
        if len(fracsecond) == 1:
            fracsecond = fracsecond + "0"
        if split_fracsecond[0] == "1":
            second = str(time_object.second + 1)
        else:
            second = str(time_object.second)
        if len(second) == 1:
            second = "0" + second

        if second == "60":
            second = "00"
            minute = str(time_object.minute + 1)
        else:
            minute = str(time_object.minute)
        if len(minute) == 1:
            minute = "0" + minute

        if minute == "60":
            minute = "00"
            hour = str(time_object.hour + 1)
        else:
            hour = str(time_object.hour)
        if len(hour) == 1:
            hour = "0" + hour
        return f"{year}{month}{day}{hour}{minute}{second}.{fracsecond}"
if __name__ == "__main__":
    while True:
        print(update_time())
        time.sleep(0.05)
        # = np.random.uniform()
        #print(f"sleeping for {sleeptime}")
        #time.sleep(sleeptime)