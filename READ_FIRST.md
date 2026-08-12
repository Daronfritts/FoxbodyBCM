# FoxbodyBCM - READ FIRST

Last updated: 2026-08-12

This file is the first thing to read before changing BCM code, wiring plans or hardware assignments.

## Current milestone

The full v1 schematic set now exists at the subsystem level. Next: verify exact physical board terminals, freeze the Output Board logic interface and Analog Board, add final wire gauges/colors/connectors, then implement the real BCM software around the frozen map.

## Current architecture decisions

- Raspberry Pi 4B is the high-level **BCM Controller**.
- Eletechsup 24DIB32 NPN is the **Input Board**.
- Eletechsup OPMSD16 PNP 12V is the **Output Board**.
- Cytron MDD20A is the **Window Driver**: one channel per window motor.
- Cytron MDD10A is the **Lock Driver**: one channel per lock actuator.
- Do NOT design reversing Bosch-relay pairs for windows or locks.
- Output Board project ceiling is 4A continuous per channel; heavier/inrush loads use a relay or dedicated driver.
- Bosch-style relays are intentionally limited mainly to starter control, headlight/high-beam power, horn, rear defrost, ignition/accessory isolation and any final high-current fan enable stage that actually requires one.
- Cooling-fan motor current uses separate high-current feeds/drivers and does not pass through the Output Board.
- Factory gauge cluster is removed; BCM owns fuel level and publishes it to the digital dash.
- MicroSquirt owns engine management and remains independent from BCM convenience/security logic.

## Important newly verified interface fact

The owned Output Board is the **12V-input OPMSD16 version**. Its X1-X16 control inputs require the 8-25V control range for that version, while Pi/MCP23017 logic is only 3.3/5V. Therefore Pi GPIO must NOT connect directly to Output Board X1-X16.

A 16-channel, 3.3V-compatible sinking logic interface must be frozen between the BCM logic and Output Board. This is now explicitly shown on `docs/schematics/03_output_board.svg` rather than being hidden or assumed.

## Superseded information

Any previous relay-heavy schematic showing paired reversing relays for every window/door-lock motor is superseded and must not be used for vehicle wiring.

## Source-of-truth files

Read in this order:

1. `docs/17_master_build_plan.md`
2. `docs/19_hardware_inventory_and_purchases.md`
3. `docs/20_feature_specification.md`
4. `docs/21_io_assignment_plan.md`
5. `docs/22_wiring_schematic_spec.md`
6. `docs/23_software_architecture_plan.md`
7. `docs/24_fuse_schedule.md`
8. `config/io_map.json`
9. `docs/schematics/README.md` and the SVG schematic sheets

Existing historical/research docs remain useful, but if they conflict with the files above, the files above win unless intentionally revised.

## Current schematic files

- `docs/schematics/01_core_power.svg`
- `docs/schematics/02_input_board.svg`
- `docs/schematics/03_output_board.svg`
- `docs/schematics/04_door_locks_hbridge.svg`
- `docs/schematics/05_windows_hbridge.svg`
- `docs/schematics/06_lighting_horn_defrost.svg`
- `docs/schematics/07_wipers_washer_hatch.svg`
- `docs/schematics/08_start_ignition_accessory.svg`
- `docs/schematics/09_cooling_fans.svg`
- `docs/schematics/10_sensors_analog_comms.svg`

F00-F23 now have design amperage values in `docs/24_fuse_schedule.md` and on the applicable schematic sheets.

The drawings are editable vector source. The architecture is laid out, but the set is not marked INSTALLATION RELEASE until exact physical terminal order, new-harness wire gauge/color, connector IDs and measured/verified heavy-load currents are added.

## Current code base

Existing code includes:

- `main.py`
- `config.py`
- `hardware.py`
- `gpio_manager.py`
- `logger.py`
- `event_bus.py`
- startup infrastructure
- feature modules under `modules/`

The software architecture rule is: feature modules use symbolic names; raw board channels live only in config/HAL.

## Next tasks

1. Verify exact physical terminal layout/polarity of the Input Board and Output Board in hand.
2. Freeze the 16-channel logic-to-12V sinking interface for Output Board X1-X16.
3. Freeze the Analog Board/front-end for fuel, voltage and current sensing.
4. Copy exact factory connector IDs/pins and relevant factory wire colors from the 1988 EVTM/donor harness.
5. Assign final new-harness wire gauges, colors and splice IDs.
6. Measure/verify heavy loads and adjust fuse values downward where appropriate.
7. Freeze `config/io_map.json` as v1 hardware map.
8. Implement HAL/drivers from that map.
9. Implement each feature module as non-blocking state machines.
10. Bench test every subsystem before vehicle wiring.

## Safety rules

- Starter defaults OFF.
- BCM security logic never intentionally kills an already-running engine.
- High-current motors do not return current through Pi/signal grounds.
- Opposite H-bridge directions are software-interlocked and include reversal dead-time.
- Every high-current branch is independently fused.
- Raw automotive +12V inputs are conditioned as required before logic electronics.
- Brake-light operation remains hardware-safe and independent of BCM software.
