# FoxbodyBCM Wiring / Schematic Specification

Status: DESIGN SOURCE OF TRUTH
Last updated: 2026-08-12

This document defines how the final wire-the-car-from-it schematic must be drawn and what it must contain.

## Naming convention used on all schematics

Use a simple functional name first. Put the actual model number in smaller text underneath or in parentheses.

- **BCM Controller** = Raspberry Pi 4B.
- **Input Board** = 24DIB32 NPN 32-channel RS485 digital input board.
- **Output Board** = OPMSD16 PNP 16-channel 12 V MOSFET output board.
- **Window Driver** = Cytron MDD20A dual H-bridge.
- **Lock Driver** = Cytron MDD10A dual H-bridge.
- **I/O Expander** = MCP23017.
- **Aux MOSFET Board** = 4-channel low-side MOSFET board.
- **Relay Board** = 8-channel 12 V relay board.
- **RS485 Adapter** = isolated USB-RS485/RS422 adapter.
- **LIN Adapter** = TJA1020 TTL-LIN interface.
- **Analog Board** = protected ADC/front-end hardware, exact model still TBD.

These simple names should also be used in code comments, wire labels and documentation unless the exact model number is needed for a terminal reference.

## Required schematic format

The final schematic must be a real line schematic, not a block diagram and not ASCII.

Every circuit sheet must show:

- Battery positive source.
- Fuse number and amperage.
- Wire path from fuse to board/relay/driver/load.
- Exact board terminal names.
- Exact switch terminals where known.
- Exact motor/load terminals.
- Ground path back to chassis/ground bus.
- Connector IDs and pin numbers once final connectors are selected.
- Wire gauge and color for every conductor.
- Splice IDs where one feed branches.
- Relay terminals 30/85/86/87/87a where a relay is actually used.
- H-bridge power/control/motor terminals for windows and locks.
- Sensor signal/power/ground terminals.
- Notes for transient suppression, shielding, twisted pairs or protected interfaces.

## Electrical color convention for drawings

Suggested drawing colors:

- Red: unswitched/fused +12 V power.
- Orange: switched +12 V / load-control power.
- Black: ground.
- Blue: discrete input/switch signal.
- Green: motor/load conductor.
- Purple: analog/sensor signal.
- Gray: communication/bus/reference.

Actual vehicle wire colors will be assigned separately and printed beside each conductor.

## Fuse schedule - v1 baseline

These are now the working fuse values for the schematics. They are not permission to exceed the ampacity of the final wire. If measured load current or final wire size requires a change, the schematic and this table must be changed together.

- **F00 BCM MAIN - 80 A**: feeds BCM electronics/body-power distribution only. Cooling fans, starter high-current path and any other very high-current branches use separate battery feeds and protection.
- **F01 BCM CONTROLLER - 5 A**: 12 V side of the DC/DC converter feeding the BCM Controller.
- **F02 INPUT BOARD - 3 A**: Input Board power.
- **F03 OUTPUT CONTROL - 5 A**: Output Board/control electronics only. High-current loads controlled by the Output Board receive their own branch fuses.
- **F04 WINDOWS - 40 A**: Window Driver common high-current feed for both window channels.
- **F05 LOCKS - 20 A**: Lock Driver common feed for both door-lock actuators.

Additional fuse numbers will be assigned sequentially as the remaining sheets are completed. Every final fuse symbol must show both its fuse ID and amperage on the drawing.

## High-level power topology

Battery + -> main protection -> BCM power distribution -> individual branch fuses.

Separate fused branches are planned for:

- BCM Controller / logic DC-DC supply.
- Input Board.
- Output Board/control loads.
- Window Driver power.
- Lock Driver power.
- Starter control.
- Ignition/accessory power stages.
- Headlight/high-beam feeds if relay controlled.
- Rear defrost.
- Cooling fan power stages.
- Wiper/washer power.
- Horn.
- Lighting/accessory circuits as appropriate.

## Ground topology

- Battery negative bonded to chassis/body and engine block with heavy cable.
- BCM electronics use a documented ground distribution point.
- High-current motor grounds return through suitable gauge wiring to a strong chassis/ground point rather than through BCM Controller/logic grounds.
- Signal grounds are not used as motor-current return paths.
- Shield drains, if used, terminate according to the specific sensor/bus design rather than randomly at both ends.

## Window circuit - required final topology

For each window:

Battery + -> F04 40 A -> Window Driver power input.

Window Driver motor output pair -> two wires of the window motor.

Window Driver ground -> high-current ground point.

Window UP and DOWN switches -> Input Board channels -> BCM software.

BCM Controller logic outputs -> Window Driver direction/control inputs.

Hall current sensor -> appropriate motor/power conductor -> Analog Board -> BCM.

No reversing Bosch relay pair is required for normal window operation.

## Door-lock circuit - required final topology

Battery + -> F05 20 A -> Lock Driver power input.

Lock Driver channel 1 -> driver lock actuator two wires.

Lock Driver channel 2 -> passenger lock actuator two wires.

Lock Driver ground -> high-current ground point.

Lock/unlock switch commands -> Input Board inputs -> BCM.

BCM Controller logic outputs -> Lock Driver control inputs.

No four-relay-per-door arrangement.

## Lighting circuit philosophy

- Use Output Board directly only for loads proven within its continuous current and thermal rating.
- Headlights/high beams may use conventional relays if they are retained as high-current/fail-safe stages.
- Puddle/courtesy LEDs are preferred direct MOSFET loads if current is safely within rating.
- Turn/hazard logic is software controlled with a final power stage selected according to actual lamp current.

## Starter / ignition / accessory

- Starter must use a dedicated automotive relay/solenoid control stage.
- Starter command requires software interlock and should default OFF on BCM failure.
- Ignition/accessory power strategy must be reviewed for safe failure behavior before final wiring.
- Retained accessory power is controlled by BCM but must not compromise engine operation.

## Cooling fans

- Fan motor current does not flow through the Output Board.
- Final fan control uses a dedicated high-current fan/PWM controller or appropriately rated relay/contactor stage.
- Fan current is monitored.
- Fan circuits are independently fused.
- Consider a MicroSquirt emergency/backup fan authority path.

## Input interception example

For a switch such as rear defrost:

- Existing switch load wire is separated from the original direct load path.
- Switch side is routed to an Input Board channel.
- Actual defrost grid is powered from a BCM-controlled output stage/relay.
- BCM interprets the switch press, including the emergency-start-sequence timing, then commands the output.

The same interception model applies to other switches where the BCM takes ownership of the load.

## Fuel sender

Factory sender -> protected measurement network -> Analog Board -> BCM.

Do not power the sender from an arbitrary BCM Controller pin. Final measurement circuit must be designed around the factory sender resistance range and automotive transient protection.

## Final-release gate

A schematic sheet is not marked FINAL until all of the following are present:

1. Board terminal names verified against the exact board in hand.
2. Load current measured or reliably specified.
3. Fuse size selected.
4. Wire gauge selected.
5. Wire color assigned.
6. Connector/pin IDs assigned.
7. Ground path shown.
8. Software symbolic I/O name matched to the same terminal.
9. Bench-test procedure written.

Older relay-heavy draft diagrams are superseded and are not installation instructions.
