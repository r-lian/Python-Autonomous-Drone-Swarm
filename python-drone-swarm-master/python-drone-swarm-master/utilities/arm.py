#!/usr/bin/env python3

import asyncio, sys, os, getopt

from mavsdk import System
from mavsdk.offboard import (Attitude, OffboardError)
from setup import get_connection_string

from utilities.drone_helpers import connect_drone, start_offboard, stop_offboard

async def run():
    try:
        opts, args = getopt.getopt(sys.argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('arm.py -d <serial_device> -b <baud_rate>')
        sys.exit(2)

    drone = await connect_drone(opts)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
