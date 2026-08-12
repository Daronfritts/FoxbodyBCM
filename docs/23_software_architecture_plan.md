# FoxbodyBCM Software Architecture Plan

Status: IMPLEMENTATION BASELINE
Last updated: 2026-08-12

## Principle

Vehicle behavior modules must not know raw board pin numbers. Hardware assignments live in the HAL/config layer. Feature modules use symbolic names and state objects.

## Main layers

### 1. Hardware / HAL

Responsibilities:

- Initialize RS485, GPIO expanders, ADCs and smart sensors.
- Map symbolic names to physical channels.
- Read discrete inputs.
- Read analog/sensor values.
- Command MOSFET outputs.
- Command H-bridge direction/speed inputs.
- Command relay control stages.
- Apply low-level safety such as mutually exclusive motor directions.
- Report hardware communication failures.

Planned files:

- hardware.py
- gpio_manager.py
- drivers/rs485_inputs.py
- drivers/opmsd16.py
- drivers/mdd20a.py
- drivers/mdd10a.py
- drivers/adc.py
- drivers/current_sensors.py
- drivers/tpms.py
- drivers/imu.py

### 2. State / event layer

Responsibilities:

- Keep normalized current vehicle state.
- Timestamp state changes.
- Publish events to interested feature modules.
- Debounce switches/sensors.
- Prevent modules from polling hardware independently in inconsistent ways.

Existing event_bus.py is the starting point.

### 3. Feature state machines

Each major vehicle function is a state machine, not a pile of blocking sleeps.

Modules:

- push_start.py
- door_locks.py
- windows.py
- wipers.py
- lighting.py / headlights.py
- interior_lights.py
- cooling.py
- security.py
- bluetooth.py
- horn.py
- diagnostics.py
- touchscreen.py
- fuel.py
- tpms.py

### 4. API / user interface

Expose read-only state and validated commands to FoxbodyDash/UI.

Examples:

- GET vehicle state.
- GET BCM inputs/outputs.
- GET active faults/events.
- POST lock/unlock/window/hatch/light commands.
- POST service/test commands with safety checks.
- POST settings/calibration changes.

The UI must never directly toggle GPIO or board terminals.

## Core system states

Suggested power states:

- OFF
- ACCESSORY
- RUN
- CRANKING
- RETAINED_ACCESSORY
- SHUTDOWN_PENDING
- FAULT

Suggested security states:

- DISARMED
- ARMING
- ARMED
- TRIGGERED
- SERVICE
- AUTH_OVERRIDE_PENDING

Suggested window states per door:

- IDLE
- MANUAL_UP
- MANUAL_DOWN
- AUTO_UP
- AUTO_DOWN
- VENTING
- RAIN_CLOSE
- OBSTRUCTION
- FAULT

Suggested lock states per door:

- UNKNOWN
- LOCKED
- UNLOCKED
- LOCKING
- UNLOCKING
- FAULT

## Timing rules

Do not use long blocking sleeps inside feature logic.

Use monotonic timestamps/deadlines for:

- 3-second emergency-sequence intent delay.
- Retained accessory timeout.
- Follow-me-home lighting.
- Hazard reminder.
- Washer post-wipes and 6-second courtesy wipe.
- Fan after-run.
- Bluetooth proximity hysteresis/dwell.
- Window motor timeout and obstruction reaction.

## Safety interlocks

### Starter

Allow starter only if all required conditions are true, including clutch valid and engine RPM effectively zero. Starter command has a maximum crank timeout.

### H-bridges

- Never command both invalid directions simultaneously.
- Insert a short dead-time when reversing direction.
- Stop on current limit, timeout or loss of control communication.
- Window automatic movement must stop/reverse on configured obstruction behavior.

### Service/Test mode

Potentially dangerous tests require parked/stationary state and explicit service-mode authorization. Starter test should be separately guarded or omitted from ordinary UI service commands.

### Engine-running behavior

Security/BCM logic does not intentionally drop an already-running engine merely because phone authorization is lost or the Pi restarts.

## Fault model

Each fault object should contain:

- code
- severity: INFO/WARNING/CRITICAL
- subsystem
- reason
- first_seen
- last_seen
- active
- snapshot of relevant values

Examples:

- WINDOW_DRIVER_OVERCURRENT_CLOSE
- WINDOW_PASSENGER_NO_CURRENT
- FAN1_COMMANDED_NO_CURRENT
- TPMS_RF_TIMEOUT
- BATTERY_LOW_VOLTAGE
- SENSOR_RAIN_INVALID
- SECURITY_HOOD_TRIGGER
- BCM_INPUT_BOARD_OFFLINE

## Logging

- Circular event log.
- Separate system log and user-visible event history if useful.
- Store configuration changes.
- Store security triggers and failed authorization.
- Store BCM restart reason where detectable.
- Keep critical-event snapshots.

## Configuration

Existing config.py backup rotation remains useful.

Settings should eventually include:

- auto-lock speed
- follow-me-home seconds
- accessory timeout
- cabin hot threshold
- vent percentage
- rain-close enable
- window current thresholds
- wiper timing
- fan thresholds/after-run
- Bluetooth proximity thresholds
- TPMS thresholds
- fuel calibration table
- diagnostic/service settings

## Bench-test strategy

Before car installation, run a simulated/bench HAL where feature modules can execute without real hardware.

Test sequence:

1. Unit-test state machines with synthetic events.
2. Connect input board and verify every X channel live.
3. Connect output board with test lamps/relay coils rather than vehicle loads.
4. Bench-test MDD20A with spare motor/current-limited supply.
5. Bench-test MDD10A with lock actuator/current-limited supply.
6. Add sensors/ADC.
7. Test safety interlocks/failure modes.
8. Install one vehicle subsystem at a time.

## Current code status

The repository already contains the main entry point, configuration manager, hardware abstraction skeleton, GPIO manager, logger, event bus and module placeholders/some early module code. These should be evolved rather than discarded unless a specific architectural conflict is found.
