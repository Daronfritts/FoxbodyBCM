# FoxbodyBCM

A modern Raspberry Pi based Body Control Module for the 1987-1993 Ford Mustang Foxbody.

## Project goals

FoxbodyBCM replaces large parts of the original body-control wiring logic with a programmable, serviceable BCM while preserving safe operation of critical vehicle systems.

Main planned features include:

- Push-button start and retained accessory power.
- Bluetooth phone authorization / proximity locking.
- Alarm and security logic.
- Power-window automation with rain/hot-car behavior and current sensing.
- Automatic door locks.
- Automatic headlights, high beams, turn/hazard logic and puddle lights.
- Wiper/washer automation with park sensing and courtesy wipe.
- Cooling-fan control and monitoring.
- BCM-owned digital fuel gauge and calibration.
- TPMS.
- Touchscreen BCM controls integrated with FoxbodyDash.
- Diagnostics, service/test mode, event logging and configuration backups.
- MicroSquirt data integration.

## Hardware architecture

Current baseline:

- Raspberry Pi 4B 8 GB.
- 24DIB32 NPN 32-channel isolated RS485 digital-input board.
- OPMSD16 PNP 16-channel 12 V MOSFET output board.
- MCP23017 GPIO expansion.
- USB-RS485 interface.
- Cytron MDD20A dual H-bridge for both power-window motors.
- Cytron MDD10A dual H-bridge for both door-lock actuators.
- Conventional automotive relays only where they genuinely make sense for high-current/isolation/fail-safe duties.

Windows and locks are not intended to use four-relay-per-door reversing arrangements.

## Read these first

- `READ_FIRST.md` - current milestone, warnings and next work.
- `docs/17_master_build_plan.md` - consolidated architecture and agreed behavior.
- `docs/19_hardware_inventory_and_purchases.md` - what is owned, what is still needed and what not to buy blindly.
- `docs/20_feature_specification.md` - behavioral requirements.
- `docs/21_io_assignment_plan.md` - provisional X/Y/H-bridge assignment map.
- `docs/22_wiring_schematic_spec.md` - rules for the final wire-the-car-from-it schematics.
- `docs/23_software_architecture_plan.md` - software/HAL/state-machine design.
- `config/io_map.json` - machine-readable provisional symbolic I/O map.
- `docs/schematics/` - editable SVG schematic source.

## Project status

Current milestone: hardware/I/O freeze and schematic consolidation before full BCM software implementation and vehicle wiring.

The repository already contains the core configuration manager, logging, event bus, hardware skeleton, GPIO manager, startup/main entry point and feature-module files. The next coding phase should build on those pieces using the frozen I/O map rather than hard-coding board channels throughout feature logic.
