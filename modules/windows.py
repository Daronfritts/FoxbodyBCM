"""
modules/windows.py

Power-window controller for the dual high-current Window Driver.

This module owns manual window commands and exposes safe request methods for
rain-close, lock-close and hot-car vent logic. Current sensing/end-stop logic
will plug into the same state machine when the analog board is finalized.
"""

from dataclasses import dataclass
from time import monotonic

from hardware import hardware
from logger import logger


@dataclass
class WindowState:
    direction: str = "stop"
    started_at: float = 0.0
    requested_until: float = 0.0


class Windows:
    MAX_RUN_S = 8.0
    REVERSE_DEADTIME_S = 0.10
    VENT_TIME_S = 0.80  # calibration value; tune to ~15% opening on car

    def __init__(self):
        self.states = {
            "driver": WindowState(),
            "passenger": WindowState(),
        }
        self._pending = {"driver": None, "passenger": None}

    @staticmethod
    def _motor(side):
        return f"{side}_window"

    def _stop(self, side, brake=False):
        hardware.motor_stop(self._motor(side), brake=brake)
        self.states[side] = WindowState()

    def _start(self, side, direction, duration=None):
        now = monotonic()
        if direction == "up":
            hardware.motor_forward(self._motor(side))
        elif direction == "down":
            hardware.motor_reverse(self._motor(side))
        else:
            self._stop(side)
            return

        self.states[side] = WindowState(
            direction=direction,
            started_at=now,
            requested_until=(now + duration) if duration else 0.0,
        )
        self._pending[side] = None
        logger.info("WINDOWS | %s -> %s", side, direction)

    def command(self, side, direction, duration=None):
        if side not in self.states:
            raise ValueError(f"Unknown window side: {side}")
        if direction not in ("up", "down", "stop"):
            raise ValueError(f"Unknown direction: {direction}")

        if direction == "stop":
            self._pending[side] = None
            self._stop(side)
            return

        current = self.states[side].direction
        if current not in ("stop", direction):
            # Non-blocking reversal interlock.
            self._stop(side)
            self._pending[side] = (
                direction,
                duration,
                monotonic() + self.REVERSE_DEADTIME_S,
            )
            return

        self._start(side, direction, duration)

    def close_all(self):
        """Used by lock/rain logic. Current sensing will stop at end travel."""
        self.command("driver", "up")
        self.command("passenger", "up")

    def vent_all(self):
        """Hot-car feature: approximate 15% opening; calibrate duration in car."""
        self.command("driver", "down", self.VENT_TIME_S)
        self.command("passenger", "down", self.VENT_TIME_S)

    def stop_all(self):
        self.command("driver", "stop")
        self.command("passenger", "stop")

    def _manual_inputs(self):
        return {
            "driver": (
                hardware.read("driver_window_up"),
                hardware.read("driver_window_down"),
            ),
            "passenger": (
                hardware.read("passenger_window_up"),
                hardware.read("passenger_window_down"),
            ),
        }

    def update(self):
        now = monotonic()

        # Physical switch input always has immediate authority.
        for side, (up, down) in self._manual_inputs().items():
            if up and not down:
                if self.states[side].direction != "up":
                    self.command(side, "up")
            elif down and not up:
                if self.states[side].direction != "down":
                    self.command(side, "down")
            elif up and down:
                self.command(side, "stop")
            elif self.states[side].direction in ("up", "down") and not self.states[side].requested_until:
                # A manual hold was released.
                self.command(side, "stop")

        for side in self.states:
            pending = self._pending[side]
            if pending and now >= pending[2]:
                self._start(side, pending[0], pending[1])

            state = self.states[side]
            if state.direction == "stop":
                continue

            if state.requested_until and now >= state.requested_until:
                self._stop(side, brake=True)
                continue

            if now - state.started_at >= self.MAX_RUN_S:
                logger.warning("WINDOWS | %s run timeout; stopping", side)
                self._stop(side, brake=True)

        # TODO(ANALOG): stop/anti-pinch based on measured motor current.

    def shutdown(self):
        self.stop_all()


windows = Windows()
