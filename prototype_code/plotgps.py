import numpy as np
import matplotlib.pyplot as pl

read_data = []
empty_lines = 0

times = []
latitudes = []
longitudes = []

sample_line = "$GPGGA172016.005207.90012N10637.95549W1051.5000525M-020M*5C"

with open("/Users/erikstacey/Documents/GitHub/phys5492022/data/test_gps_data_bowlwalk.txt", "r") as f:
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
                times.append(time)
                latitudes.append(lat)
                longitudes.append(long)
            
        
for i in range(len(latitudes)):
    latdeg = float(latitudes[i][:2])
    latminute = float(latitudes[i][2:])
    latitudes[i] = latdeg + latminute/60

    longdeg = float(longitudes[i][:3])
    longminute = float(longitudes[i][3:])
    longitudes[i] = -(longdeg + longminute / 60)

    timeh = times[i][:2]
    timem = times[i][2:4]
    timesec = times[i][4:6]
    times[i] = f"{timeh}:{timem}:{timesec}"

pl.plot(longitudes, latitudes, linestyle="none", marker='.', markersize=8, color="black")
pl.xlabel("Longitude [deg]")
pl.ticklabel_format(useOffset=False, style='plain')
pl.ylabel("Latitude [deg]")

#pl.show()
pl.savefig("bowlwalk.png")

with open("gpsdata_bowlwalk.csv", "w") as f:
    f.write("Time,Latitude,Longitude\n")
    for i in range(len(latitudes)):
        f.write(f"{times[i]},{latitudes[i]},{longitudes[i]}\n")


