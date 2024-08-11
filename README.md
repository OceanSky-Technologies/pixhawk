# Pixhawk configuration

## Building the PX4 firmware

Follow the [official docs](https://docs.px4.io/main/en/dev_setup/getting_started.html) that describe how to set up the dev environment.

Then start the docker container that comes with it:

```bash
./Tools/docker_run.sh 'bash'
```

The board target is `px4_fmu-v6x_default`.

Also make sure to have the correct branch checked out.

First configure the target:

```bash
make px4_fmu-v6x_default boardconfig
```

Disable these drivers:
- `rc_input` (needed to enable crossfire input for ELRS)

Enable these drivers (some are enabled by default):
- Barometer
  - `bmp388`
  - InvenSense
    - `icp201xx`
- Differential pressure
  - `ms4525do`
- Distance sensors
  - `vl53l1x`
- IMU
  - Invensense
    - `icm45686`
- Magnetometer
  - Bosch
    - `bmm150`
- Optical flow
  - `pmw3901`
- Power monitor
  - `ina228`
- RC
  - `crsf_rc`


Then build the firmware with

```bash
make px4_fmu-v6x_default
```

Uploading the firmware can be done 2 ways:
1. Open `QGroundControl` -> `Vehicle Setup` -> `Firmware`
   1. Select `PX4 Pro` -> `Advanced Settings` -> `Custom Firmware File` and chose the `px4_fmu-v6x_default.px4` file from the `build/px4_fmu-v6x_default` folder.
2. Using `make px4_fmu-v6x_default upload` (not working out of the box with WSL)

To detect the board for firmware update remove the USB connection and plug it back in.

## Model

`Quadcopter X` -> `Generic Quadcopter`

## Radio

- `AUX 1 Passthrough RC channel`: Channel 8

## Actuators

- Number of Motors: 4
  - Motor 1: 
    - Position X: 0.3
    - Position Y: 0.4
    - Direction CCW: yes
    - Upwards
  - Motor 2: 
    - Position X: -0.2
    - Position Y: -0.4
    - Direction CCW: yes
    - Upwards
  - Motor 3: 
    - Position X: 0.3
    - Position Y: -0.4
    - Direction CCW: no
    - Upwards
  - Motor 4: 
    - Position X: -0.2
    - Position Y: 0.4
    - Direction CCW: no
    - Upwards

- PWM AUX:
  - DSHOT 1200
  - AUX 1: Motor 1
  - AUX 2: Motor 2
  - AUX 3: Motor 3
  - AUX 4: Motor 4
  - AUX 8: RC AUX 1 (camera servo)

- `DSHOT_TEL_CFG`: EXT2

For testing servos while the aircraft is not armed enable `COM_PREARM_MODE`.

## RC input

- `RC_CRSF_PRT_CFG`: TELEM2

# Failsafe

Configure failsafe behavior and select a button to power off the motors.

## Battery/Power module

Power sensor:
- `SENS_EN_INA228`: Enabled
- `INA228_CURRENT`: Leave at default (327.68)
- `INA228_SHUNT`: Leave at default (0.0005)

Run the [Battery Voltage/Current Calibration](https://docs.qgroundcontrol.com/master/en/qgc-user-guide/setup_view/power.html) and configure the battery `Voltage Drop on Full Load` as described [here](https://docs.qgroundcontrol.com/master/en/qgc-user-guide/setup_view/power.html#advanced-power-settings).

## Sensors

Air pressure:
- `SENS_EN_MS4525DO`: Enabled

Optical flow sensor:
- `SENS_EN_PMW3901`: Enabled
- Enable for state estimation: `EKF2_OF_CTRL`: Enabled

Distance sensor:
- `SENS_EN_VL53L1X`: Enabled

## OSD

- `MSP_OSD_CONFIG`: TELEM3

## Filter / control

Adjust the IMU/FC position against the center of gravity:

`EKF2_IMU_POS_X`: 0.3

## Autotune the PID controller

Use the `altitude` mode and run the steps described [here](https://docs.px4.io/main/en/config/autotune_mc.html).

## BLHeli32

Connect using Arduino Nano on ports D3, D4, D5, D6 and GND

[![Foo](./blheli32.png)](./blheli32.png)
