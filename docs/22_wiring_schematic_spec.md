# FoxbodyBCM Wiring / Schematic Specification

Status: DESIGN SOURCE OF TRUTH
Last updated: 2026-08-12

This document defines how the final wire-the-car-from-it schematic must be drawn and what it must contain.

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

## High-level power topology

Battery + -> main protection -> BCM power distribution -> individual branch fuses.

Separate fused branches are planned for:

- Pi / logic DC-DC supply.
- 24DIB32 input board.
- OPMSD16 output board/control loads.
- Window H-bridge power.
- Lock H-bridge power.
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
- High-current motor grounds return through suitable gauge wiring to a strong chassis/ground point rather than through Pi/logic grounds.
- Signal grounds are not used as motor-current return paths.
- Shield drains, if used, terminate according to the specific sensor/bus design rather than randomly at both ends.

## Window circuit - required final topology

For each window:

Battery + -> window fuse -> MDD20A power input.

MDD20A motor output pair -> two wires of the window motor.

MDD20A ground -> high-current ground point.

Window UP and DOWN switches -> 24DIB32 input channels -> BCM software.

BCM logic outputs -> MDD20A direction/control inputs.

Hall current sensor -> appropriate motor/power conductor -> ADC -> BCM.

No reversing Bosch relay pair is required for normal window operation.

## Door-lock circuit - required final topology

Battery + -> lock fuse -> MDD10A power input.

MDD10A channel 1 -> driver lock actuator two wires.

MDD10A channel 2 -> passenger lock actuator two wires.

MDD10A ground -> high-current ground point.

Lock/unlock switch commands -> 24DIB32 inputs -> BCM.

BCM logic outputs -> MDD10A control inputs.

No four-relay-per-door arrangement.

## Lighting circuit philosophy

- Use OPMSD16 directly only for loads proven within the board's continuous current and thermal rating.
- Headlights/high beams may use conventional relays if they are retained as high-current/fail-safe stages.
- Puddle/courtesy LEDs are preferred direct MOSFET loads if current is safely within rating.
- Turn/hazard logic is software controlled with a final power stage selected according to actual lamp current.

## Starter / ignition / accessory

- Starter must use a dedicated automotive relay/solenoid control stage.
- Starter command requires software interlock and should default OFF on BCM failure.
- Ignition/accessory power strategy must be reviewed for safe failure behavior before final wiring.
- Retained accessory power is controlled by BCM but must not compromise engine operation.

## Cooling fans

- Fan motor current does not flow through the OPMSD16.
- Final fan control uses a dedicated high-current fan/PWM controller or appropriately rated relay/contactor stage.
- Fan current is monitored.
- Fan circuits are independently fused.
- Consider a MicroSquirt emergency/backup fan authority path.

## Input interception example

For a switch such as rear defrost:

- Existing switch load wire is separated from the original direct load path.
- Switch side is routed to a BCM input channel.
- Actual defrost grid is powered from a BCM-controlled output stage/relay.
- BCM interprets the switch press, including the emergency-start-sequence timing, then commands the output.

The same interception model applies to other switches where the BCM takes ownership of the load.

## Fuel sender

Factory sender -> protected measurement network -> ADC -> BCM.

Do not power the sender from an arbitrary Pi pin. Final measurement circuit must be designed around the factory sender resistance range and automotive transient protection.

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
