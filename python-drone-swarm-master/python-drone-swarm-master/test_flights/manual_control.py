#!/usr/bin/env python3

import asyncio, random, sys, os, getopt

from utilities.drone_helpers import connect_drone, start_manual

from mavsdk import System

# Test set of manual inputs. Format: [roll, pitch, throttle, yaw]
async def manual_controls():
    try:
        opts, args = getopt.getopt(sys.argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('manual_control.py -d <serial_device> -b <baud_rate>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('manual_control.py -d <serial_device> -b <baud_rate>')
            sys.exit(2)
        elif opt == '-c':
            coordinates_file_name = arg

    drone = await connect_drone(opts)

    # Set the manual control input after arming.
    await start_manual(drone)

    # This is supposed to send joystick commands at higher than 10Hz.
    print('Attempting to set throttle to 0...');
    counter = 1
    while counter != 1000:
        await drone.manual_control.set_manual_control_input(float(0),float(0),float(0),float(0));
        # await asyncio.sleep(0.1)
        counter = counter + 1
        # print(counter)

    print('Attempting to set throttle to half...');
    counter = 1
    while counter != 1000:
        await drone.manual_control.set_manual_control_input(float(.5),float(.5),float(.5),float(.5));
        # await asyncio.sleep(0.1)
        counter = counter + 1
        # print(counter)

    print('Attempting to set throttle to max...');
    counter = 1
    while counter != 1000:
        await drone.manual_control.set_manual_control_input(float(1),float(1),float(1),float(1));
        # await asyncio.sleep(0.1)
        counter = counter + 1
        # print(counter)

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(manual_controls())
