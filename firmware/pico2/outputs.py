"""MCP23017 BANK=0, ULN2803A sinking interface; MCP HIGH commands load ON.
Requires dedicated expander ownership and verified RESET/power-on wiring.
"""

class Outputs:
    def __init__(self, i2c, address, channels, enabled_names):
        self.i2c, self.address, self.channels = i2c, address, channels
        self.enabled_names = set(enabled_names)
        self.fault = False
        if not 0x20 <= address <= 0x27:
            raise ValueError("MCP address outside range")
        # Recover BANK=0 from either BANK layout without writing output registers.
        self.write(0x05, b"\x00")
        self.write(0x0a, b"\x00")
        # Clear latches BEFORE changing pins from inputs to outputs.
        self.write(0x14, b"\x00\x00")
        self.write(0x00, b"\x00\x00")

    def write(self, register, data):
        self.i2c.writeto_mem(self.address, register, data)

    def apply(self, desired):
        if self.fault:
            raise OSError("Output fault latched; reset/retest required")
        mask = 0
        for name in self.enabled_names:
            if desired.get(name, False):
                mask |= 1 << (self.channels[name] - 1)
        try:
            self.write(0x14, bytes((mask & 255, (mask >> 8) & 255)))
        except OSError:
            self.fault = True
            self.off()
            raise

    def off(self):
        # Best effort only; bus failure can leave previously latched outputs ON.
        try:
            self.write(0x14, b"\x00\x00")
            return True
        except OSError:
            return False
