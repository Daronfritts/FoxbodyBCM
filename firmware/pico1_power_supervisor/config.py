# FoxbodyBCM Pico 1 - Power Supervisor configuration
# Raspberry Pi Pico 2 / RP2350

PICO_ROLE = "POWER_SUPERVISOR"
FIRMWARE_VERSION = "0.3.0"

# Bench hardware mode uses a jumper from GP2 to GND to simulate KEY ON.
# GP2 uses the RP2350 internal pull-up:
#   GP2 grounded  = KEY ON
#   GP2 open      = KEY OFF
BENCH_MODE = True
IGNITION_SENSE_PIN = 2
IGNITION_ACTIVE_LOW = True

# During bench testing the Pico onboard LED represents SCREEN_ENABLE.
SCREEN_OUTPUT = "LED"

# Simulated battery input for state-machine testing only.
# This will be replaced by a protected ADC input later.
SIMULATED_BATTERY_VOLTS = 12.6

# Temporary bench thresholds used only to test logic.
# Final vehicle thresholds will be chosen after the real power hardware
# and battery behavior are measured under load.
LOW_BATTERY_VOLTS = 12.0
CRITICAL_BATTERY_VOLTS = 11.5

# Future hardware assignments. Do not connect raw vehicle 12 V directly
# to RP2350 GPIO; the vehicle ignition signal must use a protected interface.
PI_SHUTDOWN_REQUEST_PIN = None
PI_POWER_CONTROL_PIN = None
PI_ALIVE_PIN = None
BATTERY_ADC_PIN = None

SHUTDOWN_GRACE_SECONDS = 30
