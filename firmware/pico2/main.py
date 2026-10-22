from machine import Pin, UART, I2C
import time
import config
from control import DebouncedInput, Lighting
from link import Link
from outputs import Outputs

IMPLEMENTED_LIGHTS = {"parking_lamps", "headlamp_enable", "high_beam_enable",
                      "left_turn_output", "right_turn_output", "fog_lamp_control"}


def run():
    if not set(config.VERIFIED_OUTPUTS).issubset(IMPLEMENTED_LIGHTS):
        raise ValueError("Only implemented lighting channels can be enabled")
    led = Pin(config.LED_PIN, Pin.OUT, value=0)
    pins = {name: Pin(number, Pin.IN, Pin.PULL_UP if config.INPUT_ACTIVE_LOW
                     else Pin.PULL_DOWN) for name, number in config.INPUT_PINS.items()}
    debounce = {name: DebouncedInput(config.DEBOUNCE_MS) for name in pins}
    uart = UART(0, baudrate=config.UART_BAUD, tx=Pin(config.UART_TX_PIN), rx=Pin(config.UART_RX_PIN), timeout=100, rxbuf=2048, txbuf=2048)
    link = Link(uart, "pico2", "pico1")
    lighting = Lighting()
    outputs = None
    last_report = time.ticks_ms()
    print("PICO2", config.FIRMWARE_VERSION, "BENCH_ONLY")
    print("MOTORS / WIPERS / RELEASES / HORN INHIBITED")
    try:
        if config.ENABLE_MCP_OUTPUTS:
            i2c = I2C(1, sda=Pin(config.I2C_SDA_PIN),
                      scl=Pin(config.I2C_SCL_PIN), freq=100000)
            outputs = Outputs(i2c, config.MCP_ADDRESS,
                              config.OUTPUT_CHANNELS, config.VERIFIED_OUTPUTS)
        while True:
            now = time.ticks_ms()
            inputs = {name: debounce[name].update(
                pin.value() == (0 if config.INPUT_ACTIVE_LOW else 1),
                now, time.ticks_diff) for name, pin in pins.items()}
            link.poll(now)
            fresh = link.fresh(now, time.ticks_diff)
            parking = (fresh and link.peer["inputs"].get("parking_switch", False))
            desired = lighting.update(inputs, parking, now, time.ticks_diff)
            if outputs is not None:
                outputs.apply(desired)
            if time.ticks_diff(now, last_report) >= 250:
                state = {"desired": desired, "peer_online": fresh,
                         "physical_outputs_enabled": config.ENABLE_MCP_OUTPUTS}
                link.send(inputs, state)
                print("LIGHT_REQUESTS", desired, "PICO1_ONLINE", fresh)
                led.toggle()
                last_report = now
            time.sleep_ms(10)
    finally:
        if outputs is not None and not outputs.off():
            print("FAULT: CANNOT CONFIRM OUTPUTS OFF; REMOVE BENCH LOAD POWER")
        led.off()


if __name__ == "__main__":
    run()
