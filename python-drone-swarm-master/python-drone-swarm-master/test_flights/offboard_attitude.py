#!/usr/bin/env python3

import asyncio, sys, getopt

from mavsdk import System
from mavsdk.offboard import (Attitude, OffboardError)

from utilities.drone_helpers import connect_drone, start_offboard

async def run():

    try:
        opts, args = getopt.getopt(sys.argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('offboard_attitude.py -d <serial_device> -b <baud_rate>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('offboard_attitude.py -d <serial_device> -b <baud_rate>')
            sys.exit(2)
        elif opt == '-c':
            coordinates_file_name = arg

    drone = await connect_drone(opts)
    await start_offboard(drone)

    print("-- Setting initial Attitude")
    await drone.offboard.set_attitude(Attitude(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(2)

    print("-- Go up at 70% thrust")
    await drone.offboard.set_attitude(Attitude(0.0, 0.5, 0.5, 0.7))
    await asyncio.sleep(2)

    print("-- Roll 30 at 60% thrust")
    await drone.offboard.set_attitude(Attitude(30.0, 0.0, 0.0, 0.6))
    await asyncio.sleep(2)

    print("-- Roll -30 at 60% thrust")
    await drone.offboard.set_attitude(Attitude(-30.0, 0.0, 0.0, 0.6))
    await asyncio.sleep(2)

    print("-- Hover at 20% thrust")
    await drone.offboard.set_attitude(Attitude(0.0, 0.0, 0.0, 0.2))
    await asyncio.sleep(2)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: \
              {error._result.result}")

#    await drone.action.land()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
