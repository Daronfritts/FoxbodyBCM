# FoxbodyBCM Hardware Photo Index

Status: PHOTO IDENTIFICATION STARTED
Last updated: 2026-09-20

This file is the working index for the physical BCM boards and devices. It links each visible label or board function to the planned project name used in the wiring docs and code.

Note: The original board photos were reviewed from the ChatGPT workspace upload batch on 2026-09-20. Binary JPEG assets are not yet stored in this repository. When photos are added to the repo, place them under `assets/hardware/` using the target filenames below.

## Board Labels From Current Photo Batch

| Photo file | Visible label / marking | Project name | What it is | Main use | Raw car wiring safe? | Notes |
|---|---|---|---|---|---|---|
| `28F51B02-42D8-4CAD-9CE8-A29F09339BA0.jpeg` | `RLY-01`, 8 blue relays | Relay Board | 8-channel 12V relay module | Loads that need relay isolation/current handling | Control side only | Use for relay-driven loads after coil/current verification. |
| `1323EA86-DC5B-4509-AD64-3A335D6D5F96.jpeg` | `OUT-01` | Output Board | 16-channel output board, likely MOSFET output module | Main positive-switched BCM outputs | Yes, within verified current limit | Verify exact model/current rating before assigning high-current loads. |
| `3147AF87-2E7C-4456-A876-636A5295AD77.jpeg` | `PICO-02` | Pico 2 Board | Raspberry Pi Pico on screw-terminal carrier | Local logic/control node | No | Logic-level only unless protected by interface hardware. |
| `AB2AAD6E-6741-4E3F-ADE5-ACB0EFC80712.jpeg` | `PICO STWH` / Pico 2 W | Steering Wheel Pico | Raspberry Pi Pico W on screw-terminal carrier | Steering wheel buttons/wireless control | No | Intended for button inputs and wireless BCM communication. |
| `FCCB702C-E989-48FD-B82A-7CC0CF20D41B.jpeg` | `DRV-02` | Window Driver / Motor Driver | High-current H-bridge style driver board | Power windows or other reversible motor loads | Motor side only | Verify terminal labels and current rating before final use. |
| `396E4358-23B0-4A38-99D3-8D4E0E9EEBAA.jpeg` | `DRV-01` | Small Driver Board | Small dual-driver/MOSFET style board | Small loads or test driver functions | Not for unknown raw loads yet | Needs pinout/current verification before assignment. |
| `EE9701F4-DA52-4E72-A276-87871BEB9CED.jpeg` | `IN-01`, 24DIB32 NPN marking | Input Board | 32-channel isolated digital input board | Main factory switch/input interface | Yes, if wired per board input requirements | Primary input board for doors, brake, clutch, wipers, lights, etc. |
| `BEF4A237-4DDF-4F53-91FD-72F263FA2ECA.jpeg` | `LIN-01` | LIN Adapter | TTL-LIN transceiver board | LIN bus experiments/devices | No | Use only for LIN communication wiring, not general switches/loads. |
| `046B1471-A212-4A91-A636-493D66CB9498.jpeg` | `PICO-01` | Pico 1 Board | Raspberry Pi Pico on screw-terminal carrier | Local logic/control node | No | Logic-level only unless protected by interface hardware. |
| `8292275D-CCA2-42F4-8602-B21C79023A3E.jpeg` | `SEE... SG-IO-E017-A`, `VCC/GND/SDA/SCL/INTA/INTB`, `PA0-PA7`, `PB0-PB7` | Logic I/O Expander | MCP23017-style I2C GPIO expander board | Extra low-voltage GPIO | No | Not 12V safe. Use only behind conditioning/interface circuits. |

## Recommended Target Photo Filenames

Use these names when the actual images are committed to `assets/hardware/`:

| Current upload | Target repo filename |
|---|---|
| `28F51B02-42D8-4CAD-9CE8-A29F09339BA0.jpeg` | `assets/hardware/rly-01_8ch_relay_board.jpg` |
| `1323EA86-DC5B-4509-AD64-3A335D6D5F96.jpeg` | `assets/hardware/out-01_16ch_output_board.jpg` |
| `3147AF87-2E7C-4456-A876-636A5295AD77.jpeg` | `assets/hardware/pico-02_terminal_board.jpg` |
| `AB2AAD6E-6741-4E3F-ADE5-ACB0EFC80712.jpeg` | `assets/hardware/pico-steering-wheel_terminal_board.jpg` |
| `FCCB702C-E989-48FD-B82A-7CC0CF20D41B.jpeg` | `assets/hardware/drv-02_motor_driver.jpg` |
| `396E4358-23B0-4A38-99D3-8D4E0E9EEBAA.jpeg` | `assets/hardware/drv-01_small_driver_board.jpg` |
| `EE9701F4-DA52-4E72-A276-87871BEB9CED.jpeg` | `assets/hardware/in-01_32ch_input_board.jpg` |
| `BEF4A237-4DDF-4F53-91FD-72F263FA2ECA.jpeg` | `assets/hardware/lin-01_ttl_lin_adapter.jpg` |
| `046B1471-A212-4A91-A636-493D66CB9498.jpeg` | `assets/hardware/pico-01_terminal_board.jpg` |
| `8292275D-CCA2-42F4-8602-B21C79023A3E.jpeg` | `assets/hardware/mcp23017_logic_io_expander.jpg` |

## Working Rules

- Anything connected directly to factory 12V wiring must be isolated, protected, or designed for automotive 12V input.
- Pico boards and raw MCP23017 boards are logic-level devices only.
- Output boards and driver boards need final current limits verified before powering real vehicle loads.
- Board labels used in wiring docs should match the physical labels: `IN-01`, `OUT-01`, `RLY-01`, `DRV-01`, `DRV-02`, `LIN-01`, `PICO-01`, `PICO-02`.
