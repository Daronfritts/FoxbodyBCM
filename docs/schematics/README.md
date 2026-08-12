# FoxbodyBCM Schematics

These SVG files are the editable vector source for the BCM wiring schematics. They are intended to become the wire-the-car-from-it drawings.

## Board names used on drawings

- **BCM Controller** = Raspberry Pi 4B.
- **Input Board** = Eletechsup 24DIB32 NPN 32-channel RS485 digital-input board.
- **Output Board** = Eletechsup OPMSD16 PNP 12V 16-channel MOSFET output board.
- **Window Driver** = Cytron MDD20A dual 20A H-bridge.
- **Lock Driver** = Cytron MDD10A dual 10A H-bridge.
- **I/O Expander** = MCP23017.
- **RS485 Adapter** = isolated USB-RS485/RS422 adapter.
- **Analog Board** = protected ADC/front-end, exact hardware still to freeze.

## Current sheets

- `01_core_power.svg` - battery, F00 main distribution, logic power, Input/Output boards, Window/Lock drivers and ground architecture.
- `02_input_board.svg` - Input Board terminals, X00-X31 assignments, NPN common wiring and raw +12V signal-conditioning examples.
- `03_output_board.svg` - Output Board direct-load rules, provisional Y01-Y16 assignments and required logic-to-12V control interface.
- `04_door_locks_hbridge.svg` - solid-state lock wiring using one Lock Driver (MDD10A) for both actuators.
- `05_windows_hbridge.svg` - solid-state power-window wiring using one Window Driver (MDD20A) for both window motors.
- `06_lighting_horn_defrost.svg` - headlights, high beams, marker/turn/hazard, horn, rear defrost, puddle and courtesy lighting.
- `07_wipers_washer_hatch.svg` - wiper/park, washer, hatch release and fuel-door actuator.
- `08_start_ignition_accessory.svg` - starter relay, ignition/RUN relay, retained accessory power and emergency override logic.
- `09_cooling_fans.svg` - separate high-current fan feeds, control authority and fan-current sensing.
- `10_sensors_analog_comms.svg` - fuel sender, current sensors, digital sensors, TPMS, IMU, RS485, MicroSquirt and dash communications.

## Fuse schedule

See `../24_fuse_schedule.md` for F00-F23 and their amperage values. Every fuse shown on these drawings has a design amperage assigned.

## Important installation status

The system architecture and fuse schedule are now laid out, but **do not terminate the complete vehicle harness from these files yet**. Before the set is marked INSTALLATION RELEASE, the remaining work is:

1. Verify the physical screw-terminal order and polarity on the exact Input Board and Output Board in hand.
2. Freeze the 16-channel 3.3V-to-12V sinking logic interface needed to drive the owned 12V-input Output Board.
3. Freeze the Analog Board/front-end.
4. Copy exact factory connector IDs, motor terminal IDs and relevant factory wire colors from the 1988 Mustang EVTM / donor harness.
5. Assign actual new-harness wire colors and gauges.
6. Measure or reliably verify heavy load current and adjust branch fuse values downward where appropriate.

Any older relay-heavy window/lock drawing is superseded. Windows and locks use H-bridges, not reversing Bosch relay pairs.
