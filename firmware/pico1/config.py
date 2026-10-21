"""Pico 1 Power/Ignition: proposed drawing map; BENCH RELEASE ONLY."""
PICO_ROLE = "POWER_SUPERVISOR"
FIRMWARE_VERSION = "0.4.0-bench"
BENCH_MODE = True
INPUT_ACTIVE_LOW = True  # Bench jumpers only; verify every protected interface.
DEBOUNCE_MS = 30
UART_TX_PIN = 0
UART_RX_PIN = 1
UART_BAUD = 115200
INPUT_PINS = {
    "ignition": 2, "pi_alive": 4, "start_button": 11,
    "clutch": 12, "brake": 13, "run_feedback": 15,
    "parking_switch": 17,
}
PI_SHUTDOWN_REQUEST_PIN = 3
SCREEN_ENABLE_PIN = 5
RELAY_PINS = {"acc": 6, "run": 7, "start": 8, "rear_defrost": 9, "blower": 10}
RELAY_ACTIVE_LOW = True
# No vehicle power-state controller is enabled in this bench release.
# Hardware pull-ups must keep active-low relay inputs OFF during reset/boot.
ENGINE_RPM_PIN = 14  # Reserved: protected signal/decoding not designed.
PI_POWER_CONTROL_PIN = 16  # Reserved: disconnect hardware/confirmation not verified.
BATTERY_ADC_PIN = 26  # Reserved: protected divider/calibration not verified.
SIMULATED_BATTERY_VOLTS = 12.6
LOW_BATTERY_VOLTS = 12.0
CRITICAL_BATTERY_VOLTS = 11.5
SHUTDOWN_GRACE_SECONDS = 30
# Keep GP3 disconnected from Pi until Pi-side GPIO/protocol is documented.
ENABLE_PI_SHUTDOWN_SIGNAL = False
ENABLE_SCREEN_SIGNAL = False
LED_PIN = "LED"
