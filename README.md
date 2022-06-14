# phys5492022

The code repository for the RMC PH549 Summer 2022 edition. This repository contains the prototype and main code used for the on-board computer and ground stations for the SasKatoon Altitude Temperature Experiment (SKATE) high-altitude balloon.

main_code contains the main OBC code. Running main.py (or run.sh) will run the main program, create a Controller object, then add modules corresponding to the two temperature sensors, humidity sensor, GPS receiver, RPi cpu temperature sensor, and the downlink antenna. Inquiries regarding this program can be directed to Erik Stacey.

prototype_code contains several short scripts that were used to individually test the sensors/etc employed in the main program.

groundTerminal contains code for receiving and plotting data on the ground in real time
