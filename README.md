# Python-Autonomous-Drone-Swarm

A Python-based project for controlling and coordinating multiple drones using the MAVSDK framework. This project enables autonomous flight control, swarm coordination, and various test flight patterns for multiple drones.

## Project Overview

This project provides a robust framework for controlling multiple drones simultaneously, allowing for complex flight patterns, autonomous navigation, and synchronized movements. It's built on top of MAVSDK, a modern SDK for drone communication using MAVLink, making it compatible with various drone platforms that support the MAVLink protocol.

## Features

- Multiple drone control and coordination
- Autonomous takeoff and landing capabilities
- Pre-programmed flight patterns and maneuvers
- Real-time flight control and monitoring
- Utility functions for drone management
- Test flight programs for various scenarios
- Environment setup and configuration tools

## Project Structure

The project is organized into several key directories:

### `/flight_programs`
Contains the main flight control programs for executing various drone maneuvers and patterns:

- `mission_directions.py`: Implements mission-based navigation using waypoints defined in mission_plan.txt
- `mission_plan.txt`: Contains waypoint coordinates and mission parameters
- `offboard_directions.py`: Handles offboard control for precise movement directions
- `offboard_plan.txt`: Defines movement patterns for offboard control

### `/test_flights`
Houses various test programs for different flight capabilities:

- `takeoff_and_land.py`: Basic takeoff and landing functionality demonstration
- `goto.py`: Simple point-to-point navigation test
- `manual_control.py`: Implementation of manual control interface
- `mission.py`: Complex mission planning and execution test
- `offboard_attitude.py`: Tests attitude control in offboard mode
- `offboard_position_ned.py`: Position control using NED (North-East-Down) coordinates
- `offboard_velocity_body.py`: Velocity control in body frame
- `offboard_velocity_ned.py`: Velocity control in NED frame

### `/utilities`
Contains helper functions and utility modules:

- `drone_helpers.py`: Core functions for drone connection, control mode switching, and common operations
- `arm.py`: Functions for safely arming the drone
- `disarm.py`: Safe disarming procedures and checks
- `telemetry.py`: Functions for reading and processing drone telemetry data

### Root Directory Files

- `setup-env.py`: Environment setup script that configures Python path and dependencies

## Code Details

### Utility Modules
- `drone_helpers.py`: Core module containing:
  - `connect_drone()`: Establishes connection with drone using MAVLink
  - `start_offboard()`: Initiates offboard control mode
  - `start_manual()`: Switches to manual control mode
  - `stop_offboard()`: Safely exits offboard control

### Flight Programs
- `mission_directions.py`: 
  - Reads mission plans from text files
  - Executes waypoint-based navigation
  - Monitors mission progress
  - Handles takeoff, mission execution, and landing

### Test Programs
- Each test program focuses on a specific aspect of drone control:
  - Position control (NED coordinates)
  - Velocity control (body and NED frame)
  - Attitude control
  - Manual control interface
  - Basic movement patterns

## Prerequisites

- Python 3.7 or higher
- MAVSDK-Python
- Compatible drone hardware with MAVLink support
- Required Python packages (specified in requirements)

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/python-drone-swarm.git
cd python-drone-swarm
```

2. Set up the Python environment:
```bash
python setup-env.py
```

3. Install required dependencies:
```bash
pip install mavsdk
```

## Usage

1. Connect your drone(s) to your computer
2. Configure the connection settings in the respective flight program
3. Run the desired flight program:
```bash
python test_flights/takeoff_and_land.py -d <serial_device> -b <baud_rate>
```

## Safety Considerations

- Always follow local drone regulations and laws
- Maintain visual line of sight with all drones
- Test in open areas away from people and obstacles
- Have a fail-safe mechanism ready
- Monitor battery levels and connection status

## Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, or suggest new features.
