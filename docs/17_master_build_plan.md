# FoxbodyBCM Master Build Plan

Status: ACTIVE DESIGN BASELINE
Last consolidated: 2026-08-12

This file is the high-level source of truth for the FoxbodyBCM project. It exists so the design does not depend on chat history.

## Vehicle

- 1988 Ford Mustang Fox Body LX hatchback, 5-speed manual.
- Factory gauge cluster is being removed and replaced by the FoxbodyDash display.
- MicroSquirt handles engine management. The BCM must not become a single point of failure that can intentionally shut off an already-running engine.

## Core architecture

- Raspberry Pi 4B 8 GB is the high-level BCM computer.
- 24DIB32 NPN 32-channel isolated RS485 digital-input board reads switches and discrete vehicle states.
- OPMSD16 PNP 16-channel 12 V MOSFET output board handles suitable one-direction loads and control signals.
- MCP23017 GPIO expansion is available for additional low-current logic/control channels.
- USB-RS485 adapter connects Pi to RS485 I/O.
- Cytron MDD20A: one board, two H-bridge channels, reserved for driver/passenger window motors.
- Cytron MDD10A: one board, two H-bridge channels, reserved for driver/passenger door-lock actuators.
- Conventional automotive relays are to be used only where a relay is genuinely appropriate: starter and selected high-current/fail-safe loads such as headlight feeds or cooling system power if required by the final hardware design.
- Cooling fans use a dedicated high-current fan/PWM power stage; do not run fan motor current through the OPMSD16.

## Design rules

1. Switches are command inputs, not load-carrying controls, unless a safety fallback specifically requires otherwise.
2. Reversible two-wire motors use H-bridges, not relay forests.
3. One-direction low/moderate-current loads use the MOSFET output board when within its verified limits.
4. High-current loads are individually fused near their power source.
5. The Pi never directly drives automotive loads.
6. All inductive loads require appropriate flyback/transient suppression.
7. Automotive input signals that are +12 V are conditioned before reaching logic that cannot accept raw vehicle voltage.
8. Grounds are designed intentionally: battery/body/engine bonding plus dedicated electronics ground distribution.
9. Software output conflicts are interlocked. Opposite H-bridge directions can never be commanded simultaneously.
10. Final wiring must match the committed I/O map; code must use the same symbolic names and assignments.

## Major BCM functions

### Push-to-start / power states

- Defrost switch is reused as the physical start button.
- Clutch + start button = crank/start.
- Start button without clutch = accessory mode.
- Clutch + start button while engine is running = engine off request.
- Accessory power automatically times out after approximately 2 minutes when appropriate.
- Retained accessory power: radio/accessories stay on after engine shutdown until either door is opened.
- Starter can energize only when clutch state is valid and engine RPM indicates not running.

### Emergency/secret start override

Emergency authorization sequence currently defined as:

1. Hatch button in glove box: two presses.
2. Defrost/start button: one press.
3. Brake + start button to continue start authorization.

Normal defrost and hatch operation are delayed approximately 3 seconds after the initial qualifying press so the BCM can determine whether the user is entering the emergency sequence. If the sequence is not continued, the normal hatch/defrost command executes.

### Door locks

- Phone Bluetooth proximity can arm/disarm/lock/unlock based on distance bands, with hysteresis/timing to avoid chatter.
- Auto-lock at approximately 15 mph.
- Unlock when ignition is switched off.
- Requested multi-press behavior: one press unlock doors, two presses hatch, three presses fuel door where applicable.
- Driver/passenger actuators are individually controllable through the MDD10A.

### Security / alarm

- Raspberry Pi is primary alarm/security logic.
- Monitor driver door, passenger door, hatch, hood, vehicle tilt/impact/tow state, authorization state and main-battery events.
- No cabin motion sensor in v1.
- IMU intended for shock/tilt/jacking/tow detection.
- Alarm can flash exterior lights and honk horn.
- Security immobilization prevents unauthorized starting but does not intentionally kill a running engine.
- Event history records triggers and failed authorization attempts.
- Backup power/emergency access remains a design item.

### Windows

- MDD20A provides bidirectional control of both power-window motors.
- Manual window switches are BCM inputs.
- Current sensing is used for end-stop/obstruction logic.
- Rain mode can close windows.
- Hot-car mode can open windows to approximately 15% above a configured cabin-temperature threshold, then close them if rain is detected.
- Windows close on lock when conditions permit.
- If automatic close fails due to overcurrent/obstruction, the BCM logs it and can use the horn as a local warning so the owner does not unknowingly leave the car exposed to rain.

### Lighting

- Automatic headlights based on ambient light.
- Manual switch can override while engine is on.
- High beam controlled from stalk/input.
- One-touch turn signal = approximately three flashes.
- Follow-me-home lighting approximately 60 seconds.
- Puddle/logo projector lights under mirrors are included.
- Headlights flash as part of lock/security confirmation.
- Hazard audible reminder after approximately 30 seconds.

### Wipers / washer

- Wiper park state is monitored.
- Mist/tap-to-wipe and variable intermittent are planned.
- Washer behavior: wipers continue for 2-3 passes after washer is released, then one courtesy wipe about 6 seconds later.
- Rain sensor can eventually support automatic/intermittent wiping.
- Multifunction switch candidate remains under research; newer Ford switch options were documented in docs/16_research_notes.md.

### Cooling

- Two-speed / dual-fan control.
- Up to approximately 3 minutes of fan after-run after key-off when required.
- Overheat limp/protective behavior.
- Fan current sensing for failed-fan detection.
- MicroSquirt must retain an independent/emergency cooling authority path if feasible.

### Fuel level

- BCM owns the fuel gauge because the factory cluster is being removed.
- Initial sensor is the factory tank sender.
- BCM reads the sender through a protected analog/ADC input.
- Calibration is by known fuel additions on level ground: near-empty reference, then known gallon steps such as 2, 5, 10, 15 and full.
- Software interpolates the calibration points and filters slosh.
- Future options include distance-to-empty, fill-up detection, fuel history and consumption estimates using ECU data.

### TPMS

- TPMS is required in the desired feature set.
- Individual tire pressure and temperature should be available to the dash.
- Receiver/sensor hardware selection is still to be finalized.

### Diagnostics / service mode

- INFO / WARNING / CRITICAL fault classes.
- Reason-coded faults instead of generic warnings.
- Circular event history with timestamp, vehicle state and relevant sensor values.
- Serious faults can preserve before/after snapshots.
- Live I/O diagnostics page.
- Self-test on BCM boot.
- Service/Test page can manually command outputs while parked with safety interlocks.
- Examples: puddle lights, horn, window directions, locks, wiper speeds, fan commands and lighting.

### User interface

- Primary plan is to put dash and BCM pages on the main wide display.
- The smaller touchscreen already owned is reserve hardware if the main-screen controls prove inconvenient.
- BCM API/state model must stay display-independent so controls can be moved later without rewriting vehicle logic.
- Expected pages: Dash, Vehicle, BCM Controls, TPMS, Weather/Traffic, Diagnostics, Service/Test, Settings.
- Critical speed/RPM/warnings should remain available even when another page is open.

## Sensors / data

Required or planned physical sensors include:

- Driver door, passenger door, hatch and hood states.
- Brake, clutch, parking brake, reverse and ignition/run sense.
- Cabin temperature and humidity.
- Outside-air temperature.
- Ambient light.
- Rain sensor.
- Battery voltage and battery current.
- Factory fuel sender through ADC.
- Driver/passenger window motor current.
- Cooling fan current.
- BCM enclosure/electronics temperature.
- IMU for impact/tilt/tow detection.
- TPMS receiver + four wheel sensors.

MicroSquirt supplies engine data including RPM, coolant, IAT, TPS, MAP, AFR, ignition data, injector pulse/duty, engine runtime and ECU battery voltage.

## Software modules

Target module organization:

- main.py
- config.py
- hardware.py / HAL
- gpio_manager.py
- logger.py
- event_bus.py
- modules/push_start.py
- modules/door_locks.py
- modules/windows.py
- modules/wipers.py
- modules/headlights.py / lighting.py
- modules/interior_lights.py
- modules/cooling.py
- modules/security.py
- modules/bluetooth.py
- modules/diagnostics.py
- modules/touchscreen.py
- modules/horn.py
- sensor/ADC/current/TPMS/IMU drivers as hardware is finalized

## Current next steps

1. Freeze hardware inventory and verify every board terminal/current specification.
2. Freeze the I/O assignment map.
3. Replace old relay-heavy concept schematics with the actual solid-state architecture.
4. Produce circuit-by-circuit schematics showing exact board terminals, fuses, connectors, wire gauge/color and grounds.
5. Implement the HAL from the frozen I/O map.
6. Implement state machines module by module.
7. Bench-test each circuit before vehicle installation.
8. Commission the vehicle one subsystem at a time.

## Important warning

Any older drawing showing four relays per door or relay pairs for every window/lock is superseded by this plan. Windows use MDD20A H-bridges and locks use MDD10A H-bridges. Do not build the car from an old relay-heavy draft.
