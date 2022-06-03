import numpy as np
import matplotlib.pyplot as pl

read_data = []
empty_lines = 0

times = []
latitudes = []
longitudes = []

sample_line = "$GPGGA172016.005207.90012N10637.95549W1051.5000525M-020M*5C"

with open("test_gps_data_bowlwalk.txt", "r") as f:
    while empty_lines < 10:
        cline = f.readline()
        if cline == "":
            empty_lines+=1
        else:
            empty_lines = 0
            if not (len(cline) < len(sample_line)):
                read_data.append(cline)
                fmt = cline[:5]
                time = cline[6:15]
                lat = cline[15:25]
                latd = cline[25]
                long = cline[26:37]
                longd = cline[37]
                print(time, lat, latd, long, longd)
                times.append(float(time))
                latitudes.append(float(lat))
                longitudes.append(float(long))
            
        
pl.plot(longitudes, latitudes)
pl.show()


