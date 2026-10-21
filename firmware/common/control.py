"""Portable control logic; no machine imports or vehicle-voltage assumptions."""

class DebouncedInput:
    def __init__(self, delay_ms=30):
        self.delay_ms = delay_ms
        self.candidate = None
        self.since = 0
        self.value = False
        self.ready = False

    def update(self, raw, now, diff):
        raw = bool(raw)
        if raw != self.candidate:
            self.candidate, self.since = raw, now
        if diff(now, self.since) >= self.delay_ms:
            self.value, self.ready = raw, True
        return self.value


class Supervisor:
    """Shutdown request only. A timeout is NOT confirmation of Linux halt."""
    def __init__(self):
        self.state = "PARKED"
        self.low_since = None

    def update(self, ignition, volts, now, diff, low=12.0, critical=11.5,
               grace_ms=30000):
        # Ignition wins: low battery must not drop a running vehicle.
        if ignition:
            self.low_since = None
            self.state = "RUNNING"
        elif volts is None:
            self.low_since = None
            self.state = "BATTERY_UNKNOWN"
        elif volts > low:
            self.low_since = None
            self.state = "PARKED"
        else:
            if self.low_since is None:
                self.low_since = now
            if volts <= critical:
                self.state = "CRITICAL_SHUTDOWN_REQUEST"
            elif diff(now, self.low_since) >= grace_ms:
                self.state = "SHUTDOWN_TIMEOUT"
            else:
                self.state = "LOW_BATTERY"
        return {
            "state": self.state,
            "screen_enable": bool(ignition),
            "shutdown_request": self.state in (
                "LOW_BATTERY", "CRITICAL_SHUTDOWN_REQUEST", "SHUTDOWN_TIMEOUT"),
            "power_removal_allowed": False,
        }


class Lighting:
    """Local manual lights and continuous turns/hazards; no Pi dependency."""
    def __init__(self, half_period_ms=500):
        self.half_period_ms = half_period_ms
        self.last_flash = 0
        self.flashing = False
        self.phase = False

    def update(self, requests, parking, now, diff):
        left = bool(requests.get("left_turn", False))
        right = bool(requests.get("right_turn", False))
        hazard = bool(requests.get("hazard", False))
        # Contradictory left/right requests without hazards produce neither.
        if left and right and not hazard:
            left = right = False
        flashing = left or right or hazard
        if flashing and not self.flashing:
            self.phase, self.last_flash = True, now
        elif flashing and diff(now, self.last_flash) >= self.half_period_ms:
            self.phase = not self.phase
            self.last_flash = now
        elif not flashing:
            self.phase = False
        self.flashing = flashing
        head = bool(requests.get("headlight_switch", False))
        high = bool(requests.get("high_beam_switch", False))
        return {
            "parking_lamps": bool(parking or head),
            "headlamp_enable": head and not high,
            "high_beam_enable": high,
            "left_turn_output": self.phase and (left or hazard),
            "right_turn_output": self.phase and (right or hazard),
            "fog_lamp_control": bool(requests.get("fog_switch", False)),
        }
