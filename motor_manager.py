"""
motor_manager.py

Reversible motor abstraction for FoxbodyBCM.

The feature modules do not know whether a motor is driven by GPIO,
an H-bridge module, a future CAN/RS485 driver, or a bench simulator.
Only this layer is allowed to translate a symbolic motor command into
forward/reverse/PWM control.
"""

from dataclasses import dataclass
from enum import Enum
from time import monotonic

from logger import logger


class MotorDirection(str, Enum):
    STOP = "stop"
    FORWARD = "forward"
    REVERSE = "reverse"
    BRAKE = "brake"


@dataclass
class MotorState:
    direction: MotorDirection = MotorDirection.STOP
    duty: float = 0.0
    changed_at: float = 0.0


class MotorManager:
    """Symbolic reversible-motor manager.

    Hardware-specific output writes will be inserted here after the exact
    control terminals are bench-verified. Until then this is safe simulation
    state and lets all BCM feature logic be written/tested now.
    """

    def __init__(self):
        self._motors = {}

    def register_motor(self, name: str):
        if name in self._motors:
            return
        self._motors[name] = MotorState(changed_at=monotonic())
        logger.info("MOTOR | Registered %s", name)

    def command(self, name: str, direction: MotorDirection, duty: float = 1.0):
        if name not in self._motors:
            raise KeyError(f"Unknown motor: {name}")

        duty = max(0.0, min(1.0, float(duty)))
        if direction in (MotorDirection.STOP, MotorDirection.BRAKE):
            duty = 0.0

        state = self._motors[name]
        if state.direction == direction and state.duty == duty:
            return

        state.direction = direction
        state.duty = duty
        state.changed_at = monotonic()
        logger.info("MOTOR | %s -> %s duty=%.2f", name, direction.value, duty)

        # TODO(HARDWARE): translate symbolic command to verified H-bridge pins.
        # Window Driver: dual 9-30V high-current H-bridge, A/B + PA/PB PWM.
        # Lock Driver: dual 5A/9A peak H-bridge, 3.3V-compatible inputs.

    def stop(self, name: str, brake: bool = False):
        self.command(
            name,
            MotorDirection.BRAKE if brake else MotorDirection.STOP,
            0.0,
        )

    def state(self, name: str) -> MotorState:
        if name not in self._motors:
            raise KeyError(f"Unknown motor: {name}")
        return self._motors[name]

    def stop_all(self):
        for name in tuple(self._motors):
            self.stop(name)


motors = MotorManager()
