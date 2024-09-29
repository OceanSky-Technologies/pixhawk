#!/usr/bin/env python3

import asyncio
from mavsdk import System


async def run():
    drone = System(mavsdk_server_address="localhost", port=50051)

    print("Waiting for drone to connect ...")

    await drone.connect(system_address="udp://:50051")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone discovered!")
            break

    print("Waiting for drone to have a pose...")

    attitude = await drone.telemetry.attitude_euler().__aiter__().__anext__()

    print(f"{attitude}")

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    position = await drone.telemetry.position().__aiter__().__anext__()

    print(f"Position: {position}")

    await drone.action.set_takeoff_altitude(3)
    await drone.action.set_return_to_launch_altitude(10)

    print("-- Arming")
    await drone.action.arm()

    print("--- Taking Off")
    await drone.action.takeoff()
    await asyncio.sleep(30)

    print("--- Landing - waiting for disarm")
    await drone.action.land()

    async for armed in drone.telemetry.armed():
        if not armed:
            break

    print("Finished!")


if __name__ == "__main__":
    # Start the main function
    asyncio.run(run())
