import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'firmware/common'))
from control import DebouncedInput, Lighting, Supervisor
from link import Link

spec = importlib.util.spec_from_file_location('pico_outputs', ROOT / 'firmware/pico2/outputs.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
Outputs = module.Outputs

PERIOD = 1 << 30

def diff(a, b):
    return ((a - b + PERIOD // 2) % PERIOD) - PERIOD // 2


class UART:
    def __init__(self):
        self.rx = b''
        self.tx = b''
    def any(self):
        return len(self.rx)
    def read(self, n):
        data, self.rx = self.rx[:n], self.rx[n:]
        return data
    def write(self, data):
        self.tx += data
        return len(data)


class Bus:
    def __init__(self):
        self.writes = []
        self.fail = False
    def writeto_mem(self, address, register, data):
        if self.fail:
            raise OSError('bus disconnected')
        self.writes.append((address, register, data))


class FirmwareTests(unittest.TestCase):
    def test_debounce_startup_bounce_and_clock_wrap(self):
        d = DebouncedInput(30)
        self.assertFalse(d.update(True, PERIOD-20, diff))
        self.assertFalse(d.ready)
        self.assertFalse(d.update(False, PERIOD-10, diff))
        self.assertFalse(d.update(True, PERIOD-5, diff))
        self.assertFalse(d.update(True, 20, diff))
        self.assertTrue(d.update(True, 25, diff))
        self.assertTrue(d.ready)

    def test_shutdown_never_claims_halt_or_cuts_power(self):
        s = Supervisor()
        for volts, now in [(11.9, 0), (11.9, 30000), (11.0, 31000)]:
            result = s.update(False, volts, now, diff)
            self.assertTrue(result['shutdown_request'])
            self.assertFalse(result['power_removal_allowed'])
        self.assertEqual(result['state'], 'CRITICAL_SHUTDOWN_REQUEST')
        result = s.update(True, 10, 32000, diff)
        self.assertEqual(result['state'], 'RUNNING')
        self.assertFalse(result['shutdown_request'])
        self.assertTrue(result['screen_enable'])
        self.assertEqual(s.update(False, None, 33000, diff)['state'], 'BATTERY_UNKNOWN')
        self.assertEqual(s.update(False, 12.6, 34000, diff)['state'], 'PARKED')

    def test_low_battery_timeout_and_recovery(self):
        s = Supervisor()
        self.assertEqual(s.update(False, 11.9, 100, diff)['state'], 'LOW_BATTERY')
        self.assertEqual(s.update(False, 11.9, 30100, diff)['state'], 'SHUTDOWN_TIMEOUT')
        s.update(False, 12.6, 31000, diff)
        self.assertEqual(s.update(False, 11.9, 32000, diff)['state'], 'LOW_BATTERY')

    def test_fogs_independent_and_headlights_mutually_exclusive(self):
        light = Lighting()
        for head in [False, True]:
            for high in [False, True]:
                out = light.update({'headlight_switch': head, 'high_beam_switch': high,
                                    'fog_switch': True}, False, 0, diff)
                self.assertTrue(out['fog_lamp_control'])
                self.assertFalse(out['headlamp_enable'] and out['high_beam_enable'])
                self.assertEqual(out['parking_lamps'], head)
        self.assertTrue(light.update({}, True, 0, diff)['parking_lamps'])

    def test_hazard_precedence_and_flasher(self):
        light = Lighting()
        out = light.update({'left_turn': True}, False, PERIOD-100, diff)
        self.assertTrue(out['left_turn_output'])
        self.assertFalse(out['right_turn_output'])
        out = light.update({'hazard': True}, False, 400, diff)
        self.assertFalse(out['left_turn_output'])
        out = light.update({'hazard': True}, False, 900, diff)
        self.assertTrue(out['left_turn_output'] and out['right_turn_output'])
        out = light.update({'left_turn': True, 'right_turn': True}, False, 910, diff)
        self.assertFalse(out['left_turn_output'] or out['right_turn_output'])
        out = light.update({}, False, 920, diff)
        self.assertFalse(out['left_turn_output'] or out['right_turn_output'])

    def test_link_fragmentation_bad_data_and_expiry(self):
        uart = UART()
        link = Link(uart, 'pico2', 'pico1')
        valid = b'{"v":1,"role":"pico1","inputs":{"parking_switch":true}}\n'
        uart.rx = valid[:15]
        link.poll(0)
        self.assertFalse(link.fresh(0, diff))
        uart.rx = valid[15:]
        link.poll(PERIOD-100)
        self.assertTrue(link.fresh(100, diff))
        self.assertFalse(link.fresh(1400, diff))
        for invalid in [b'bad\n', b'[]\n', valid.replace(b'pico1', b'pico2'),
                        valid.replace(b'true', b'"false"')]:
            uart.rx = invalid
            link.poll(1500)
        self.assertEqual(link.errors, 4)
        self.assertEqual(link.last_rx, PERIOD-100)
        uart.rx = b'x' * 800 + b'\n' + valid
        while uart.any():
            link.poll(2000)
        self.assertEqual(link.errors, 5)
        self.assertTrue(link.fresh(2000, diff))

    def test_link_roundtrip(self):
        uart = UART()
        Link(uart, 'pico1', 'pico2').send({'parking_switch': True}, {'state': 'RUNNING'})
        uart.rx, uart.tx = uart.tx, b''
        receiver = Link(uart, 'pico2', 'pico1')
        receiver.poll(0)
        self.assertTrue(receiver.peer['inputs']['parking_switch'])

    def test_output_startup_allowlist_and_fault_latch(self):
        bus = Bus()
        outputs = Outputs(bus, 0x20, {'parking_lamps': 1, 'fog_lamp_control': 10,
                                    'start': 3}, ['parking_lamps', 'fog_lamp_control'])
        self.assertEqual(bus.writes[-2:], [(0x20, 0x14, b'\0\0'), (0x20, 0, b'\0\0')])
        outputs.apply({'parking_lamps': True, 'fog_lamp_control': True, 'start': True})
        self.assertEqual(bus.writes[-1], (0x20, 0x14, b'\x01\x02'))
        bus.fail = True
        with self.assertRaises(OSError):
            outputs.apply({})
        self.assertTrue(outputs.fault)
        self.assertFalse(outputs.off())
        bus.fail = False
        with self.assertRaises(OSError):
            outputs.apply({'parking_lamps': True})
        self.assertTrue(outputs.off())

    def test_assignment_uniqueness_and_repository_output_map(self):
        configs = []
        for role in ['pico1', 'pico2']:
            scope = {}
            exec((ROOT / ('firmware/' + role + '/config.py')).read_text(), scope)
            configs.append(scope)
        p1, p2 = configs
        used1 = list(p1['INPUT_PINS'].values()) + list(p1['RELAY_PINS'].values()) + [0, 1, 3, 5, 14, 16, 26]
        used2 = list(p2['INPUT_PINS'].values()) + list(p2['WINDOW_PINS'].values()) + list(p2['LOCK_PINS'].values()) + [0, 1, 2, 3, 28]
        self.assertEqual(len(used1), len(set(used1)))
        self.assertEqual(len(used2), len(set(used2)))
        self.assertFalse(p2['ENABLE_MCP_OUTPUTS'])
        self.assertEqual(p2['VERIFIED_OUTPUTS'], ())
        mapping = json.loads((ROOT / 'config/io_map.json').read_text())['mosfet_outputs']
        self.assertEqual(p2['OUTPUT_CHANNELS'], {k: int(v[1:]) for k, v in mapping.items()})

# Execute each real main loop against a fake MicroPython environment. This checks
# actual pin initialization/cleanup, not just the pure state machines above.
class MainLoopTests(unittest.TestCase):
    def run_main(self, role):
        import types
        from unittest.mock import patch
        clock = {'now': 0}
        class StopLoop(Exception):
            pass
        class Pin:
            IN, OUT, PULL_UP, PULL_DOWN = 0, 1, 2, 3
            instances = []
            def __init__(self, number, mode=None, pull=None, value=None):
                self.number, self.mode, self.pull = number, mode, pull
                self.v = value if value is not None else int(pull == self.PULL_UP)
                self.history = [self.v]
                self.instances.append(self)
            def value(self, value=None):
                if value is not None:
                    self.v = int(value)
                    self.history.append(self.v)
                return self.v
            def off(self):
                self.value(0)
            def toggle(self):
                self.value(not self.v)
        class Serial(UART):
            def __init__(self, *args, **kwargs):
                super().__init__()
        def sleep_ms(ms):
            clock['now'] += ms
            if clock['now'] >= 300:
                raise StopLoop()
        def forbidden_i2c(*args, **kwargs):
            raise AssertionError('MCP must not be initialized with shipped defaults')
        config_spec = importlib.util.spec_from_file_location('config', ROOT / ('firmware/' + role + '/config.py'))
        config = importlib.util.module_from_spec(config_spec)
        config_spec.loader.exec_module(config)
        fake = types.SimpleNamespace(Pin=Pin, UART=Serial, I2C=forbidden_i2c)
        fake_time = types.SimpleNamespace(ticks_ms=lambda: clock['now'], ticks_diff=diff,
                                          sleep_ms=sleep_ms)
        modules = {'machine': fake, 'time': fake_time, 'config': config, 'outputs': module}
        main_spec = importlib.util.spec_from_file_location('firmware_main', ROOT / ('firmware/' + role + '/main.py'))
        main = importlib.util.module_from_spec(main_spec)
        with patch.dict(sys.modules, modules), patch('builtins.print'):
            main_spec.loader.exec_module(main)
            with self.assertRaises(StopLoop):
                main.run()
        return config, Pin.instances

    def test_pico1_never_energizes_relays_and_cleans_up(self):
        config, pins = self.run_main('pico1')
        for pin in pins:
            if pin.number in config.RELAY_PINS.values():
                self.assertEqual(pin.history, [1, 1])
            if pin.number in [3, 5]:
                self.assertTrue(all(value == 0 for value in pin.history))
        self.assertFalse(any(pin.number in [14, 16, 26] for pin in pins))

    def test_pico2_default_never_initializes_motors_or_i2c(self):
        config, pins = self.run_main('pico2')
        reserved = set(config.WINDOW_PINS.values()) | set(config.LOCK_PINS.values())
        self.assertFalse(any(pin.number in reserved for pin in pins))
        self.assertEqual([pin.history[-1] for pin in pins if pin.number == 'LED'], [0])


if __name__ == '__main__':
    unittest.main()
