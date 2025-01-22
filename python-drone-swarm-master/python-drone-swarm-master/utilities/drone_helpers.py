import asyncio, sys, os, getopt

from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)

async def connect_drone(opts):
    # Default settings
    # serial_port = "serial:///dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0"
    serial_port = "serial:///dev/serial/by-id//usb-ArduPilot_Pixhawk1_2D004D000D51353136343335-if00"
    baud_rate = "57600"

    for opt, arg in opts:
        if opt == '-d':
            serial_port = arg
        elif opt == '-b':
            baud_rate = arg

    connection_string = serial_port + ':' + baud_rate

    print("-- Connecting To Drone")
    print("connection_string=connection_string")
    drone = System()
    await drone.connect(connection_string)

    # This waits till a mavlink based drone is connected
    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone with UUID: {state.uuid}")
            break

#    print("Waiting for gps...")
#    # Checking if Global Position Estimate is ok
#    async for global_lock in drone.telemetry.health():
#        if global_lock.is_global_position_ok:
#            print("-- Global position state is ok")
#            break

#    print("-- Waiting for drone to go to offboard")
#    async for flight_mode in drone.telemetry.flight_mode():
#        if flight_mode == 'offboard':
#            break


    print("-- Arming")
    await drone.action.arm()
    await asyncio.sleep(2) # Time for arming to sync in.

    return drone

async def start_offboard(drone):
    print("-- Starting offboard")
    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return
    return drone

async def start_manual(drone):
    print("-- Setting initial manual control")
    await drone.manual_control.set_manual_control_input(float(0), float(0), float(0), float(0))
    print("-- Starting manual control")
    await drone.manual_control.start_position_control()
    return drone

async def stop_offboard(drone):
    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")
    return drone
