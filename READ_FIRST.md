# FoxbodyBCM - READ FIRST

Last updated: 2026-08-12

This file is the first thing to read before changing BCM code, wiring plans or hardware assignments.

## Current milestone

Freeze hardware/I/O architecture, finish readable terminal-level schematics, then implement the real BCM software around that frozen map.

## Current architecture decisions

- Raspberry Pi 4B is the high-level BCM controller.
- 24DIB32 NPN 32-channel RS485 board is the primary digital-input board.
- OPMSD16 PNP 16-channel 12 V MOSFET board is the primary one-direction output/control board.
- Windows use one Cytron MDD20A dual H-bridge: one channel per window motor.
- Door locks use one Cytron MDD10A dual H-bridge: one channel per lock actuator.
- Do NOT design four-relay-per-door reversing circuits.
- Bosch-style automotive relays are reserved for the few circuits that genuinely need high-current mechanical isolation/fail-safe handling.
- Factory gauge cluster is removed; BCM owns fuel level and sends it to the digital dash.
- MicroSquirt owns engine management and remains independent from BCM convenience/security logic.

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
7. `config/io_map.json`
8. `docs/schematics/README.md` and the SVG schematic sheets

Existing historical/research docs remain useful, but if they conflict with the files above, the files above win unless intentionally revised.

## Current schematic files

- `docs/schematics/01_core_power.svg`
- `docs/schematics/04_door_locks_hbridge.svg`
- `docs/schematics/05_windows_hbridge.svg`

These are editable vector source. They show the corrected solid-state architecture but are not marked FINAL until exact terminal order, fuse size, wire gauge/color, connector IDs and measured/verified loads are added.

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

1. Verify exact physical terminal layout and electrical behavior of the 24DIB32 and OPMSD16 boards in hand.
2. Verify/select ADC and analog protection for fuel/current/voltage sensing.
3. Finalize exact MDD20A/MDD10A control interface and power protection.
4. Expand schematic set to lighting, wipers, starter/ACC/ignition, cooling, sensors and communications.
5. Add fuse numbers, wire gauges/colors, splice IDs and connector IDs.
6. Freeze `config/io_map.json` as v1 hardware map.
7. Implement HAL/drivers from that map.
8. Implement each feature module as non-blocking state machines.
9. Bench test every subsystem before vehicle wiring.

## Safety rules

- Starter defaults OFF.
- BCM security logic never intentionally kills an already-running engine.
- High-current motors do not return current through Pi/signal grounds.
- Opposite H-bridge directions are software-interlocked and include reversal dead-time.
- Every high-current branch is independently fused.
- Raw automotive +12 V inputs are conditioned as required before logic electronics.
