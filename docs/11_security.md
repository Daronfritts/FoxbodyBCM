# Foxbody BCM Security and Parked-Power Architecture

## Core security controller

The always-on security/BCM core should live on a low-power microcontroller (Pico-class MCU), not on the Raspberry Pi. The Pico remains responsible for the functions that must survive a Pi crash, reboot, software update, or low-battery shutdown.

Core Pico responsibilities:

- armed/disarmed state
- door, hatch, and hood monitoring
- alarm trigger logic
- siren/horn output
- lock/unlock authorization
- ignition/ACC monitoring
- battery-voltage monitoring
- Pi wake/power request
- event handoff to the Pi when available

The Raspberry Pi remains the high-level computer for the touchscreen dash, MicroSquirt communications, networking/Tailscale, detailed event history, configuration, diagnostics, and other higher-power services.

## Two-battery parked-power plan

Use the engine-bay starting battery and a separate auxiliary battery. The auxiliary battery is charged from the vehicle through a proper automotive DC-DC charger/isolator with reverse-current protection so the auxiliary system cannot normally discharge the starting battery.

Normal power path:

1. Engine running: alternator/main battery charges the auxiliary battery through the DC-DC charger.
2. Key off: display/backlight off immediately; Pi stays on; Pico/security stays on; parked loads run from the auxiliary battery.
3. Auxiliary battery low: shed nonessential Pi/display/network loads as configured.
4. Auxiliary battery critical: Pico requests a graceful Pi shutdown.
5. Auxiliary battery nearly exhausted: Pico/security transfers to a separately protected, very-low-current emergency feed from the engine-bay starting battery.
6. The emergency main-battery feed powers only the Pico/security survival functions, not the Pi, dash, NVMe, or other high-current accessories.
7. A hardware low-voltage disconnect protects the starting battery even if software fails.

The two batteries must not simply be paralleled when parked. The emergency feed must be current-limited/regulated and isolated so auxiliary loads cannot backfeed or flatten the starting battery.

## Long-term airport scenario

For a multi-week park, the auxiliary battery is intentionally consumed first. If it becomes depleted, the Pi shuts down and the Pico/security controller remains alive from the isolated starting-battery survival feed. This preserves security coverage while reserving the overwhelming majority of the starting battery for cranking the engine when the owner returns.

## Power-state behavior

- `KEY ON / ENGINE RUNNING` -> screen on, Pi on, Pico on, full services
- `KEY OFF` -> screen off, Pi on, Pico on, security active
- `AUX BATTERY LOW` -> screen remains off, optional load shedding
- `AUX BATTERY CRITICAL` -> save state/logs and gracefully shut Pi down
- `AUX BATTERY DEPLETED` -> Pico/security only on isolated main-battery emergency feed
- `MAIN BATTERY LOW` -> deepest Pico-only survival mode
- `MAIN BATTERY CRITICAL` -> hardware cutoff protects starting reserve

Battery state changes must use filtered voltage, timers, and hysteresis rather than a single instantaneous voltage reading. Final voltage thresholds will be selected after the exact starting-battery chemistry/capacity, auxiliary-battery chemistry/capacity, and measured parked current are known.

## Recovery / wake behavior

The Pico should be capable of requesting Pi power/wake when any configured wake condition occurs, such as ignition/ACC on, authorized unlock, driver-door opening, or a security event that requires higher-level logging/networking.
