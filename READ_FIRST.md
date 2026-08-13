# FoxbodyBCM - READ FIRST

Last updated: 2026-08-12

This file is the first thing to read before changing BCM code, wiring plans or hardware assignments.

## Current milestone

The v1 subsystem schematic set exists and Python implementation has started. Next: bench-verify exact physical terminals, finalize Output Board interface and Analog Board, add final wire gauges/colors/connectors, then continue feature modules against the frozen symbolic I/O map.

## Current architecture decisions

- Raspberry Pi 4B is the **BCM Controller**.
- Eletechsup 24DIB32 NPN is the **Input Board**.
- Eletechsup OPMSD16 PNP 12V is the **Output Board**.
- **Window Driver** = selected dual high-current H-bridge, 9-30V supply, 3.3/5V control, A/B direction plus PA/PB PWM; one channel per window.
- **Lock Driver** = selected dual H-bridge, 3-14V supply, 2.2-6V logic, 5A continuous / 9A peak per channel; one channel per lock actuator.
- Windows and locks do NOT use reversing Bosch relay pairs.
- Output Board project ceiling is 4A continuous per channel; heavier/inrush/safety loads use a relay or dedicated driver.
- Bosch-style relays are intentionally limited mainly to starter control and verified heavy/isolation loads such as rear defrost/headlights where required.
- Cooling-fan motor current uses separate high-current feeds/drivers and does not pass through the Output Board.
- Factory gauge cluster is removed; BCM owns fuel level and publishes it to the digital dash.
- MicroSquirt owns engine management and remains independent from BCM convenience/security logic.
- Selected BCM 5V supply is a 12/24V -> 5V, 10A / 50W DC-DC converter; vehicle-side fuse/transient protection is still required.

## Important Output Board interface fact

The owned Output Board is the 12V-input OPMSD16 version. Its X1-X16 control inputs use the higher-voltage control range while Pi/MCP23017 logic is only 3.3/5V. Pi GPIO must therefore NOT connect directly to Output Board X1-X16.

The exact sinking/level interface is still to be frozen and remains shown as an interface stage on `docs/schematics/03_output_board.svg`.

## Superseded information

- Relay-heavy window/lock reversing circuits are superseded.
- Cytron MDD20A/MDD10A are no longer the selected window/lock hardware.
- Legacy direct-RPi.GPIO feature scripts are superseded by the HAL/runtime architecture.

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

F00-F23 have design amperage values in `docs/24_fuse_schedule.md` and on applicable sheets. The drawings are editable vector source but are not INSTALLATION RELEASE until exact terminal order, wire gauge/color, connector IDs and measured/verified heavy-load currents are added.

## Python architecture now active

- `main.py` runs a 50Hz cooperative control loop.
- `runtime.py` schedules non-blocking feature modules.
- `hardware.py` is the symbolic hardware abstraction layer.
- `gpio_manager.py` is currently the safe simulation/stub layer until real Input/Output Board drivers are bound.
- `motor_manager.py` abstracts all reversible H-bridge motors.
- `modules/windows.py` now controls driver/passenger windows non-blocking with reversal dead-time and run timeout hooks.
- `modules/door_locks.py` now controls driver/passenger lock actuators with non-blocking timed pulses.

Rule: feature modules use symbolic names only. Raw Pi pins, RS485 registers, Output Board channels and physical H-bridge pins belong only in driver/HAL code.

## Next tasks

1. Bench-verify exact Window Driver and Lock Driver physical terminal order/polarity on arrival.
2. Bind verified H-bridge control pins into the HAL/motor driver layer.
3. Implement Input Board RS485 driver.
4. Freeze and implement Output Board interface/driver.
5. Freeze Analog Board/front-end for fuel, voltage and current sensing.
6. Add final wire gauges, colors, connector IDs and splice IDs to all schematic sheets.
7. Continue Python modules: push start, lighting, wipers, cooling, security, fuel, diagnostics and touchscreen/API.
8. Bench-test every subsystem before vehicle wiring.

## Safety rules

- Starter defaults OFF.
- BCM security logic never intentionally kills an already-running engine.
- High-current motors do not return current through Pi/signal grounds.
- Opposite H-bridge directions are software-interlocked and include reversal dead-time.
- Every high-current branch is independently fused.
- Raw automotive +12V inputs are conditioned as required before logic electronics.
- Brake-light operation remains hardware-safe and independent of BCM software.
- Reversible motors stop on process shutdown and include maximum-run timing.
