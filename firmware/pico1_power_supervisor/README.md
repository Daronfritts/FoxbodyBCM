# Pico 1 - Power Supervisor

Target: Raspberry Pi Pico 2 / RP2350 running MicroPython.

## Role

Pico 1 is the always-available low-level power supervisor for FoxbodyBCM. It is intentionally separate from Linux so basic vehicle power behavior does not depend on the Raspberry Pi remaining responsive.

Planned responsibilities:

- Read protected ignition/key state.
- Turn the dashboard display on when ignition becomes active.
- Turn the dashboard display off when ignition becomes inactive while normally leaving the Raspberry Pi running.
- Monitor vehicle battery voltage through a protected analog interface.
- Request a graceful Raspberry Pi shutdown if battery voltage remains below the configured threshold.
- After confirmed shutdown or a defined failsafe timeout, control the final Pi power stage if the installed power hardware supports it.
- Restore/wake the system when ignition becomes active again.
- Report supervisor state/faults to the Raspberry Pi.

## Current status

Version 0.1.0 is BENCH MODE only.

The onboard Pico LED represents the future screen-enable output. Ignition state is simulated in software. No raw automotive voltage may be connected directly to RP2350 GPIO.

Current proven bench behavior:

- simulated ignition OFF -> LED/screen output OFF
- simulated ignition ON -> LED/screen output ON
- output changes only when ignition state changes

## Safety / architecture rules

- The Pico does not intentionally kill an already-running engine.
- The Pico must request graceful Linux shutdown before removing Pi power.
- Raw 12-14.5 V vehicle signals require verified conditioning/protection before Pico GPIO/ADC.
- GPIO assignments and battery thresholds remain unfrozen until the power hardware is bench tested.
- Screen and Pi power outputs will drive appropriate control hardware; they will not power those loads directly from Pico GPIO.

## Bench use

Copy `config.py` and `main.py` to the Pico filesystem. `main.py` runs automatically when the Pico boots.

For the current no-jumper-wire test, change:

`supervisor.set_bench_ignition(False)`

to:

`supervisor.set_bench_ignition(True)`

The onboard LED should follow the simulated ignition state.
