# FoxbodyBCM Pico 1 - Power Supervisor configuration
# Raspberry Pi Pico 2 / RP2350

PICO_ROLE = "POWER_SUPERVISOR"
FIRMWARE_VERSION = "0.2.0"

# Bench hardware mode uses a jumper from GP2 to GND to simulate KEY ON.
# GP2 uses the RP2350 internal pull-up:
#   GP2 grounded  = KEY ON
#   GP2 open      = KEY OFF
BENCH_MODE = True
IGNITION_SENSE_PIN = 2
IGNITION_ACTIVE_LOW = True

# During bench testing the Pico onboard LED represents SCREEN_ENABLE.
SCREEN_OUTPUT = "LED"

# Future hardware assignments. Do not connect raw vehicle 12 V directly
# to RP2350 GPIO; the vehicle ignition signal must use a protected interface.
PI_SHUTDOWN_REQUEST_PIN = None
PI_POWER_CONTROL_PIN = None
PI_ALIVE_PIN = None
BATTERY_ADC_PIN = None

# Battery thresholds remain intentionally unset until the vehicle power
# supply and protected battery-voltage sensing circuit are bench tested.
LOW_BATTERY_VOLTS = None
CRITICAL_BATTERY_VOLTS = None
SHUTDOWN_GRACE_SECONDS = 30
