"""
modules/door_locks.py

Door lock controller for the dual-channel Lock Driver.

No RPi.GPIO access and no blocking sleeps are allowed here. Each lock
actuator is a two-wire reversible motor on one H-bridge channel.
"""

from time import monotonic

from hardware import hardware
from logger import logger


class DoorLocks:
    LOCK_PULSE_S = 0.40
    REVERSE_DEADTIME_S = 0.075

    def __init__(self):
        self.locked = False
        self._active_until = 0.0
        self._pending = None
        self._last_lock_button = False
        self._last_unlock_button = False

    def lock(self):
        self._request("lock")

    def unlock(self):
        self._request("unlock")

    def _request(self, action):
        if action not in ("lock", "unlock"):
            raise ValueError(action)

        # Always stop before reversing direction. The small delay is handled
        # non-blocking in update().
        hardware.motor_stop("driver_lock")
        hardware.motor_stop("passenger_lock")
        self._pending = (action, monotonic() + self.REVERSE_DEADTIME_S)
        logger.info("LOCKS | request=%s", action)

    def _start(self, action, now):
        # Polarity is arbitrary until bench verification; changing these two
        # lines is all that is required if physical lock/unlock direction is
        # opposite after wiring.
        if action == "lock":
            hardware.motor_forward("driver_lock")
            hardware.motor_forward("passenger_lock")
        else:
            hardware.motor_reverse("driver_lock")
            hardware.motor_reverse("passenger_lock")

        self._active_until = now + self.LOCK_PULSE_S
        self._pending = None
        self.locked = action == "lock"
        logger.info("LOCKS | %s pulse started", action)

    def _stop(self):
        hardware.motor_stop("driver_lock")
        hardware.motor_stop("passenger_lock")
        self._active_until = 0.0

    def update(self):
        now = monotonic()

        lock_button = hardware.read("lock_button")
        unlock_button = hardware.read("unlock_button")

        if lock_button and not self._last_lock_button:
            self.lock()
        if unlock_button and not self._last_unlock_button:
            self.unlock()

        self._last_lock_button = lock_button
        self._last_unlock_button = unlock_button

        if self._pending and now >= self._pending[1]:
            self._start(self._pending[0], now)

        if self._active_until and now >= self._active_until:
            self._stop()

    def shutdown(self):
        self._pending = None
        self._stop()


door_locks = DoorLocks()
