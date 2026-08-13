# FoxbodyBCM Schematics

These SVG files are the editable vector source for the BCM wiring schematics. They are intended to become the wire-the-car-from-it drawings.

## Board names used on drawings

- **BCM Controller** = Raspberry Pi 4B.
- **Input Board** = Eletechsup 24DIB32 NPN 32-channel RS485 digital-input board.
- **Output Board** = Eletechsup OPMSD16 PNP 12V 16-channel MOSFET output board.
- **Window Driver** = selected dual high-current H-bridge; 9-30V supply, 3.3/5V logic, A/B direction plus PA/PB PWM; one channel per window.
- **Lock Driver** = selected dual H-bridge; 3-14V supply, 2.2-6V logic, 5A continuous / 9A peak per channel; one channel per lock actuator.
- **I/O Expander** = MCP23017.
- **RS485 Adapter** = isolated USB-RS485/RS422 adapter.
- **Analog Board** = protected ADC/front-end, exact hardware still to freeze.
- **5V Power Supply** = 12/24V to 5V, 10A / 50W DC-DC converter.

## Current sheets

- `01_core_power.svg` - battery, F00 main distribution, 5V supply, Input/Output boards, Window/Lock drivers and ground architecture.
- `02_input_board.svg` - Input Board terminals, X00-X31 assignments, NPN common wiring and raw +12V signal-conditioning examples.
- `03_output_board.svg` - Output Board direct-load rules, provisional Y01-Y16 assignments and required logic interface.
- `04_door_locks_hbridge.svg` - solid-state lock wiring using the selected dual 5A/9A Lock Driver.
- `05_windows_hbridge.svg` - solid-state power-window wiring using the selected dual 9-30V high-current Window Driver.
- `06_lighting_horn_defrost.svg` - headlights, high beams, marker/turn/hazard, horn, rear defrost, puddle and courtesy lighting.
- `07_wipers_washer_hatch.svg` - wiper/park, washer, hatch release and fuel-door actuator.
- `08_start_ignition_accessory.svg` - starter relay, ignition/RUN relay, retained accessory power and emergency override logic.
- `09_cooling_fans.svg` - separate high-current fan feeds, control authority and fan-current sensing.
- `10_sensors_analog_comms.svg` - fuel sender, current sensors, digital sensors, TPMS, IMU, RS485, MicroSquirt and dash communications.

## Fuse schedule

See `../24_fuse_schedule.md` for F00-F23 and their amperage values. Every fuse shown on these drawings has a design amperage assigned.

## Important installation status

The architecture is laid out, but **do not terminate the complete vehicle harness from these files yet**. Before INSTALLATION RELEASE:

1. Bench-verify the actual screw-terminal and signal-header order/polarity on the exact Input Board, Output Board, Window Driver and Lock Driver in hand.
2. Freeze the Output Board logic-level/sinking interface.
3. Freeze the Analog Board/front-end.
4. Copy exact factory connector IDs, motor terminal IDs and relevant factory wire colors from the 1988 Mustang EVTM/donor harness.
5. Assign actual new-harness wire colors, gauges and splice IDs.
6. Measure/verify heavy-load current and adjust branch fuse values where appropriate.

Older Cytron and relay-heavy window/lock drawings are superseded. Windows and locks use the selected H-bridge boards, not reversing Bosch relay pairs.
