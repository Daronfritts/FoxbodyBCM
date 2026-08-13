"""
runtime.py

FoxbodyBCM cooperative runtime scheduler.

Every feature module gets a fast non-blocking update() call. No BCM module is
allowed to own an infinite loop or sleep for user-visible timing; timers are
implemented with monotonic timestamps so safety functions keep running.
"""

from logger import logger
from modules.door_locks import door_locks
from modules.windows import windows


class BCMRuntime:
    def __init__(self):
        self.modules = [
            door_locks,
            windows,
        ]

    def update(self):
        for module in self.modules:
            module.update()

    def shutdown(self):
        logger.info("Runtime | Safe shutdown")
        for module in reversed(self.modules):
            shutdown = getattr(module, "shutdown", None)
            if shutdown:
                try:
                    shutdown()
                except Exception as error:
                    logger.error("Runtime | shutdown error in %s: %s", module.__class__.__name__, error)


runtime = BCMRuntime()
