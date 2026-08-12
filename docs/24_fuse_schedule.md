# FoxbodyBCM Fuse Schedule

Status: V1 DESIGN BASELINE
Last updated: 2026-08-12

These are the fuse values currently shown on the schematic set. They are design values, not permission to install wiring smaller than the fuse can safely protect. Final harness release still requires wire-gauge and measured-load verification.

| Fuse | Circuit | Baseline |
|---|---|---:|
| F00 | BCM/body main distribution | 125A |
| F01 | BCM Controller / Pi DC-DC | 5A |
| F02 | Input Board / 24DIB32 | 3A |
| F03 | Output Board control / OPMSD16 | 5A |
| F04 | Window Driver / MDD20A | 40A |
| F05 | Lock Driver / MDD10A | 20A |
| F06 | Headlights low beam | 20A |
| F07 | High beams | 20A |
| F08 | Parking / marker lights | 15A |
| F09 | Turn / hazard lamps | 15A |
| F10 | Horn | 20A |
| F11 | Rear defrost | 30A |
| F12 | Puddle lights | 5A |
| F13 | Courtesy / interior lights | 10A |
| F14 | Wiper motor | 25A |
| F15 | Washer pump | 10A |
| F16 | Hatch release | 15A |
| F17 | Fuel-door actuator | 10A |
| F18 | Starter control / solenoid-S branch | 15A |
| F19 | Ignition / RUN switched bus | 30A |
| F20 | Accessory / retained-accessory bus | 30A |
| F21 | Cooling fan 1 | 50A |
| F22 | Cooling fan 2 | 50A |
| F23 | Sensor / analog regulated supply | 5A |

## Power-routing rules

- F21 and F22 are separate battery-side fan feeds and do not pass through F00.
- The starter motor main battery cable does not pass through F00; F18 is only the starter-control/solenoid branch.
- F00 feeds the BCM/body distribution block and its branch fuses.
- Every conductor downstream of a fuse must be sized for that fuse and the installation environment.
- Output Board direct-load design ceiling is 4A continuous even though the published 8-24V per-channel ceiling is under 5A.
- Loads above the Output Board design ceiling, loads with severe inrush, and safety/isolation loads use a dedicated driver or relay.
- Windows and locks use H-bridges, not reversing relay pairs.

## Values requiring measurement before installation release

The following fuse sizes are intentionally conservative baselines and should be confirmed against the installed hardware: F04, F05, F06, F07, F08, F09, F10, F11, F14-F17, F19-F22.

Cooling-fan fuse selection especially depends on the exact Focus fan motors/controller and measured inrush. Rear-defrost fuse selection depends on the actual hatch-grid resistance/current. Ignition/accessory branch values depend on the final replacement harness load allocation.
