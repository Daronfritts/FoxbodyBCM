from machine import Pin
from time import sleep

from config import BENCH_MODE, PICO_ROLE, FIRMWARE_VERSION, SCREEN_OUTPUT


class PowerSupervisor:
    def __init__(self):
        self.screen = Pin(SCREEN_OUTPUT, Pin.OUT)
        self.ignition = False
        self.last_ignition = None
        self.shutdown_requested = False

        # Fail-safe boot behavior for bench testing: screen starts off.
        self.screen.off()

    def set_bench_ignition(self, state):
        if not BENCH_MODE:
            return
        self.ignition = bool(state)

    def read_inputs(self):
        if BENCH_MODE:
            return

        # Hardware ignition sense, battery ADC, and Pi status inputs
        # will be implemented only after their conditioning circuits
        # and final GPIO assignments are verified.
        raise NotImplementedError("Vehicle input hardware is not configured")

    def update_power_state(self):
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
        print("BENCH MODE" if BENCH_MODE else "VEHICLE MODE")
        print("SYSTEM READY")

        while True:
            self.read_inputs()
            self.update_power_state()
            sleep(0.05)


supervisor = PowerSupervisor()

# Current bench default. Change to True to simulate KEY ON.
supervisor.set_bench_ignition(False)
supervisor.run()
