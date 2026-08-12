# FoxbodyBCM Schematics

These SVG files are the editable vector source for the BCM wiring schematics. They are intended to become the wire-the-car-from-it drawings.

Current sheets:

- `01_core_power.svg` - battery, main fuse, logic power, input/output boards, ground architecture.
- `04_door_locks_hbridge.svg` - corrected solid-state door-lock wiring using one MDD10A board for both lock actuators.
- `05_windows_hbridge.svg` - corrected solid-state power-window wiring using one MDD20A board for both window motors.

Important: these are architecture-level schematics. Before any sheet is marked FINAL, exact board terminal order, fuse values, wire gauge/colors, connector IDs and measured load currents must be verified and added.

Any older relay-heavy window/lock drawing is superseded. Windows and locks use H-bridges, not four relays per door.
