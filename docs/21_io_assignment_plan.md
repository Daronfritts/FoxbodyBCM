# FoxbodyBCM I/O Assignment Plan

Status: PROVISIONAL BASELINE - MUST BE VERIFIED AGAINST FINAL BOARD TERMINALS BEFORE VEHICLE WIRING
Last updated: 2026-08-12

This file is the working map that software and schematics will converge on. It is intentionally explicit so the project does not depend on chat history.

## 24DIB32 digital input assignments

| Channel | Function | Source |
|---|---|---|
| X00 | Driver door ajar | Factory door switch |
| X01 | Passenger door ajar | Factory door switch |
| X02 | Hatch ajar | Factory hatch switch |
| X03 | Hood open | Added hood plunger/microswitch |
| X04 | Brake pedal | Factory brake switch through appropriate interface |
| X05 | Clutch pedal | Factory/additional clutch switch |
| X06 | Parking brake | Factory parking-brake switch |
| X07 | Reverse state | Factory reverse-light circuit through protected interface |
| X08 | Start/defrost button command | Repurposed defrost/start switch logic |
| X09 | Rear defrost command | Same physical button after intent handling / dedicated contact if available |
| X10 | Glove-box hatch button | Hatch / emergency override sequence |
| X11 | Door lock command | Lock switch |
| X12 | Door unlock command | Unlock switch |
| X13 | Driver window UP | Driver window switch |
| X14 | Driver window DOWN | Driver window switch |
| X15 | Passenger window UP | Passenger window switch |
| X16 | Passenger window DOWN | Passenger window switch |
| X17 | Wiper mist | Multifunction switch |
| X18 | Wiper intermittent | Multifunction switch |
| X19 | Wiper low | Multifunction switch |
| X20 | Wiper high | Multifunction switch |
| X21 | Washer request | Multifunction switch |
| X22 | Headlight/manual lighting request | Lighting switch |
| X23 | High beam request | Stalk / multifunction switch |
| X24 | Left turn request | Turn-signal switch |
| X25 | Right turn request | Turn-signal switch |
| X26 | Hazard request | Hazard switch |
| X27 | Ignition/run sense | Vehicle power-state feedback through protected interface |
| X28 | Wiper park | Wiper motor park contact through appropriate interface |
| X29 | Fuel-door command | Optional fuel-door button / assigned convenience input |
| X30 | Spare | Reserved |
| X31 | Spare | Reserved |

### Input-board design notes

- Do not assume every factory switch is ground-switching. Measure/verify each circuit before connecting.
- Any raw +12 V signal must be interfaced according to the actual 24DIB32 input topology and verified datasheet/silk-screen.
- Grounds and commons must follow the exact board version installed in the car.
- Switch wiring should be low-current command wiring only once intercepted by BCM.

## OPMSD16 output assignment concept

The final OPMSD16 map must be verified against the exact board output polarity and current rating. The following is the intended logical allocation, not permission to connect a high-current motor directly.

| Output | Intended function | Load strategy |
|---|---|---|
| Y01 | Parking/running lamps | Direct only if verified within rating; otherwise relay/driver coil |
| Y02 | Headlamp enable | Relay/driver control likely |
| Y03 | High beam enable | Relay/driver control likely |
| Y04 | Left turn output | Direct/driver depending lamp load |
| Y05 | Right turn output | Direct/driver depending lamp load |
| Y06 | Horn | Relay/driver control likely |
| Y07 | Rear defrost | Relay/contactor control likely because grid current is high |
| Y08 | Hatch release | Direct only if solenoid current/transient is within rating, otherwise relay/driver |
| Y09 | Fuel-door release | Direct only if actuator current is within rating, otherwise relay/driver |
| Y10 | Driver-lock H-bridge command A / spare control | Logic/control only |
| Y11 | Driver-lock H-bridge command B / spare control | Logic/control only |
| Y12 | Passenger-lock H-bridge command A / spare control | Logic/control only |
| Y13 | Passenger-lock H-bridge command B / spare control | Logic/control only |
| Y14 | Wiper low control | Relay/driver/control stage |
| Y15 | Wiper high control | Relay/driver/control stage |
| Y16 | Washer pump | Direct if verified or relay/driver control |

The Cytron motor drivers may be better controlled from MCP23017/Pi-safe logic outputs instead of consuming OPMSD16 power channels. That will be frozen after logic-level compatibility is verified.

## Cytron MDD20A - window motor assignment

- Channel 1 motor terminals -> Driver window motor two wires.
- Channel 1 direction/control inputs -> BCM logic outputs DR_WIN_A / DR_WIN_B.
- Channel 2 motor terminals -> Passenger window motor two wires.
- Channel 2 direction/control inputs -> BCM logic outputs PS_WIN_A / PS_WIN_B.
- Power input -> individually fused automotive +12 V supply sized for both channel loads.
- Ground -> dedicated high-current ground to BCM/body ground architecture.
- Never command both direction states in an invalid combination.

## Cytron MDD10A - door lock assignment

- Channel 1 motor terminals -> Driver door lock actuator.
- Channel 1 control -> DR_LOCK_A / DR_LOCK_B.
- Channel 2 motor terminals -> Passenger door lock actuator.
- Channel 2 control -> PS_LOCK_A / PS_LOCK_B.
- Power -> fused +12 V.
- Ground -> high-current ground.

## Analog/sensor logical channels

Exact ADC hardware/channel numbers are NOT frozen yet. Use these symbolic names in software so the physical ADC can change without changing feature logic.

- ANALOG_FUEL_LEVEL
- ANALOG_BATTERY_VOLTAGE
- ANALOG_BATTERY_CURRENT
- ANALOG_DRIVER_WINDOW_CURRENT
- ANALOG_PASSENGER_WINDOW_CURRENT
- ANALOG_FAN_CURRENT_1
- ANALOG_FAN_CURRENT_2 or combined fan current if final sensor is shared
- ANALOG_OIL_PRESSURE if BCM reads it directly
- ANALOG_FUEL_PRESSURE if BCM reads it directly

## Digital buses / smart sensors

### I2C

Possible devices:

- Ambient light sensor (BH1750 if retained).
- Cabin temp/humidity sensor (SHT31 or final selected unit).
- IMU.
- ADC if I2C type selected.
- MCP23017 expanders.

Every I2C device address must be documented before installation to avoid address conflicts.

### 1-Wire

Possible DS18B20 temperature sensors:

- Cabin temperature if retained.
- Outside-air temperature if retained.
- BCM enclosure temperature if retained.

### RS485

- 24DIB32 input board.
- Additional RS485 I/O only if deliberately added later.

### MicroSquirt / engine data

BCM/dash can consume ECU data for:

- RPM
- Coolant temperature
- Intake-air temperature
- TPS
- MAP
- AFR
- Ignition advance
- Injector pulse width/duty
- Battery voltage
- Engine runtime

## Software naming rule

Application modules must reference symbolic names such as `driver_door`, `window_driver_up`, `fuel_level`, `lock_driver_forward`, etc. Raw X00/Y01 addresses belong only in configuration/HAL files.

That allows the physical I/O map to change without rewriting the behavior modules.
