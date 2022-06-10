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
NUM_PLOT_POINTS = 24

# create figure for plotting
fig = plt.figure(figsize=(16,8))
fig.tight_layout()
fig.set(facecolor="black")
plt.subplots_adjust(left=0.08, right=0.8, wspace=0.4, hspace=0.4)
plt.rcParams.update({'text.color': "white", 'axes.labelcolor': "white"})
plt.rcParams["font.family"] = "courier new"
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.suptitle("SKATE Mission Control", fontsize=20)
# matplotlib.spines.Spine.set_color("white")
axCoords    = fig.add_subplot(2, 3, 1)
axAlt       = fig.add_subplot(2, 3, 2)
axHum       = fig.add_subplot(2, 3, 3)
axTempCPU   = fig.add_subplot(2, 3, 4)
axTempI     = fig.add_subplot(2, 3, 5)
axTempE     = fig.add_subplot(2, 3, 6)

# create data and data arrays
dataFull        = []
dataExtract     = []
serialString    = []
Time            = 0     # YYMMDDhhmmss.ss
Latitude        = 0     # DDmm.mmO
Longitude       = 0     # DDDmm.mmO
Altitude        = 0     # aaaaa.aa
NSats           = 0     # nn
GroundSpeed     = 0     # kkk.kk
QualityFlag     = 0     # n
TempInt         = 0     # sttt.tt
TempExt         = 0     # sttt.tt
TempCPU         = 0     # sttt.tt
Humidity        = 0     # hh.hhhhhhhh
xTime       = list(np.zeros(NUM_PLOT_POINTS))
xLong       = list(np.ones(NUM_PLOT_POINTS)*106)
yLat        = list(np.ones(NUM_PLOT_POINTS)*52)
yTempCPU    = list(np.zeros(NUM_PLOT_POINTS))
yTempI      = list(np.zeros(NUM_PLOT_POINTS))
yTempE      = list(np.zeros(NUM_PLOT_POINTS))
yAlt        = list(np.zeros(NUM_PLOT_POINTS))
yHum        = list(np.zeros(NUM_PLOT_POINTS))

# initialize connection with COM port
serialPort = serial.Serial(port="COM47", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
dataFull = serialPort.read_until(b'\nRSSI:')
print('Initial serial read:')
print(dataFull)

# this function is called periodically from FuncAnimation
def animate(i, xTime, xLong, yLat, yTempCPU, yTempI, yTempE, yAlt, yHum):

    # read data from serial port
    dataFull = serialPort.read_until(b'\nRSSI:')
    dataExtract = dataFull[-(NUM_CHARS+TM_END_BYTE_LEN):-TM_END_BYTE_LEN].strip()
    serialString = dataExtract.decode("utf-8").split(",")
    print(serialString)
    try:
        Time        = float(serialString[0][-6:-3])    # YYMMDDhhmmss.ss
    except:
        print("Error: Time")
        Time = 0.0
    try:
        Latitude    = float(serialString[1][:-5])/100  # DDmm.mmO
    except:
        print("Error: Latitude")
        Latitude = 0.0
    try:
        Longitude   = float(serialString[2][:-4])/100  # DDDmm.mmO
    except:
        print("Error: Longitude")
        Longitude = 0.0
    try:
        Altitude    = float(serialString[3][2:4])      # aaaaa.aa
    except:
        print("Error: Altitude")
        Altitude = 0.0
    try:
        NSats       = int(float(serialString[4]))      # nn
    except:
        print("Error: NSats")
        NSats = 0
    try:
        GroundSpeed = float(serialString[5])           # kkk.kk
    except:
        print("Error: Ground Speed")
        GroundSpeed = 0.0
    try:
        QualityFlag = int(float(serialString[6]))      # n
    except:
        print("Error: Quality Flag")
        QualityFlag = 0
    try:
        TempInt     = float(serialString[7])           # sttt.tt
    except:
        print("Error: Temp Int")
        TempInt     = 0.0
    try:
        TempExt     = float(serialString[8])           # sttt.tt
    except:
        print("Error: Temp Ext")
        TempExt     = 0.0
    try:
        TempCPU     = float(serialString[9])           # sttt.tt
    except:
        print("Error: Temp CPU")
        TempCPU     = 0.0
    try:
        Humidity    = float(serialString[10][:6])      # hh.hhhhhhhh
    except:
        print("Error: Humidity")
        Humidity    = 0.0

    # append data arrays
    xTime.append(Time)
    xLong.append(Longitude)
    yLat.append(Latitude)
    yTempCPU.append(TempCPU)
    yTempI.append(TempInt)
    yTempE.append(TempExt)
    yAlt.append(Altitude)
    yHum.append(Humidity)
    xTime       = xTime[-NUM_PLOT_POINTS:]
    xLong       = xLong[-NUM_PLOT_POINTS:]
    xLong[0]    = 106
    yLat        = yLat[-NUM_PLOT_POINTS:]
    yLat[0]     = 52
    yTempCPU    = yTempCPU[-NUM_PLOT_POINTS:]
    yTempI      = yTempI[-NUM_PLOT_POINTS:]
    yTempE      = yTempE[-NUM_PLOT_POINTS:]
    yAlt        = yAlt[-NUM_PLOT_POINTS:]
    yHum        = yHum[-NUM_PLOT_POINTS:]

    # plot data
    axCoords.clear()
    axTempCPU.clear()
    axTempI.clear()
    axTempE.clear()
    axAlt.clear()
    axHum.clear()
    axCoords.scatter(xLong, yLat, color="white")
    axTempCPU.plot(xTime, yTempCPU, color="limegreen")
    axTempI.plot(xTime, yTempI, color="red")
    axTempE.plot(xTime, yTempE, color="dodgerblue")
    axAlt.plot(xTime, yAlt, color="yellow")
    axHum.plot(xTime, yHum, color="orchid")

    # Format plots
    # Coords
    axCoords.set_title("Coordinates", fontweight="bold")
    axCoords.set_xlabel("Longitude [deg]")
    axCoords.set_ylabel("Latitude [deg]")
    axCoords.set_xlim(96, 116)
    axCoords.set_ylim(42, 62)
    # TempCPU
    axTempCPU.set_title("Temperature: CPU", fontweight="bold")
    axTempCPU.set_xlabel("Time [UTC]")
    axTempCPU.set_ylabel("T [deg C]")
    axTempCPU.set_ylim(40,100)
    # Temp I
    axTempI.set_title("Temperature: internal", fontweight="bold")
    axTempI.set_xlabel("Time [UTC]")
    axTempI.set_ylabel("T [deg C]")
    axTempI.set_ylim(0,80)
    # Temp E
    axTempE.set_title("Temperature: external", fontweight="bold")
    axTempE.set_xlabel("Time [UTC]")
    axTempE.set_ylabel("T [deg C]")
    axTempE.set_ylim(0, 80)
    # Alt
    axAlt.set_title("Altitude", fontweight="bold")
    axAlt.set_xlabel("Time [UTC]")
    axAlt.set_ylabel('A [km]')
    axAlt.set_ylim(0, 10)
    # Hum
    axHum.set_title("Humidity", fontweight="bold")
    axHum.set_xlabel("Time [UTC]")
    axHum.set_ylabel("Hum [%]")
    axHum.set_ylim(0, 100)

    # extra formatting
    for ax in [axCoords, axTempCPU, axTempI, axTempE, axAlt, axHum]:
        ax.tick_params(labelrotation=90, colors="white")
        ax.set_facecolor("black")
        ax.grid(True, color="dimgrey")
        plt.setp(ax.spines.values(), color="white")

    textTime    = "Time [UTC]      : " + serialString[0][6:]
    textY       = 0.80
    plt.text(0.82, textY, textTime, fontsize=12, transform=plt.gcf().transFigure)
    plt.text(0.82, textY-.15 , "Coordinates     : " + str(Longitude) + " W", fontsize=12, transform=plt.gcf().transFigure)
    plt.text(0.82, textY-.20 , "                  " + str(Latitude) + " N", fontsize=12, transform=plt.gcf().transFigure)
    plt.text(0.82, textY-.25 , "Altitude [km]   : " + str(Altitude), fontsize=12, transform=plt.gcf().transFigure)
    plt.text(0.82, textY-.30 , "NSats           : " + str(NSats), fontsize=12, transform=plt.gcf().transFigure)
    plt.text(0.82, textY-.35 , "Speed [kph]     : " + str(GroundSpeed), fontsize=12, transform=plt.gcf().transFigure)
    plt.text(0.82, textY-.40 , "Quality         : " + str(QualityFlag), fontsize=12, transform=plt.gcf().transFigure)
    plt.text(0.82, textY-.45 , "TempInt [deg C] : " + str(TempInt), fontsize=12, transform=plt.gcf().transFigure)
    plt.text(0.82, textY-.50 , "TempExt [deg C] : " + str(TempExt), fontsize=12, transform=plt.gcf().transFigure)
    plt.text(0.82, textY-.55 , "TempCPU [deg C] : " + str(TempCPU), fontsize=12, transform=plt.gcf().transFigure)
    plt.text(0.82, textY-.60 , "Humidity [%]    : " + str(Humidity), fontsize=12, transform=plt.gcf().transFigure)

# set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xTime, xLong, yLat, yTempCPU, yTempI, yTempE, yAlt, yHum), interval=1000)
plt.show()
