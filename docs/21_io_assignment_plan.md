# FoxbodyBCM I/O Assignment Plan

Status: PROVISIONAL BASELINE - MUST BE VERIFIED AGAINST FINAL BOARD TERMINALS BEFORE VEHICLE WIRING
Last updated: 2026-10-19

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
| X09 | Fuel-door command | Optional fuel-door button / assigned convenience input |
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
| X29 | Spare | Reserved |
| X30 | Spare | Reserved |
| X31 | Spare | Reserved |

### Input-board design notes

- Do not assume every factory switch is ground-switching. Measure/verify each circuit before connecting.
- Any raw +12 V signal must be interfaced according to the actual 24DIB32 input topology and verified datasheet/silk-screen.
- Grounds and commons must follow the exact board version installed in the car.
- Switch wiring should be low-current command wiring only once intercepted by BCM.

## 8-channel mechanical relay board assignments

The 8-channel 12 V mechanical relay board is the BCM's low-current relay-control stage for selected automotive Bosch relays and other circuits where relay isolation is appropriate.

| Relay output | Assigned function | Downstream strategy |
|---|---|---|
| RLY-01 | ACC | Commands Bosch ACC relay coil; Bosch relay carries vehicle accessory load |
| RLY-02 | RUN / IGN | Commands Bosch RUN/IGN relay coil; Bosch relay carries vehicle ignition/run load |
| RLY-03 | START | Commands Bosch START relay coil; Bosch relay carries starter-control/solenoid branch and remains subject to BCM start interlocks |
| RLY-04 | Rear defrost | Commands dedicated Bosch/high-current rear-defrost relay; downstream relay carries the separately fused rear-window grid load |
| RLY-05 | Spare | Unassigned |
| RLY-06 | Spare | Unassigned |
| RLY-07 | Spare | Unassigned |
| RLY-08 | Spare | Unassigned |

## Output Board assignments — approved drawing plan, 2026-10-19

This allocation matches `config/io_map.json` and supersedes earlier conflicting output tables and Y-channel labels in existing SVGs. It is a wiring plan, not completed firmware or an installation release. Existing schematic artwork/generator and runtime bindings still need reconciliation before use.

| Output | Intended function | Load strategy |
|---|---|---|
| Y01 | Parking / marker lamps | Direct only after current, inrush and thermal verification; otherwise dedicated driver |
| Y02 | Headlamp relay command | Relay/driver command only; verify downstream interface |
| Y03 | High-beam relay command | Relay/driver command only; verify downstream interface |
| Y04 | Left turn output | Direct only after current, inrush and thermal verification; otherwise dedicated driver |
| Y05 | Right turn output | Direct only after current, inrush and thermal verification; otherwise dedicated driver |
| Y06 | Horn relay command — reserved | Relay/driver command only; verify downstream interface |
| Y07 | Spare | Unassigned |
| Y08 | Hatch release | Direct only after current, inrush and thermal verification; otherwise dedicated driver |
| Y09 | Fuel-door release | Direct only after current, inrush and thermal verification; otherwise dedicated driver |
| Y10 | Independent fog-light relay command | Relay/driver command only; verify downstream interface |
| Y11 | Spare | Unassigned |
| Y12 | Spare | Unassigned |
| Y13 | Spare | Unassigned |
| Y14 | Wiper LOW control | Relay/driver command only; verify downstream interface |
| Y15 | Wiper HIGH control | Relay/driver command only; verify downstream interface |
| Y16 | Washer control | Direct only after current, inrush and thermal verification; otherwise dedicated driver |

- Four spare outputs: **Y07, Y11, Y12, Y13**.
- Rear defrost: **Pico 1 GP9 → Mechanical Relay A IN4 / channel 4 → automotive rear-defrost relay coil**. Y07 is no longer a defrost command.
- Independent fog lamps: protected/conditioned switch request → **Pico 2 GP22**; command through **I/O Board B1 → Output Interface 2 input 2B / output 2C → Output Board X10 → Y10 → fog-light relay command**. Fog operation must not require the headlamps and must not be cancelled by high beams. Local fog logic is now implemented in the Pico 2 bench firmware; physical output defaults disabled pending electrical verification.
- Horn Y06 remains reserved until the steering-wheel Pico code and horn-relay command path are verified.
- Mechanical Relay A carries ACC, RUN, START and rear-defrost commands on channels 1–4 respectively; Mechanical Relay B channel 1 carries the A2/blower command from Pico 1 GP10. B channels 2–4 remain spare. The owned hardware consists of two separate four-channel 3–3.3 V relay boards; the older single eight-channel 12 V board description above is superseded.
- Puddle/courtesy lighting from the older table is **not assigned by this revision**; the feature remains pending allocation rather than being silently removed.
- Window and lock motor commands use their dedicated drivers, not these 12 V outputs. Final electrical ratings, terminal verification, fuse/wire selection, safe startup and firmware bindings remain pending.

## Selected dual high-current H-bridge - window motor assignment

- Channel 1 motor terminals -> Driver window motor two wires.
- Channel 1 direction/control inputs -> BCM logic outputs DR_WIN_A / DR_WIN_B.
- Channel 2 motor terminals -> Passenger window motor two wires.
- Channel 2 direction/control inputs -> BCM logic outputs PS_WIN_A / PS_WIN_B.
- Power input -> individually fused automotive +12 V supply sized for both channel loads.
- Ground -> dedicated high-current ground to BCM/body ground architecture.
- Never command both direction states in an invalid combination.

## Selected dual H-bridge - door lock assignment

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

## Pico firmware status — 2026-10-21

See `../firmware/README.md` for both complete GP assignment tables, installation,
bench checks and remaining design items. This is a partial bench release, not
vehicle-ready firmware. Starter/RUN/ACC/defrost/blower control logic, motor
control, wipers, releases and horn are not enabled. Physical MCP outputs default
disabled. No Input Board X assignments were changed by this firmware update.
The Pi RS485 input path and direct protected Pico inputs still require a final
circuit-by-circuit ownership/fallback plan. Older SVGs are not updated here.
