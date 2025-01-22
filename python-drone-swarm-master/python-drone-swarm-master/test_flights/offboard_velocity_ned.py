#!/usr/bin/env python3


import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, VelocityNedYaw)

from utilities.drone_helpers import connect_drone, start_offboard


async def run():

    try:
        opts, args = getopt.getopt(sys.argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('offboard_velocity_ned.py -d <serial_device> -b <baud_rate>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('offboard_velocity_ned.py -d <serial_device> -b <baud_rate>')
            sys.exit(2)
        elif opt == '-c':
            coordinates_file_name = arg

    drone = await connect_drone(opts)
    await start_offboard(drone)


    print("-- Setting initial setpoint")
    await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: \
                {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    print("-- Arming")
    await drone.action.arm()

    print("-- Go up 2 m/s")
    await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, -2.0, 0.0))
    await asyncio.sleep(4)

    print("-- Go North 2 m/s, turn to face East")
    await drone.offboard.set_velocity_ned(VelocityNedYaw(2.0, 0.0, 0.0, 90.0))
    await asyncio.sleep(4)

    print("-- Go North 4 m/s, turn to face East")
    await drone.offboard.set_velocity_ned(VelocityNedYaw(4.0, 0.0, 0.0, 90.0))
    await asyncio.sleep(4)

    print("-- Go North 6 m/s, turn to face East")
    await drone.offboard.set_velocity_ned(VelocityNedYaw(6.0, 0.0, 0.0, 90.0))
    await asyncio.sleep(4)

    print("-- Go South 2 m/s, turn to face West")
    await drone.offboard.set_velocity_ned(
            VelocityNedYaw(-2.0, 0.0, 0.0, 270.0))
    await asyncio.sleep(4)

    print("-- Go West 2 m/s, turn to face East")
    await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, -2.0, 0.0, 90.0))
    await asyncio.sleep(4)

    print("-- Go East 2 m/s")
    await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 2.0, 0.0, 90.0))
    await asyncio.sleep(4)

    print("-- Turn to face South")
    await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, 180.0))
    await asyncio.sleep(2)

    print("-- Go down 1 m/s, turn to face North")
    await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 1.0, 0.0))
    await asyncio.sleep(4)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: \
                {error._result.result}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
