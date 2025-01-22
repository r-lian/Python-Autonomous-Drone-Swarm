#!/usr/bin/env python3

import asyncio, random, sys, os, getopt
from mavsdk import System
from utilities.drone_helpers import connect_drone, start_manual

async def run():
    try:
        opts, args = getopt.getopt(sys.argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('goto.py -d <serial_device> -b <baud_rate>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('goto.py -d <serial_device> -b <baud_rate>')
            sys.exit(2)
        elif opt == '-c':
            coordinates_file_name = arg

    drone = await connect_drone(opts)

    print("Fetching amsl altitude at home location....")
    async for terrain_info in drone.telemetry.home():
        absolute_altitude = terrain_info.absolute_altitude_m
        break

#    print("-- Taking off")
#    await drone.action.takeoff()
#    await asyncio.sleep(1)

    flying_alt = absolute_altitude + 20.0 #To fly drone 20m above the ground plane
#    goto_location() takes Absolute MSL altitude 
    await drone.action.goto_location(47.399386, 8.535245, flying_alt, 0)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
