#!/usr/bin/env python3

import asyncio
from mavsdk import System

from mavsdk.offboard import (OffboardError, VelocityNedYaw, Attitude)

from utilities.drone_helpers import connect_drone, start_offboard

async def run():

    try:
        opts, args = getopt.getopt(sys.argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('takoff_and_land.py -d <serial_device> -b <baud_rate>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('takeoff_and_land.py -d <serial_device> -b <baud_rate>')
            sys.exit(2)
        elif opt == '-c':
            coordinates_file_name = arg

    drone = await connect_drone(opts)
    # await start_manual(drone)


    print("-- Taking off")
    await drone.action.takeoff()

    await asyncio.sleep(5)

    print("-- Landing")
    await drone.action.land()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
