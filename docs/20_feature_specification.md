# FoxbodyBCM Feature Specification

Status: CURRENT DESIGN INTENT
Last updated: 2026-08-12

This document captures user-facing behavior that has been agreed or strongly selected during design discussions. It is intentionally separate from hardware pin assignments so behavior can survive hardware changes.

## Power / start behavior

- Push-button start replaces ordinary key-start behavior.
- Defrost switch is repurposed as the momentary start/command button while retaining normal defrost operation through BCM logic.
- Clutch + start button = crank/start request.
- Start button without clutch = accessory mode request.
- Clutch + start button while engine is running = engine-off request.
- Starter output is inhibited if RPM indicates the engine is already running.
- Retained accessory power keeps radio/accessories on after engine shutdown until either door opens.
- Accessory auto-off approximately 2 minutes when appropriate to protect the battery.

## Emergency start override

Current planned sequence:

- Glove-box hatch button: two presses.
- Defrost/start button: one press.
- Brake + start button to complete/start.

Normal hatch/defrost function waits about 3 seconds after the initial qualifying press. If the rest of the override sequence is not entered, normal function proceeds.

## Locks / access

- Bluetooth phone proximity is a primary authorization input.
- Use distance bands/hysteresis so marginal RSSI does not cause rapid arm/disarm cycling.
- Auto-lock around 15 mph.
- Unlock when ignition turns off.
- Multi-press convenience behavior: one press unlock doors; two presses hatch; three presses fuel door, where mapped to the chosen button.
- Windows can close on lock.
- Puddle/logo lights illuminate with approach/unlock behavior.
- Headlights can flash for lock/security confirmation.

## Alarm / security

- Pi handles alarm logic.
- Inputs include driver/passenger door, hatch, hood, authorization state and IMU-based shock/tilt/tow events.
- No cabin motion sensor in v1.
- Panic mode uses horn and exterior lighting.
- Unauthorized start attempts are logged.
- Security can inhibit starting but must not deliberately kill a running engine.
- Main-battery disconnect while armed should be logged and handled when backup power is implemented.

## Windows

- Driver and passenger window motors are independently controlled through H-bridges.
- Manual switch commands go to BCM inputs.
- Auto-up/down logic can be added in software.
- Current sensing is used for obstruction/end-stop detection.
- Hot-car mode: if cabin exceeds configured threshold, open windows about 15% when safe.
- Rain detected while windows are vented/open: close them.
- Lock command can close windows.
- If auto-close reverses/stops because of overcurrent/obstruction, log the event and optionally honk horn as a local warning so the car is not unknowingly left open before rain.

## Lighting

- Automatic headlights at night via ambient light sensor.
- Manual lighting switch overrides automatic state while engine is on.
- High-beam stalk/input controls high beams.
- One-touch turn signal produces approximately three flashes.
- Follow-me-home exterior lights about 60 seconds.
- Mirror-mounted logo projector puddle lights included.
- Hazard reminder can beep/honk after approximately 30 seconds if desired/configured.

## Wipers / washer

- Wiper park feedback is required.
- Mist / tap-to-wipe supported.
- Variable intermittent planned.
- Low and high speeds supported.
- Washer hold runs washer and wipers.
- After washer is released, wipers continue for 2-3 passes.
- About 6 seconds later, perform one courtesy wipe.
- Rain sensor can support future automatic/intermittent operation.

## Rear defrost

- Factory defrost switch becomes a BCM input.
- Rear defrost grid is controlled by a BCM output/power stage.
- The same physical button participates in the start/override logic, which is why normal defrost action may be delayed briefly while the BCM resolves button intent.

## Hatch / fuel door

- Hatch button becomes a BCM input.
- Hatch release becomes a BCM-controlled output.
- Hatch input participates in emergency override sequence.
- Fuel-door release can be BCM controlled if the final actuator hardware is installed.

## Cooling

- Dual/two-speed electric fan management.
- Fan after-run for up to roughly 3 minutes after shutdown when temperature requires it.
- Fan current monitoring can detect commanded-on/no-current failure.
- Overheat protection/limp warning logic.
- MicroSquirt should retain an independent emergency cooling path if practical.

## Fuel level / fuel management

- BCM owns fuel level because the factory analog gauge cluster is removed.
- Initial sender is factory fuel sender.
- Fuel sender is read through protected analog/ADC circuitry.
- Calibration is learned from known fuel additions on level ground.
- Suggested calibration points: near empty, 2 gal, 5 gal, 10 gal, 15 gal and full as practical.
- Use interpolation and time filtering to reduce slosh.
- Future: gallons remaining, distance-to-empty, fill-up detection/history, MPG and fuel-cost data.

## TPMS

- Four-wheel TPMS desired.
- Dash should show individual tire pressure and temperature.
- Warn on low pressure, excessive temperature or lost sensor.

## Diagnostics / service

- Fault classes: INFO, WARNING, CRITICAL.
- Store reason codes rather than generic fault names.
- Circular event log prevents unbounded storage growth.
- Serious events can save before/after sensor snapshots.
- Live diagnostics show every relevant input/output and sensor.
- Boot self-test checks communication, storage and major I/O/sensor subsystems.
- Service/Test mode can command outputs manually while parked with safety interlocks.
- Service/Test examples: horn, puddle lights, locks, windows, wipers, fans and exterior lighting.

## Fail-safe philosophy

- BCM failure should not intentionally shut off a running engine.
- Starter defaults OFF.
- Opposite H-bridge directions are mutually exclusive.
- Critical road-safety functions should have a defined safe fallback where practical.
- Fancy convenience features may fail disabled rather than adding dangerous complexity.
- Keep the last two known-good software/settings backups.

## User interface

Primary display plan:

- Dash
- Vehicle
- BCM Controls
- TPMS
- Weather / Traffic when internet is available
- Diagnostics
- Service / Test
- Settings

Critical warnings can interrupt any page. Speed/RPM/turn/high-beam/critical status should remain visible in a compact region when practical.

The small extra touchscreen is reserve hardware. The BCM API must permit moving controls to it later without changing underlying vehicle logic.

## Future connectivity

- Cellular hotspot/modem is optional future hardware.
- With internet access, remote status, alerts, weather, traffic and other connected features become possible.
- iPhone interface should be a companion control/status client, not the only means of vehicle operation.
