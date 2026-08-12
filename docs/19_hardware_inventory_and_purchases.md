# FoxbodyBCM Hardware Inventory and Purchase Plan

Status: CONSOLIDATED BASELINE
Last updated: 2026-08-12

## Simple names used throughout the project

Use these functional names in schematics, code comments and normal discussion. The model number stays documented for terminal references and purchasing.

- **BCM Controller** = Raspberry Pi 4B, 8 GB.
- **Input Board** = 24DIB32 NPN 32-channel isolated digital input / RS485 board.
- **Output Board** = OPMSD16 PNP 16-channel 12 V MOSFET output board.
- **Window Driver** = Cytron MDD20A dual H-bridge motor driver.
- **Lock Driver** = Cytron MDD10A dual H-bridge motor driver.
- **I/O Expander** = MCP23017.
- **LIN Adapter** = TJA1020 TTL-LIN interface.
- **RS485 Adapter** = isolated USB-RS485/RS422 adapter.
- **Aux MOSFET Board** = 4-channel low-side MOSFET board, approximately 5 A/channel class.
- **Relay Board** = 8-channel 12 V relay board.
- **Analog Board** = protected ADC/front-end hardware; exact model still to be frozen.

## Hardware already owned / previously identified

- BCM Controller (Raspberry Pi 4B, 8 GB).
- 1 TB NVMe storage via USB.
- Input Board (24DIB32 NPN 32-channel isolated digital input / RS485 board).
- Output Board (OPMSD16 PNP 16-channel 12 V MOSFET output board).
- I/O Expanders (MCP23017).
- LIN Adapter (TJA1020).
- RS485 Adapter (isolated USB-RS485/RS422).
- Aux MOSFET Board (4-channel low-side MOSFET, approximately 5 A/channel class).
- Relay Board (8-channel 12 V relay board).
- Rain-sensor hardware currently on hand, but the final rain sensor may be replaced with a more automotive-suitable optical unit.
- Miscellaneous current sensors already discussed/purchased; exact ratings must be verified before final assignment.
- Raspberry Pi / vehicle networking hardware already used elsewhere in the project.

## Newly identified missing motor-driver hardware

Do not buy relay pairs for the windows/locks. The correct missing hardware is:

### 1 x Window Driver (Cytron MDD20A)

Purpose: both power-window motors.

- Dual-channel bidirectional brushed-DC motor driver.
- One channel = driver window.
- One channel = passenger window.
- Gives the BCM forward/reverse control without mechanical reversing relays.
- Use current sensing separately for obstruction/end-stop logic.

### 1 x Lock Driver (Cytron MDD10A)

Purpose: both door-lock actuators.

- Dual-channel bidirectional brushed-DC motor driver.
- One channel = driver lock actuator.
- One channel = passenger lock actuator.
- Independent channels preserve future per-door behavior.

## Conventional automotive relays

Existing Bosch-style relays remain useful but are not the default output method.

Likely relay uses after final verification:

- Starter-solenoid control.
- Main ignition or accessory isolation if required by the final fail-safe design.
- Headlamp main/high-beam power if current or fallback strategy makes relay control preferable.
- Rear defrost if the grid current is above the Output Board's safe verified load rating.
- Horn if preferred for isolation/current handling.
- Cooling-fan enable/contactors only if the final PWM/fan controller requires them.
- Spare/emergency bypass circuits.

Do not use Bosch relays as the normal reversing method for windows or door locks once the Window Driver and Lock Driver are installed.

## Output Board role

Use for outputs that are within its verified voltage/current/thermal envelope, including suitable one-direction loads and control signals. Potential examples include:

- Puddle/courtesy lights.
- Small exterior/interior lighting loads if verified.
- Relay coils/contactors.
- Hatch/fuel-door release if current is within limit and suppression is correct.
- Indicators/auxiliary loads.

Final allocation depends on measured load current and verified board specifications.

## Input Board role

The Input Board is the primary discrete-input board.

It reads:

- Door/hatch/hood switches.
- Brake/clutch/parking-brake/reverse/run states.
- Push/start/defrost/hatch/lock/window/wiper/light/hazard switch commands.
- Wiper park.
- Other on/off vehicle states.

Factory signals that present raw +12 V must be conditioned appropriately for the exact input configuration rather than assumed safe.

## Analog / sensor interface still required in final design

The BCM Controller has no native analog inputs. A protected Analog Board is required for analog values such as:

- Fuel sender.
- Battery voltage if not taken solely from another trusted source.
- Hall-effect current sensors.
- Oil/fuel pressure transducers if routed through BCM.
- Any analog rain/light/current sensor selected later.

The exact ADC part is not yet frozen. Do not buy a random ADC solely from an old chat recommendation; select it when the analog channel count, input ranges and protection network are finalized.

## Sensor hardware still to finalize

- TPMS receiver + four wheel sensors.
- IMU module for shock/tilt/tow sensing.
- Final rain sensor.
- Final cabin temperature/humidity sensor.
- Final ambient temperature sensor.
- Ambient light sensor if BH1750 is retained.
- Exact battery-current sensor rating.
- Exact driver/passenger window-current sensor ratings.
- Exact fan-current sensor rating.
- Analog Board / front-end hardware.

## Purchase rule from this point forward

No new BCM hardware should be purchased simply because a generic circuit example uses it. Every new purchase must have:

1. A named function in the frozen schematic.
2. A verified voltage/current requirement.
3. A defined interface to a board terminal.
4. A reason the hardware already owned cannot safely perform that job.

This rule is intended to stop architecture drift and unnecessary duplicate purchases.
