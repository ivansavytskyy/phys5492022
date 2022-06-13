"""
Controller module for RMC 549 Balloon mission.
Author: Erik Stacey
Date:
"""
import time
import os
from BModule import BModule
from TemperatureModule import TemperatureModule
from TemperatureCPU import TemperatureCPUModule
from GPSModule import GPSModule
from HumidityModule import HumidityModule
from CameraModule import CameraModule
from CommunicationsModule import CommunicationsModule
from datetime import datetime
from datetime import timezone

class Controller():
    """Attributes:
        :var modules: dict of classes extending BModule. This will store sensors and objects with behaviour
        (e.g. reading, writing, transmitting)
        :type modules: dict

        :var mod_list: list of modules. This shouldn't be used to access specific modules, use the modules attribute
        instead.
        :type mod_list: list

        :var last_time: stores the time at the end of the previous cycle such that we can ensure steady cycle time.
        format = hhmmss.ss
        :type last_time: string.
        :var current_time: stores the retrieved time from the GPS. format = hhmmss.ss
        :type current_time: string
        :var cycle_time: length in seconds for each controller cycle
        :type cycle_time: float
    Methods:
        run(self): iterates over all the modules to call update and write_to_file. updates the controller time.
            :returns None
        update_time(self): retrieves the UTC from the GPS module. If the GPS module has no reading, it reads system
        time
            :returns None
        get_t_ext(self): retrieves the current temperature measurement from the external sensor
            :returns float if module is active and has measurement, otherwise None
        get_t_int(self): retrieves the current temperature measurement from the internal sensor
            :returns float if module is active and has measurement, otherwise None
        get_t_CPU(self): retrieves the current temperature measurement from the CPU
            :returns float if module is active and has measurement, otherwise None
        get_humidity(self): retrieves the current humidity measurement from the humidity sensor
            :returns float if module is active and has measurement, otherwise None
        get_humidity_temp(self): retrieves the current temperature measurement from the humidity sensor
            :returns float if module is active and has measurement, otherwise None
        get_gps(self): retrieves a package of GPS measurements. Each element of the returned list will be a string,
        however they will be empty strings if the GPS doesn't have a measurement.
            :returns list of strings [lat, latd, long, longd, nsats, ground_speed, quality_flag, alt] if module is
            active, otherwise None
        transmit_data(self): collects position data from the gps, external/internal/cpu temp sensors, humidity sensor
        and the current_time and calls the communications module to format and transmit.
            :returns None"""


    mod_list = []
    modules = {}

    last_time = None
    current_time = None

    cycle_time = 10.0  # second

    debug_mode = True
    
    cycle_counter = 0
    
    

    def run(self):
        # grab the time from the GPS or computer and set it in the controller
        self.update_time()
        
        # run update on all the modules
        if self.debug_mode:
            print(f"\n ===== STARTING ITERATION {self.cycle_counter} =======")

        for module in self.mod_list:
            if module.active:
                try:
                    # every module should have an update function, even if it does nothing otherwise this will yell
                    module.update()
                except:
                    print(f"{module.name} failed update()")
                if self.debug_mode:
                    module.print_diagnostic_data()


        

        # if communication module is still alive, check if we should transmit
        if "Antenna" in self.modules.keys() and self.modules["Antenna"].active:
            if self.modules["Antenna"].is_it_time_to_transmit():
                self.transmit_data()

        # writing it to file
        for module in self.mod_list:
            if module.active:
                try:
                    module.write_to_file(self.current_time)
                except OSError:
                    print("Probably out of disc space - skipping write to file")
        
        time.sleep(self.cycle_time)
        self.cycle_counter += 1

    def __init__(self):

        # try initializing every module - if they fail just ignore it. The rest of the program can function fine without
        # any individual module. If you don't like naked exceptions bite me.
        self.boot_modules()

        print("Modules Status:")
        for module in self.mod_list:
            print(f"{module.name}: {module.active}")

        # create the directory for instrument data
        try:
            if not os.path.isdir(f'/home/phys5492022/Desktop/instrument_data/'):
                os.makedirs(f'/home/phys5492022/Desktop/instrument_data/')
        except OSError:
            print("Probably no disc space, therefore we're skipping saving locally"
    
    def boot_modules(self):
        print("Booting sensors...")
        try:
            self.mod_list.append(TemperatureModule())
            self.mod_list[-1].activate(name="MAX31865-E", board_pin="D5")
            self.modules[self.mod_list[-1].name] = self.mod_list[-1]
            self.mod_list[-1].active = True
        except:
            print("Failed to initialize MAX31865-E")
        try:
            self.mod_list.append(TemperatureModule())
            self.mod_list[-1].activate(name="MAX31865-I", board_pin="D6")
            self.modules[self.mod_list[-1].name] = self.mod_list[-1]
            self.mod_list[-1].active = True
        except:
            print("Failed to initialize MAX31865-I")
        try:
            self.mod_list.append(TemperatureCPUModule())
            self.mod_list[-1].activate()
            self.modules[self.mod_list[-1].name] = self.mod_list[-1]
            self.mod_list[-1].active = True
        except:
            print("Failed to initialize CPUTemp")
        try:
            self.mod_list.append(GPSModule())
            self.mod_list[-1].activate()
            self.modules[self.mod_list[-1].name] = self.mod_list[-1]
            self.mod_list[-1].active = True
        except:
            print("Failed to initialize GPS module")
        try:
            self.mod_list.append(HumidityModule())
            self.mod_list[-1].activate()
            self.modules[self.mod_list[-1].name] = self.mod_list[-1]
            self.mod_list[-1].active = True
        except:
            print("Failed to initialize humidity module")

        try:
            self.mod_list.append(CameraModule())
            self.mod_list[-1].activate()
            self.modules[self.mod_list[-1].name] = self.mod_list[-1]
            self.mod_list[-1].active = True
        except:
            print("Failed to initialize camera module")

        try:
            self.mod_list.append(CommunicationsModule())
            self.mod_list[-1].activate()
            self.modules[self.mod_list[-1].name] = self.mod_list[-1]
            self.mod_list[-1].active = True
        except:
            print("Failed to initialize communications module")

    def update_time(self):
        """this is ugly and hackey but I think it works. It checks to see if the GPS module is active, reads the time,
        and sets it in this module such that it's available for everything else that needs it. If the gps module is
        not available, not active, or gives a weird reading it'll just take the system time."""
        
        self.last_time = self.current_time
        # check if the GPS is active
        gps_active = False
        if "CopernicusII-GPS" in self.modules.keys():
            if self.modules["CopernicusII-GPS"].active:
                gps_active = True

        # gets time and formats it like hhmmss.ss to match gps output
        # gets date from system
        time_object = datetime.now(timezone.utc)
        year = str(time_object.year)[2:]
        month = str(time_object.month)
        if len(month) == 1:
            month = "0" + month
        day = str(time_object.day)


        if len(day) == 1:
            day = "0" + day
        if gps_active:
            try:
                rounded_utc = str(round(float(self.modules["CopernicusII-GPS"].utc), 2))
                split_time = rounded_utc.split(".")
                second = split_time[0][4:6]

                if len(second) == 1:
                    second = "0" + second

                if second == "60":
                    second = "00"
                    minute = str(int(split_time[0][2:4]) + 1)
                else:
                    minute = split_time[0][2:4]

                if len(minute) == 1:
                    minute = "0" + minute

                if minute == "60":
                    minute = "00"
                    hour = str(int(split_time[0][:2]) + 1)
                else:
                    hour = split_time[0][:2]

                if len(hour) == 1:
                    hour = "0" + hour

                if len(split_time[1]) == 1:
                    fracsecond = split_time[1] + "0"
                else:
                    fracsecond = split_time[1]
                self.current_time = f"T{year}{month}{day}{hour}{minute}{second}.{fracsecond}"
            except:
                gps_active = False
        if not gps_active:
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
            self.current_time = f"C{year}{month}{day}{hour}{minute}{second}.{fracsecond}"

    def get_t_ext(self):
        # External temperature
        if "MAX31865-E" in self.modules.keys() and self.modules["MAX31865-E"].active:
            out = self.modules["MAX31865-E"].ct
        else:
            out = None
        return out

    def get_t_int(self):
        # internal temperature
        if "MAX31865-I" in self.modules.keys() and self.modules["MAX31865-I"].active:
            out = self.modules["MAX31865-I"].ct
        else:
            out = None
        return out

    def get_t_CPU(self):
        # CPU temperature
        if "TemperatureCPU" in self.modules.keys() and self.modules["TemperatureCPU"].active:
            out = self.modules["TemperatureCPU"].tempCPU
        else:
            out = None
        return out

    def get_humidity(self):
        if "Si7021-Humidity" in self.modules.keys() and self.modules["Si7021-Humidity"].active:
            out = self.modules["Si7021-Humidity"].hum
        else:
            out = None
        return out
    def get_humidity_sensor_t(self):
        if "Si7021-Humidity" in self.modules.keys() and self.modules["Si7021-Humidity"].active:
            out = self.modules["Si7021-Humidity"].ct
        else:
            out = None
        return out

    def get_gps(self):
        if "CopernicusII-GPS" in self.modules.keys() and self.modules["CopernicusII-GPS"].active:
            return [self.modules["CopernicusII-GPS"].lat,
                    self.modules["CopernicusII-GPS"].latd,
                    self.modules["CopernicusII-GPS"].long,
                    self.modules["CopernicusII-GPS"].longd,
                    self.modules["CopernicusII-GPS"].nsats,
                    self.modules["CopernicusII-GPS"].ground_speed,
                    self.modules["CopernicusII-GPS"].quality_flag,
                    self.modules["CopernicusII-GPS"].alt]
        else:
            return None

    def transmit_data(self):
        if "Antenna" in self.modules.keys() and self.modules["Antenna"].active:
            self.modules["Antenna"].format_and_send_data(gps_package=self.get_gps(),
                                                         utc = self.current_time,
                                                         t_ext = self.get_t_ext(),
                                                         t_int = self.get_t_int(),
                                                         t_cpu = self.get_t_CPU(),
                                                         humidity= self.get_humidity(),
                                                         print_debug = False)
