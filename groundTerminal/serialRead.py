"""
Module: Mission Control
Author: Ivan Savytskyy
Date:   2022-06-08

This module processes the serial data received by the ground station
and provides live plotting of relevant variables
"""

import serial
import time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    # Read temperature (Celsius) from TMP102
    serialString = serialPort.readline()

    # Print the contents of the serial data
    # print(serialString.decode("Ascii"))
    tempCPU = serialString[-4:-2].decode("utf-8")
    print(tempCPU)

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(int(tempCPU))

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('CPU Temperature over Time')
    plt.ylabel('Temperature (deg C)')

serialString = ""  # Used to hold data coming over UART

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

# initialize connection with COM port
serialPort = serial.Serial(port="COM5", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
)

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
plt.show()
