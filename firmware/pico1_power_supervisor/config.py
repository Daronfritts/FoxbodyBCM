# FoxbodyBCM Pico 1 - Power Supervisor configuration
# Raspberry Pi Pico 2 / RP2350

PICO_ROLE = "POWER_SUPERVISOR"
FIRMWARE_VERSION = "0.1.0"

# Bench mode keeps vehicle inputs simulated until the protected
# automotive input/output hardware is connected and verified.
BENCH_MODE = True

# During bench testing the Pico onboard LED represents SCREEN_ENABLE.
SCREEN_OUTPUT = "LED"

# Physical GPIO assignments are intentionally NOT frozen yet.
# Do not connect raw 12 V vehicle signals directly to RP2350 GPIO.
IGNITION_SENSE_PIN = None
PI_SHUTDOWN_REQUEST_PIN = None
PI_POWER_CONTROL_PIN = None
PI_ALIVE_PIN = None
BATTERY_ADC_PIN = None

# Power-management thresholds are placeholders until the vehicle power
# supply, voltage divider/ADC path, and battery behavior are bench tested.
LOW_BATTERY_VOLTS = None
CRITICAL_BATTERY_VOLTS = None
SHUTDOWN_GRACE_SECONDS = 30
