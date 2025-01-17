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

When having a dedicated telemetry transmission channel enable

- RC
  - `crsf_rc`
and disable
- `rc_input`

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

## Actuators

Check the "advanced" box.

- Number of Motors: 4
  - Motor 1: 
    - Position X: 0.24
    - Position Y: 0.48
    - Position Z: 0.05
    - Direction CCW: yes
    - Upwards
  - Motor 2: 
    - Position X: -0.27
    - Position Y: -0.48
    - Position Z: -0.05
    - Direction CCW: yes
    - Upwards
  - Motor 3: 
    - Position X: 0.24
    - Position Y: -0.48
    - Position Z: 0.05
    - Direction CCW: no
    - Upwards
  - Motor 4: 
    - Position X: -0.27
    - Position Y: 0.48
    - Position Z: -0.05
    - Direction CCW: no
    - Upwards

**DO NOT CHANGE THE MOTOR ROTATION CA_ROTOR[i]_AY as this makes the aircraft unstable!**

- PWM AUX:
  - DSHOT 1200
  - AUX 1: Motor 1
  - AUX 2: Motor 2
  - AUX 3: Motor 3
  - AUX 4: Motor 4
  - AUX 8: RC AUX 1 (camera servo)

- `DSHOT_TEL_CFG`: EXT2

For testing servos while the aircraft is not armed enable `COM_PREARM_MODE`.

## RC / MAVLINK input

Servo control:

- `AUX 1 Passthrough RC channel`: Channel 8

**Separate MAVLINK telemetry channel:**

- `RC_CRSF_PRT_CFG`: TELEM1

**MAVLINK through ExpressLRS:**
Connect the ELRS receiver to TELEM1 and configure it:

- `SER_TEL1_BAUD`: 460800 8N1
- `MAV_0_CONFIG`: TELEM1
- `MAV_0_RATE`: 9600 B/s

Reboot the flight controller afterwards (needed to make RC input work).

## Failsafe

Configure failsafe behavior and select a button to power off the motors.

## Battery/Power module

Power sensor:

- `SENS_EN_INA228`: Enabled
- `INA228_CURRENT`: Leave at default (327.68)
- `INA228_SHUNT`: Leave at default (0.0005)

Battery:

- Source: Power Module
- Number of cells (in series): 6
- Empty voltage (per cell): 3.5V
- Full voltage (per cell): 4.2V

Skip the [Battery Voltage/Current Calibration](https://docs.qgroundcontrol.com/master/en/qgc-user-guide/setup_view/power.html) and configure the battery `Voltage Drop on Full Load` as described [here](https://docs.qgroundcontrol.com/master/en/qgc-user-guide/setup_view/power.html#advanced-power-settings).

`Voltage Drop on Full Load` for Tattu LiPo: 0.4V per cell.

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

## Flight controller

Adjust the IMU/FC position against the center of gravity:

`EKF2_IMU_POS_X`: 0.15

Also configure the flight controller pitch using

`SENS_BOARD_Y_OFF`: 30 deg.

Increase the horizontal velocity of the aircraft:

- `MPC_XY_VEL_ALL`: 18 m/s
- `FLW_TGT_MAX_VEL`: 18 m/s
- `LNDMC_XY_VEL_MAX`: 18 m/s

Do not use `MPC_XY_VEL_ALL`!

The Skywinger frame oscillates at ~17.5 Hz (check FFT of IMU). Therefore enable a notch filter:

- `IMU_GYRO_NF0_FRQ`: 17.5 Hz
- `IMU_GYRO_NF0_BW`: 2.0 Hz

## Autotune the PID controller

Use the `altitude` mode and run the steps described [here](https://docs.px4.io/main/en/config/autotune_mc.html).

## ExpressLRS

Enable MAVLINK mode (latest firmware).

Flash TX as RX module:

- Make sure the TX is on the correct firmware
- Go to the hardware page (elrs_tx.local/hardware.json)
- Download that config
- Flash a compatible RX firmware to the TX module
- Load the config you saved

Verify that the fan is working! (`"misc_fan_en": 2`).

How do I know which RX firmware is compatible to the TX module?

- the MCU should match
- Check the target config to see what base target it uses: https://github.com/ExpressLRS/targets

[Alternative approach](./elrs/Converting_an_Emax_Nano_Tx_to_a_Rx.pdf).

## BLHeli32

Connect using Arduino Nano on ports D3, D4, D5, D6 and GND

[![Foo](./blheli32.png)](./blheli32.png)
