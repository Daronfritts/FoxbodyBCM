from machine import Pin
from time import sleep

from config import (
    BENCH_MODE,
    PICO_ROLE,
    FIRMWARE_VERSION,
    SCREEN_OUTPUT,
    IGNITION_SENSE_PIN,
    IGNITION_ACTIVE_LOW,
)


class PowerSupervisor:
    def __init__(self):
        # Onboard LED represents the future screen-enable output on the bench.
        self.screen = Pin(SCREEN_OUTPUT, Pin.OUT)

        # Tested bench input: GP2 with internal pull-up.
        self.ignition_pin = Pin(IGNITION_SENSE_PIN, Pin.IN, Pin.PULL_UP)

        self.ignition = False
        self.last_ignition = None
        self.shutdown_requested = False

        # Fail-safe startup state.
        self.screen.off()

    def read_inputs(self):
        raw_ignition = self.ignition_pin.value()

        if IGNITION_ACTIVE_LOW:
            self.ignition = raw_ignition == 0
        else:
            self.ignition = raw_ignition == 1

    def update_power_state(self):
        # Only act when ignition state changes.
        if self.ignition == self.last_ignition:
            return

        if self.ignition:
            self.screen.on()
            self.shutdown_requested = False
            print("KEY ON -> SCREEN ON")
        else:
            self.screen.off()
            print("KEY OFF -> SCREEN OFF / PI REMAINS ON")

        self.last_ignition = self.ignition

    def run(self):
        print("FOXBODY BCM")
        print("PICO 1 - " + PICO_ROLE)
        print("FIRMWARE " + FIRMWARE_VERSION)
        print("BENCH HARDWARE MODE" if BENCH_MODE else "VEHICLE MODE")
        print("IGNITION INPUT: GP" + str(IGNITION_SENSE_PIN))
        print("SYSTEM READY")

        while True:
            self.read_inputs()
            self.update_power_state()
            sleep(0.05)


supervisor = PowerSupervisor()
supervisor.run()
