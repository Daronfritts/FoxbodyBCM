"""
hardware.py

Foxbody BCM Hardware Abstraction Layer.

Feature modules use symbolic names only. Raw Raspberry Pi pins, RS485
registers, MOSFET channels and H-bridge terminals are translated below this
layer after the hardware is bench verified.
"""

from logger import logger
from gpio_manager import gpio
from motor_manager import motors, MotorDirection


DIGITAL_INPUTS = (
    "driver_door", "passenger_door", "hatch_ajar", "hood_open",
    "brake", "clutch", "parking_brake", "reverse", "start_button",
    "defrost_button", "hatch_button", "lock_button", "unlock_button",
    "driver_window_up", "driver_window_down", "passenger_window_up",
    "passenger_window_down", "wiper_mist", "wiper_intermittent",
    "wiper_low", "wiper_high", "washer", "headlight_switch",
    "high_beam_switch", "left_turn", "right_turn", "hazard",
    "ignition_run_sense", "wiper_park", "fuel_door_button",
    "spare_30", "spare_31",
)

MOSFET_OUTPUTS = (
    "parking_lamps", "headlamp_enable", "high_beam_enable",
    "left_turn_output", "right_turn_output", "horn_control",
    "rear_defrost_control", "hatch_release", "fuel_door_release",
    "aux_10", "aux_11", "aux_12", "aux_13",
    "wiper_low_control", "wiper_high_control", "washer_control",
)

REVERSIBLE_MOTORS = (
    "driver_window", "passenger_window", "driver_lock", "passenger_lock",
)


class Hardware:
    def __init__(self):
        self.initialized = False

    def initialize(self):
        logger.info("Hardware | Registering digital inputs")
        for name in DIGITAL_INPUTS:
            gpio.register_input(name)

        logger.info("Hardware | Registering MOSFET/control outputs")
        for name in MOSFET_OUTPUTS:
            gpio.register_output(name)

        logger.info("Hardware | Registering reversible motors")
        for name in REVERSIBLE_MOTORS:
            motors.register_motor(name)

        self.initialized = True
        logger.info("Hardware | Initialization Complete")
        return True

    # ---------- digital inputs ----------

    def read(self, name):
        return gpio.read(name)

    # Convenience methods used by safety-critical modules.
    def driver_door_open(self):
        return self.read("driver_door")

    def passenger_door_open(self):
        return self.read("passenger_door")

    def brake_pressed(self):
        return self.read("brake")

    def clutch_pressed(self):
        return self.read("clutch")

    # ---------- one-direction outputs ----------

    def output(self, name, state):
        gpio.write(name, bool(state))

    def parking_lights(self, state):
        self.output("parking_lamps", state)

    def headlights(self, state):
        self.output("headlamp_enable", state)

    def high_beams(self, state):
        self.output("high_beam_enable", state)

    def horn(self, state):
        self.output("horn_control", state)

    def rear_defrost(self, state):
        self.output("rear_defrost_control", state)

    # ---------- reversible motors ----------

    def motor_forward(self, name, duty=1.0):
        motors.command(name, MotorDirection.FORWARD, duty)

    def motor_reverse(self, name, duty=1.0):
        motors.command(name, MotorDirection.REVERSE, duty)

    def motor_stop(self, name, brake=False):
        motors.stop(name, brake=brake)

    def stop_all_motors(self):
        motors.stop_all()


hardware = Hardware()
