#!/usr/bin/env python3

import asyncio
from mavsdk import System
from mavsdk.action import OrbitYawBehavior

async def run():
    drone = System(mavsdk_server_address='localhost', port=50051)

    print("Waiting for drone to connect ...")

    await drone.connect(system_address="udp://:50051")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone discovered!")
            break

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
    await asyncio.sleep(10)

    print('Do orbit at 10m height from the ground')
    orbit_height = position.absolute_altitude_m+10
    yaw_behavior = OrbitYawBehavior.HOLD_FRONT_TANGENT_TO_CIRCLE
    await drone.action.do_orbit(radius_m=10, # 30, negative radius=opposite direction
                                velocity_ms=2,
                                yaw_behavior=yaw_behavior,
                                latitude_deg=53.552558,
                                longitude_deg=10.288934,
                                absolute_altitude_m=orbit_height)
    await asyncio.sleep(60) # 120

    await drone.action.return_to_launch() #  drone will ascend to RTL_RETURN_ALT!
    print("--- Landing - waiting for disarm")

    async for armed in drone.telemetry.armed():
        if not armed:
            break

    print("Finished!")

if __name__ == "__main__":
    # Start the main function
    asyncio.run(run())
