# Pico firmware — staged bench release

Updated 2026-10-21. These are MicroPython programs, separate from the Raspberry Pi
Linux application at the repository root. They implement the October drawing pin
assignments, not the earlier Pico 2 input/output layout. Nothing has been flashed
or electrically tested by this change. No vehicle installation release is implied.

## Install through Thonny, one Pico at a time

1. Before replacing anything, read and save that Pico's current `main.py` and
   `config.py` to your computer. Label the backup with the physical Pico number.
2. Disconnect all vehicle loads and unverified interfaces. Use USB and ground
   jumpers only for the first test. Do not connect vehicle 12 V to a Pico pin.
3. On Pico 1 copy `pico1/main.py`, `pico1/config.py`, and both files from `common/`
   to the Pico root (`main.py`, `config.py`, `control.py`, `link.py`).
4. On Pico 2 copy `pico2/main.py`, `pico2/config.py`, `pico2/outputs.py`, and both
   `common/` files to its root. Never copy the Pi's root-level `main.py/config.py`.
5. Leave configuration defaults unchanged for the first tests. Restart, inspect
   the Thonny console, then test the ground-jumper inputs below.
6. Steering-wheel Pico is untouched; its current source has not been supplied.

The onboard LED uses `Pin("LED")` for the photographed wireless Picos. Confirm
that the MicroPython build matches the exact board. No watchdog is enabled in
this bench release; resetting an ignition controller must first have a verified
hardware fallback so it cannot drop a running engine.

## What actually works in this release

| Controller | Implemented | Electrical outputs with shipped defaults |
|---|---|---|
| Pico 1 | Debounced local inputs; simulated-battery supervisor; status UART | LED only; GP3/5 held LOW, relay GPIOs held HIGH/off |
| Pico 2 | Debounced local inputs; manual parking/head/high/fog requests; continuous turn/hazard flashing; status UART; MCP driver | MCP untouched; no motor GPIO drive |

Pico 1 keeps the original ignition-first behavior. Its simulated battery is 12.6 V;
changing `BENCH_MODE` to False reports battery unknown rather than pretending a
real ADC exists. The battery thresholds are temporary bench values. Pi alive is
telemetry only: LOW does not prove Linux halted. Shutdown grace expiry reports a
timeout and never authorizes power removal. GP3 and GP5 have separate enable flags,
both False until their receiving circuits are verified.

Pico 2 reads its own light requests regardless of Pi or Pico 1 communication.
GP5 is treated as high/flash request: high beam can be requested without headlamps;
low/high commands are mutually exclusive in this draft logic. Headlamps imply
parking lamps. Fog command is independent of head and high beams. Hazards override
turn requests. Two opposite turn requests without hazards produce neither. The
500 ms on/500 ms off timing is a bench default, not a validated vehicle flasher.
Automatic lights, three-flash lane change, follow-me-home and alarm overrides are
not implemented yet.

Pico 1 GP17 carries the separate parking-only request to Pico 2 by UART. If Pico 1
status expires after 1.5 s that remote request becomes false; a local headlight
request still keeps parking lamps requested. This is a documented bench behavior,
not a fault-tolerant vehicle lighting fallback. A Pico 1 failure must be addressed
in the wiring/fallback design before conversion.

## Pin map — GP numbers, not physical header positions

| Function | Pico 1 GP | Pico 2 GP |
|---|---:|---:|
| UART TX / RX | 0 / 1 | 0 / 1 |
| Ignition / shutdown request / Pi alive | 2 / 3 / 4 | — |
| Screen enable | 5 | — |
| ACC / RUN / START / defrost / blower relay commands | 6 / 7 / 8 / 9 / 10 | — |
| Start button / clutch / brake | 11 / 12 / 13 | — |
| RPM reserved / RUN feedback | 14 / 15 | — |
| Pi disconnect reserved / parking request | 16 / 17 | — |
| Battery ADC reserved | 26 | — |
| I/O Board SDA / SCL | — | 2 / 3 |
| Head / high-flash request | — | 4 / 5 |
| Left / right / hazard request | — | 6 / 7 / 8 |
| Wiper low / high / washer request | — | 9 / 10 / 11 |
| Window uppercase A / B / P, driver proposed | — | 12 / 13 / 14 |
| Window lowercase a / b / P, passenger proposed | — | 15 / 16 / 17 |
| Lock D0 / D1 / D2 / D3, proposed | — | 18 / 19 / 26 / 27 |
| Wiper park / intermittent / fog request | — | 20 / 21 / 22 |

UART: P1 GP0 → P2 GP1; P2 GP0 → P1 GP1; common logic ground;
115200 baud, UART0, 8N1. Bounded newline JSON carries version 1, source role,
boolean local inputs and diagnostic state every 250 ms. Invalid frames do not
refresh peer age. It is not a remote actuator command protocol and provides no
security authorization. USB is for programming/diagnostics; a Pi bridge is not
implemented here.

## I/O Board and Output Interfaces

Pico 2 uses I2C1 on GP2/GP3, 100 kHz. Address `0x20` is a configurable candidate,
not a measured address. Power the I/O Board logic at 3.3 V as documented; confirm
address straps and pull-up voltage. MCP A0–A7 → Output Interface 1 inputs 1B–8B →
collectors 1C–8C → Output Board X1–X8; MCP B0–B7 similarly via Interface 2 → X9–X16.
ULN interface GND → logic ground; ULN COM unused for these noninductive inputs.
Output Board input COM is the separately documented +5 V input common, not ULN
COM. The owned board photo shows NPN/5 V input selection; old documents claiming
12 V *control inputs* are superseded. Load VCC is a different circuit.

MCP HIGH drives the ULN sinking channel and is expected to request an output ON;
verify that end-to-end before enabling. The driver establishes BANK=0 and clears
output latches before setting output direction. It does not guarantee a glitch-free
power-up or independent Pico reset: MCP latches can survive a Pico reset, and a
broken I2C bus can leave outputs ON. Verify MCP RESET/power sequencing and hardware
output inhibit before vehicle use. On I2C error this release latches a fault,
attempts all-off, and stops; it cannot confirm all-off when the bus is broken.

To test a single verified light channel with a test lamp or relay coil only:
confirm MCP address, then set `ENABLE_MCP_OUTPUTS=True` and add just its symbolic
name to `VERIFIED_OUTPUTS`, for example `("fog_lamp_control",)`. Only the six
implemented lighting names are accepted. All other MCP channels remain off.
Never enable an unverified channel to see what happens.

## Bench checks

- Pico 1 GP2 grounded → RUNNING / onboard LED on; open → PARKED / LED off.
- Ground GP17 on Pico 1 with UART connected: Pico 2 prints parking_lamps True.
- Ground GP4 on Pico 2: prints headlamp_enable and parking_lamps True.
- Ground GP5: high_beam_enable True, low beam False.
- Ground GP22: fog True regardless of GP4/GP5.
- Ground GP6 or GP7: appropriate side flashes; GP8 flashes both.
- Unplug the Pi while Picos remain independently USB-powered: local Pico 2
  requests continue. Removing a shared USB power source is a power loss, not
  merely a Pi software reboot; the final always-on supply topology is unresolved.
- Disconnect UART: Pico 2 reports peer offline, local switches still work.
- Use no vehicle loads for simulated low/critical battery and reset/fault tests.

Host verification: `python -m unittest discover -s tests -p 'test_pico_firmware.py' -v`.
Host tests check logic and fake buses, not MicroPython execution or real wiring.

## Features deliberately not enabled / remaining design work

- ACC/RUN/START/defrost/blower control: pins initialized off only. Start
  authorization, valid independent engine-running feedback, clutch hardware
  interlock, crank timeout, button intent, intentional stop, retained accessories,
  emergency sequence and engine-preserving reset behavior still require design
  and tests. Do not replace the car's ignition path with this bench code.
- Battery ADC calibration/protection, screen driver, Pi-side GPIO numbers,
  Linux shutdown listener/alive behavior and physical disconnect circuit.
- Windows/locks: pins reserved and left high impedance, no direction/PWM output.
  Verify supply limits, header supply direction, truth tables, stop states,
  motor terminals, reversal dead time, current sensing and timeouts before use.
  The lock board's stated 14 V supply ceiling is not approval for raw vehicle power.
- Wiper outputs/washer: inhibited until park/braking/relay topology is verified;
  no generic low/high motor assumptions. Horn awaits steering-wheel source and
  ground-trigger relay interface. Hatch/fuel releases await pulse/current checks.
- RS485 Input Board remains Pi-owned and is not read by either program. Existing
  X assignments are preserved, including X28 wiper park in GitHub; the conflicting
  paper X28 label must be resolved before wiring. Window/lock/release requests
  have no local Pico path yet. Essential inputs cannot depend exclusively on Pi.
- Brake lamps remain factory hardwired. Pico brake pins are protected monitors;
  neither program switches brake-lamp power. Cooling remains ECU/fan-controller
  work and is not allocated a Pico output by this release.

Do not call this complete BCM firmware. It is a versioned, testable bench starting
point with explicit inhibited features instead of guessed vehicle behavior.
