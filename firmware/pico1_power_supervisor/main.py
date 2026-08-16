from machine import Pin
from time import sleep

from config import (
    BENCH_MODE,
    PICO_ROLE,
    FIRMWARE_VERSION,
    SCREEN_OUTPUT,
    IGNITION_SENSE_PIN,
    IGNITION_ACTIVE_LOW,
    SIMULATED_BATTERY_VOLTS,
    LOW_BATTERY_VOLTS,
    CRITICAL_BATTERY_VOLTS,
)


class PowerSupervisor:
    def __init__(self):
        self.screen = Pin(SCREEN_OUTPUT, Pin.OUT)
        self.ignition_pin = Pin(IGNITION_SENSE_PIN, Pin.IN, Pin.PULL_UP)

        self.ignition = False
        self.battery_volts = SIMULATED_BATTERY_VOLTS
        self.state = None
        self.shutdown_requested = False

        self.screen.off()

    def read_inputs(self):
        raw_ignition = self.ignition_pin.value()

        if IGNITION_ACTIVE_LOW:
            self.ignition = raw_ignition == 0
        else:
            self.ignition = raw_ignition == 1

        if BENCH_MODE:
            self.battery_volts = SIMULATED_BATTERY_VOLTS

    def determine_state(self):
        if self.ignition:
            return "RUNNING"

        if self.battery_volts <= CRITICAL_BATTERY_VOLTS:
            return "PI_SHUTDOWN"

        if self.battery_volts <= LOW_BATTERY_VOLTS:
            return "LOW_BATTERY"

        return "PARKED"

    def apply_state(self, new_state):
        if new_state == self.state:
            return

        self.state = new_state

        if self.state == "RUNNING":
            self.screen.on()
            self.shutdown_requested = False
            print("STATE: RUNNING")
            print("KEY ON -> SCREEN ON / PI ON")

        elif self.state == "PARKED":
            self.screen.off()
            self.shutdown_requested = False
            print("STATE: PARKED")
            print("KEY OFF -> SCREEN OFF / PI REMAINS ON")

        elif self.state == "LOW_BATTERY":
            self.screen.off()
            self.shutdown_requested = True
            print("STATE: LOW BATTERY")
            print("SCREEN OFF -> REQUEST PI SHUTDOWN")

        elif self.state == "PI_SHUTDOWN":
            self.screen.off()
            self.shutdown_requested = True
            print("STATE: PI SHUTDOWN")
            print("CRITICAL BATTERY -> PI MUST BE OFF")

    def run(self):
        print("FOXBODY BCM")
        print("PICO 1 - " + PICO_ROLE)
        print("FIRMWARE " + FIRMWARE_VERSION)
        print("BENCH HARDWARE MODE" if BENCH_MODE else "VEHICLE MODE")
        print("IGNITION INPUT: GP" + str(IGNITION_SENSE_PIN))
        print("BATTERY: " + str(self.battery_volts) + " V (SIMULATED)")
        print("SYSTEM READY")

        while True:
            self.read_inputs()
            new_state = self.determine_state()
            self.apply_state(new_state)
            sleep(0.05)


supervisor = PowerSupervisor()
supervisor.run()
