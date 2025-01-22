#!/usr/bin/env python3

import asyncio, sys, os, getopt

from utilities.drone_helpers import connect_drone, start_offboard, stop_offboard
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)

async def run():

    coordinates_file_name = os.path.dirname(__file__) + "/offboard_plan.txt"

    try:
        opts, args = getopt.getopt(sys.argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('offboard_directions.py -d <serial_device> -b <baud_rate> -c <offboard_directions_text_file>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('offboard_directions.py -d <serial_device> -b <baud_rate> -c <offboard_directions_text_file>')
            sys.exit(2)
        elif opt == '-c':
            coordinates_file_name = arg

    drone = await connect_drone(opts)
    await start_offboard(drone)

    try:
        coordinates_file = open(coordinates_file_name , "r")
    except FileOpenError as error:
        print(f"Could not open file!")
        return

    line_number = 0

    coordinate_string_array = coordinates_file.readline()[:-1].split('|')
    # while True:
    while len(coordinate_string_array) == 4:
        print("-- Setting Coordinate " + str(line_number))
        coordinate_float_list = [ float(coordinate) for coordinate in coordinate_string_array ]
        print(coordinate_float_list)
        
        await drone.offboard.set_position_ned(PositionNedYaw(coordinate_float_list[0], coordinate_float_list[1], coordinate_float_list[2], coordinate_float_list[3]))
        await asyncio.sleep(3)
        line_number = line_number + 1
        coordinate_string_array = coordinates_file.readline()[:-1].split('|')

    coordinates_file.close()

    await stop_offboard(drone)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
