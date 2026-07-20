"""
hardware.py

Foxbody BCM Hardware Abstraction Layer
"""

from logger import logger
from gpio_manager import gpio


class Hardware:

    def __init__(self):

        self.initialized = False

    def initialize(self):

        logger.info("Hardware | Registering Inputs")

        #
        # Inputs
        #

        gpio.register_input("driver_door")
        gpio.register_input("passenger_door")
        gpio.register_input("brake")
        gpio.register_input("clutch")
        gpio.register_input("headlight_switch")
        gpio.register_input("rain_sensor")

        logger.info("Hardware | Registering Outputs")

        #
        # Outputs
        #

        gpio.register_output("parking_lights")
        gpio.register_output("headlights")
        gpio.register_output("starter")
        gpio.register_output("ignition")
        gpio.register_output("accessory")

        self.initialized = True

        logger.info("Hardware | Initialization Complete")

        return True

    #
    # Inputs
    #

    def driver_door_open(self):
        return gpio.read("driver_door")

    def brake_pressed(self):
        return gpio.read("brake")

    #
    # Outputs
    #

    def parking_lights(self, state):
        gpio.write("parking_lights", state)

    def headlights(self, state):
        gpio.write("headlights", state)

    def starter(self, state):
        gpio.write("starter", state)

    def ignition(self, state):
        gpio.write("ignition", state)

    def accessory(self, state):
        gpio.write("accessory", state)


hardware = Hardware()
