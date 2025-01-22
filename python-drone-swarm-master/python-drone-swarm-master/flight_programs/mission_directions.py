#!/usr/bin/env python3

import asyncio, sys, os, getopt

from utilities.drone_helpers import connect_drone

from mavsdk import System
from mavsdk.mission import (MissionItem, MissionPlan)

async def run():

    mission_plan_file_name = os.path.dirname(__file__) + "/mission_plan.txt"

    try:
        opts, args = getopt.getopt(sys.argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('mission_directions.py -d <serial_device> -b <baud_rate> -c <mission_plan_text_file>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('mission_directions.py -d <serial_device> -b <baud_rate> -c <mission_plan_text_file>')
            sys.exit(2)
        elif opt == '-c':
            mission_plan_file_name = arg

    drone = await connect_drone(opts)

    print_mission_progress_task = asyncio.ensure_future(print_mission_progress(drone))
    running_tasks = [print_mission_progress_task]
    termination_task = asyncio.ensure_future(observe_is_in_air(drone, running_tasks))
    mission_items = []

    try:
        mission_plan_file = open(mission_plan_file_name , "r")
    except os.FileOpenError as error:
        print(f"Could not open file!")
        return

    line_number = 0

    coordinate_string_array = mission_plan_file.readline()[:-1].split('|')
    while len(coordinate_string_array) == 4:
        print("-- Setting Mission Direction" + str(line_number))
        coordinate_float_list = [ float(coordinate) for coordinate in coordinate_string_array ]
        print(coordinate_float_list)

        mission_items.append(MissionItem(
            coordinate_float_list[0],
            coordinate_float_list[1],
            coordinate_float_list[2],
            coordinate_float_list[3],
            True,
            float('nan'),
            float('nan'),
            MissionItem.CameraAction.NONE,
            float('nan'),
            float('nan')))

        line_number = line_number + 1
        coordinate_string_array = mission_plan_file.readline()[:-1].split('|')

    mission_plan_file.close()
    mission_plan = MissionPlan(mission_items)

    await drone.mission.set_return_to_launch_after_mission(True)

    print("-- Uploading mission")
    await drone.mission.upload_mission(mission_plan)

    print("-- Arming")
    await drone.action.arm()

    print("-- Starting mission")
    await drone.mission.start_mission()

    await termination_task

async def print_mission_progress(drone):
    async for mission_progress in drone.mission.mission_progress():
        print(f"Mission progress: "
              f"{mission_progress.current}/"
              f"{mission_progress.total}")


async def observe_is_in_air(drone, running_tasks):
    """ Monitors whether the drone is flying or not and
    returns after landing """

    was_in_air = False

    async for is_in_air in drone.telemetry.in_air():
        if is_in_air:
            was_in_air = is_in_air

        if was_in_air and not is_in_air:
            for task in running_tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            await asyncio.get_event_loop().shutdown_asyncgens()

            return


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
