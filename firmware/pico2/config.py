"""Pico 2 Body Controls: proposed drawing map; BENCH RELEASE ONLY."""
DEVICE_NAME = "PICO2_BCM_IO"
FIRMWARE_VERSION = "0.3.0-bench"
INPUT_ACTIVE_LOW = True  # Bench jumpers, not permission to connect raw vehicle wires.
DEBOUNCE_MS = 30
UART_TX_PIN = 0
UART_RX_PIN = 1
UART_BAUD = 115200
I2C_SDA_PIN = 2
I2C_SCL_PIN = 3
MCP_ADDRESS = 0x20  # Confirm address straps with scan before enabling.
ENABLE_MCP_OUTPUTS = False
# Enable one channel at a time only after interface and relay/lamp bench test.
# Names accepted here are restricted in main.py to the six implemented lights.
VERIFIED_OUTPUTS = ()
INPUT_PINS = {
    "headlight_switch": 4, "high_beam_switch": 5, "left_turn": 6,
    "right_turn": 7, "hazard": 8, "wiper_low": 9,
    "wiper_high": 10, "washer": 11, "wiper_park": 20,
    "wiper_intermittent": 21, "fog_switch": 22,
}
WINDOW_PINS = {"driver_a": 12, "driver_b": 13, "driver_pwm": 14,
               "passenger_a": 15, "passenger_b": 16, "passenger_pwm": 17}
LOCK_PINS = {"driver_d0": 18, "driver_d1": 19,
             "passenger_d2": 26, "passenger_d3": 27}
# Reserved motor GPIOs stay high impedance until truth tables and supplies verified.
SPARE_ANALOG_PIN = 28
LED_PIN = "LED"
OUTPUT_CHANNELS = {
    "parking_lamps": 1, "headlamp_enable": 2, "high_beam_enable": 3,
    "left_turn_output": 4, "right_turn_output": 5, "horn_control": 6,
    "aux_07": 7, "hatch_release": 8, "fuel_door_release": 9,
    "fog_lamp_control": 10, "aux_11": 11, "aux_12": 12,
    "aux_13": 13, "wiper_low_control": 14,
    "wiper_high_control": 15, "washer_control": 16,
}
