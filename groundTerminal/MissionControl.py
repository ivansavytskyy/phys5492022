"""
Module: Mission Control
Author: Ivan Savytskyy
Date:   2022-06-08

This module processes the serial data received by the ground station
and provides live plotting of relevant variables

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
"""

import serial
import time
import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

NUM_CHARS = 92
TM_END_BYTE = "\nRSSI:"
TM_END_BYTE_LEN = len(TM_END_BYTE)
NUM_PLOT_POINTS = 16

# create figure for plotting
fig = plt.figure(figsize=(16,8))
fig.set(facecolor="black")
plt.rcParams.update({'text.color': "white", 'axes.labelcolor': "white"})
# matplotlib.spines.Spine.set_color("white")
axCoords = fig.add_subplot(2, 2, 1)
axTempCPU = fig.add_subplot(2, 2, 2)
axTempI = fig.add_subplot(2, 2, 3)
axTempE = fig.add_subplot(2, 2, 4)

# create data arrays
xTime       = []
xLong       = []
yLat        = []
yTempCPU    = []
yTempI      = []
yTempE      = []

# initialize connection with COM port
serialPort = serial.Serial(port="COM5", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

# This function is called periodically from FuncAnimation
def animate(i, xTime, xLong, yLat, yTempCPU, yTempI, yTempE):

    # Read data from serial port
    dataFull = serialPort.read_until(b'\nRSSI:')
    dataExtract = dataFull[-(NUM_CHARS+TM_END_BYTE_LEN):-TM_END_BYTE_LEN].strip()
    serialString = dataExtract.decode("utf-8").split(",")
    print(serialString)
    try:
        serTime         = serialString[0]   # YYMMDDhhmmss.ss
        serLatitude     = serialString[1]   # DDmm.mmO
        serLongitude    = serialString[2]   # DDDmm.mmO
        serAltitude     = serialString[3]   # aaaaa.aa
        serNSats        = serialString[4]   # nn
        serGroundSpeed  = serialString[5]   # kkk.kk
        serQualityFlag  = serialString[6]   # n
        serTempInt      = serialString[7]   # sttt.tt
        serTempExt      = serialString[8]   # sttt.tt
        serTempCPU      = serialString[9]   # sttt.tt
        serHumidity     = serialString[10]  # hh.hhhhhhhh
    except IndexError:
        print("Telemetry buffer error")

    try:
        # process data  
        Time        = float(serTime[-6:-3])
        Latitude    = float(serLatitude[:-4])/100
        Longitude   = float(serLongitude[:-4])/100
        # Altitude    = serialString[3]   # aaaaa.aa
        # NSats       = serialString[4]   # nn
        # GroundSpeed = serialString[6]   # kkk.kk
        # QualityFlag = serialString[7]   # n
        TempInt     = float(serTempInt)
        TempExt     = float(serTempExt)
        TempCPU     = float(serTempCPU)
        # Humidity    = serialString[11]  # hh.hhhhhhhh
    except:
        print("Could not process data")

    # Add x and y to lists
    xTime.append(Time)
    xTime = xTime[-NUM_PLOT_POINTS:]
    xLong.append(Longitude)
    xLong = xLong[-NUM_PLOT_POINTS:]
    yLat.append(Latitude)
    yLat = yLat[-NUM_PLOT_POINTS:]
    yTempCPU.append(TempCPU)
    yTempCPU = yTempCPU[-NUM_PLOT_POINTS:]
    yTempI.append(TempInt)
    yTempI = yTempI[-NUM_PLOT_POINTS:]
    yTempE.append(TempExt)
    yTempE = yTempE[-NUM_PLOT_POINTS:]

    # Draw x and y lists
    axCoords.clear()
    axTempCPU.clear()
    axTempI.clear()
    axTempE.clear()
    axCoords.scatter(xLong, yLat)
    axTempCPU.plot(xTime, yTempCPU)
    axTempI.plot(xTime, yTempI)
    axTempE.plot(xTime, yTempE)

    # Format plots
    # Coords
    axCoords.set_title('Coordinates')
    axCoords.set_ylabel('Latitude [deg]')
    axCoords.set_ylabel('Longitude [deg]')
    # TempCPU
    axTempCPU.set_title('Temperature: CPU')
    axTempCPU.set_ylabel('T [deg C]')
    axTempCPU.set_ylim(10,80)
    # Temp I
    axTempI.set_title('Temperature: internal')
    axTempI.set_ylabel('T [deg C]')
    axTempI.set_ylim(0,100)
    # Temp E
    axTempE.set_title('Temperature: external')
    axTempE.set_ylabel('T [deg C]')
    axTempE.set_ylim(0,100)

    for ax in [axCoords, axTempCPU, axTempI, axTempE]:
        ax.tick_params(labelrotation=90, colors="white")
        ax.set_facecolor("black")
        ax.grid(True, color="grey")
        plt.setp(ax.spines.values(), color="white")

    time.sleep(.6)

# set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xTime, xLong, yLat, yTempCPU, yTempI, yTempE), interval=400)
plt.show()
