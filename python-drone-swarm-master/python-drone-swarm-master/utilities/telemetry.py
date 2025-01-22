#!/usr/bin/env python3

import asyncio, sys, os, getopt
from mavsdk import System

from utilities.drone_helpers import connect_drone

async def run():
    try:
        opts, args = getopt.getopt(sys.argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('telemetry.py -d <serial_device> -b <baud_rate>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('telemetry.py -d <serial_device> -b <baud_rate>')
            sys.exit(2)
        elif opt == '-c':
            mission_plan_file_name = arg

    drone = await connect_drone(opts)

    try:
        # Start the tasks
        asyncio.ensure_future(print_battery(drone))
        asyncio.ensure_future(print_gps_info(drone))
        asyncio.ensure_future(print_in_air(drone))
        asyncio.ensure_future(print_position(drone))
        asyncio.ensure_future(print_flight_mode(drone))
        asyncio.ensure_future(print_is_armed(drone))
        asyncio.ensure_future(print_is_in_air(drone))
    except MyError:
        print("error", MyError)

    # await drone.action.kill()

async def print_battery(drone):
    async for battery in drone.telemetry.battery():
        print(f"Battery: {battery.remaining_percent}")


async def print_gps_info(drone):
    async for gps_info in drone.telemetry.gps_info():
        print(f"GPS info: {gps_info}")


async def print_in_air(drone):
    async for in_air in drone.telemetry.in_air():
        print(f"In air: {in_air}")


async def print_position(drone):
    async for position in drone.telemetry.position():
        print(position)

async def print_flight_mode(drone):
    async for flight_mode in drone.telemetry.flight_mode():
        print("FlightMode:", flight_mode)

async def print_is_armed(drone):
    async for is_armed in drone.telemetry.armed():
        print("Is_armed:", is_armed)


async def print_is_in_air(drone):
    async for is_in_air in drone.telemetry.in_air():
        print("Is_in_air:", is_in_air)

if __name__ == "__main__":
    # Start the main function
    asyncio.ensure_future(run())

    # Runs the event loop until the program is canceled with e.g. CTRL-C
    asyncio.get_event_loop().run_forever()
