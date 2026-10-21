"""Bounded, telemetry-only newline JSON UART. Remote data never actuates motors."""
try:
    import ujson as json
except ImportError:
    import json


class Link:
    def __init__(self, uart, local_role, peer_role, timeout_ms=1500):
        self.uart = uart
        self.local_role, self.peer_role = local_role, peer_role
        self.timeout_ms = timeout_ms
        self.buffer = bytearray()
        self.discard = False
        self.last_rx = None
        self.peer = None
        self.errors = 0

    def poll(self, now):
        data = self.uart.read(256) if self.uart.any() else None
        for byte in data or b"":
            if byte == 10:
                if not self.discard:
                    try:
                        frame = json.loads(self.buffer.decode())
                        if (type(frame) is not dict or frame.get("v") != 1
                                or frame.get("role") != self.peer_role
                                or type(frame.get("inputs")) is not dict
                                or any(type(x) is not bool
                                       for x in frame["inputs"].values())):
                            raise ValueError("invalid telemetry")
                        self.peer, self.last_rx = frame, now
                    except (ValueError, UnicodeError, TypeError):
                        self.errors += 1
                self.buffer = bytearray()
                self.discard = False
            elif not self.discard:
                self.buffer.append(byte)
                if len(self.buffer) > 768:
                    self.buffer = bytearray()
                    self.discard = True
                    self.errors += 1

    def fresh(self, now, diff):
        return self.last_rx is not None and diff(now, self.last_rx) < self.timeout_ms

    def send(self, inputs, state):
        frame = {"v": 1, "role": self.local_role, "inputs": inputs, "state": state}
        payload = (json.dumps(frame) + "\n").encode()
        if len(payload) > 768:
            raise ValueError("telemetry too long")
        self.uart.write(payload)
