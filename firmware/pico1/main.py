from machine import Pin, UART
import time
import config
from control import DebouncedInput, Supervisor
from link import Link


def run():
    relay_off = 1 if config.RELAY_ACTIVE_LOW else 0
    # Atomic initial output values; software cannot control the ROM/reset interval.
    relays = [Pin(pin, Pin.OUT, value=relay_off)
              for pin in config.RELAY_PINS.values()]
    shutdown = Pin(config.PI_SHUTDOWN_REQUEST_PIN, Pin.OUT, value=0)
    screen = Pin(config.SCREEN_ENABLE_PIN, Pin.OUT, value=0)
    # Disconnect and ADC pins intentionally remain untouched.
    led = Pin(config.LED_PIN, Pin.OUT, value=0)
    pins = {name: Pin(number, Pin.IN,
                     Pin.PULL_DOWN if name == "pi_alive" else Pin.PULL_UP)
            for name, number in config.INPUT_PINS.items()}
    debounce = {name: DebouncedInput(config.DEBOUNCE_MS) for name in pins}
    supervisor = Supervisor()
    uart = UART(0, baudrate=config.UART_BAUD,
                tx=Pin(config.UART_TX_PIN), rx=Pin(config.UART_RX_PIN), timeout=0)
    link = Link(uart, "pico1", "pico2")
    last_report = time.ticks_ms()
    last_state = None
    print("PICO1", config.FIRMWARE_VERSION, "BENCH_ONLY; POWER RELAYS INHIBITED")
    try:
        while True:
            now = time.ticks_ms()
            inputs = {}
            for name, pin in pins.items():
                raw = pin.value() == (1 if name == "pi_alive" else
                                       (0 if config.INPUT_ACTIVE_LOW else 1))
                inputs[name] = debounce[name].update(raw, now, time.ticks_diff)
            volts = config.SIMULATED_BATTERY_VOLTS if config.BENCH_MODE else None
            state = supervisor.update(inputs["ignition"], volts, now, time.ticks_diff,
                                      config.LOW_BATTERY_VOLTS,
                                      config.CRITICAL_BATTERY_VOLTS,
                                      config.SHUTDOWN_GRACE_SECONDS * 1000)
            led.value(state["screen_enable"])
            screen.value(state["screen_enable"] and config.ENABLE_SCREEN_SIGNAL)
            shutdown.value(state["shutdown_request"] and config.ENABLE_PI_SHUTDOWN_SIGNAL)
            link.poll(now)
            if state["state"] != last_state:
                print("STATE", state["state"], "POWER_REMOVAL_ALLOWED=False")
                last_state = state["state"]
            if time.ticks_diff(now, last_report) >= 250:
                link.send(inputs, state)
                last_report = now
            time.sleep_ms(10)
    finally:
        for relay in relays:
            relay.value(relay_off)
        screen.off()
        shutdown.off()
        led.off()


if __name__ == "__main__":
    run()
