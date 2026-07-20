"""
gpio_manager.py

Foxbody BCM GPIO Manager

All Raspberry Pi GPIO access goes through this file.

Nothing else in the BCM should directly use gpiozero,
RPi.GPIO, lgpio, or pigpio.
"""

from logger import logger


class GPIOManager:

    def __init__(self):

        self.inputs = {}
        self.outputs = {}

    def register_input(self, name, pin=None):

        self.inputs[name] = {
            "pin": pin,
            "state": False
        }

        logger.info(f"GPIO | Registered Input: {name}")

    def register_output(self, name, pin=None):

        self.outputs[name] = {
            "pin": pin,
            "state": False
        }

        logger.info(f"GPIO | Registered Output: {name}")

    def read(self, name):

        if name not in self.inputs:
            raise KeyError(f"Unknown input: {name}")

        return self.inputs[name]["state"]

    def write(self, name, state):

        if name not in self.outputs:
            raise KeyError(f"Unknown output: {name}")

        self.outputs[name]["state"] = state

        logger.info(f"GPIO | {name} -> {state}")

    def set_input_state(self, name, state):
        """
        Testing only.
        This will later be replaced with actual GPIO reads.
        """

        if name in self.inputs:
            self.inputs[name]["state"] = state


gpio = GPIOManager()
