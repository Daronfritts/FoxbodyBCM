# FoxbodyBCM Hardware Inventory and Purchase Plan

Status: CONSOLIDATED BASELINE
Last updated: 2026-08-12

## Simple names used throughout the project

Use these functional names in schematics, code comments and normal discussion. Specific model/listing data stays documented for terminal references and purchasing.

- **BCM Controller** = Raspberry Pi 4B, 8 GB.
- **Input Board** = 24DIB32 NPN 32-channel isolated digital input / RS485 board.
- **Output Board** = OPMSD16 PNP 16-channel 12 V MOSFET output board.
- **Window Driver** = selected dual high-current H-bridge, 9-30 V motor supply, 3.3/5 V control, A/B direction plus PA/PB PWM, advertised 60 A module rating.
- **Lock Driver** = selected dual H-bridge, 3-14 V supply, 2.2-6 V logic input, 5 A continuous / 9 A peak per channel.
- **I/O Expander** = MCP23017.
- **LIN Adapter** = TJA1020 TTL-LIN interface.
- **RS485 Adapter** = isolated USB-RS485/RS422 adapter.
- **Aux MOSFET Board** = 4-channel low-side MOSFET board, approximately 5 A/channel class.
- **Relay Board** = 8-channel 12 V relay board.
- **Analog Board** = protected ADC/front-end hardware; exact model still to be frozen.
- **5V Power Supply** = 12/24 V to 5 V, 10 A / 50 W DC-DC converter selected for BCM Controller and 5 V electronics.

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

## Selected reversible-motor hardware

Do not buy relay pairs for the windows or locks.

### 1 x Window Driver

Purpose: both power-window motors.

- Dual-channel full H-bridge.
- Motor supply: 9-30 V.
- Advertised module current: up to 60 A; actual usable current must be bench verified and thermally validated.
- 3.3 V and 5 V microcontrollers explicitly supported by the listing.
- Direction control uses A/B logic per channel plus PA/PB PWM.
- Channel 1 = driver window.
- Channel 2 = passenger window.
- Separate Hall current sensing remains planned for obstruction/end-stop protection.

### 1 x Lock Driver

Purpose: both door-lock actuators.

- Dual-channel full H-bridge.
- Supply: 3-14 V.
- Input logic range: 2.2-6 V; 3.3 V logic supported.
- 5 A continuous, 9 A peak per channel per listing.
- Channel 1 = driver lock actuator.
- Channel 2 = passenger lock actuator.
- Lock pulse is short and software timed.

## Conventional automotive relays

Existing Bosch-style relays remain useful but are not the default output method.

Likely relay uses after final verification:

- Starter-solenoid control.
- Main ignition or accessory isolation if required by the final fail-safe design.
- Headlamp low/high beam power where final current exceeds the direct Output Board design ceiling.
- Rear defrost.
- Cooling-fan enable/contactors only if the final fan controller requires them.
- Spare/emergency bypass circuits.

Windows and locks do not use reversing relay pairs.

## Output Board role

Use for one-direction loads within the verified electrical/thermal envelope. Project design ceiling is 4 A continuous per channel even though the published ceiling is just under 5 A at automotive voltage.

Typical direct/control uses:

- Puddle/courtesy LEDs.
- Small lighting loads after current verification.
- Relay coils/contactors.
- Hatch/fuel-door release if measured current and suppression allow it.
- Indicators/auxiliary loads.

## Input Board role

The Input Board is the primary discrete-input board. It reads door/hatch/hood switches, brake/clutch/parking-brake/reverse/run states, start/defrost/hatch/lock/window/wiper/light/hazard commands, wiper park and other on/off states.

Factory signals that present raw +12 V must be conditioned for the exact input configuration rather than assumed safe.

## Analog / sensor interface still required

The BCM Controller has no native analog inputs. A protected Analog Board is required for fuel level, battery voltage/current, Hall current sensors, pressure transducers and other analog sensors.

## Sensor hardware still to finalize

- TPMS receiver + four wheel sensors.
- IMU module for shock/tilt/tow sensing.
- Final rain sensor.
- Final cabin temperature/humidity sensor.
- Final ambient temperature sensor.
- Ambient light sensor if retained.
- Exact battery-current sensor rating.
- Exact window-current sensor ratings.
- Exact fan-current sensor rating.
- Analog Board / front-end hardware.

## Purchase rule

No new BCM hardware should be purchased simply because a generic circuit example uses it. Every purchase must have a named function, verified requirement, defined interface and a reason existing hardware cannot safely perform that job.
