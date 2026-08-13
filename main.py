"""
main.py

Foxbody BCM main entry point.
"""

import time

from logger import logger
from startup import startup
from runtime import runtime
from hardware import hardware


LOOP_PERIOD_S = 0.02  # 50 Hz cooperative control loop


def main():
    logger.info("")
    logger.info("========================================")
    logger.info("Starting Foxbody BCM")
    logger.info("========================================")

    if not startup.initialize():
        logger.critical("Startup Failed")
        return

    logger.info("")
    logger.info("========================================")
    logger.info("SYSTEM READY")
    logger.info("========================================")
    logger.info("")

    try:
        while True:
            started = time.monotonic()
            runtime.update()

            elapsed = time.monotonic() - started
            delay = LOOP_PERIOD_S - elapsed
            if delay > 0:
                time.sleep(delay)
            else:
                logger.warning("Main loop overrun: %.1f ms", elapsed * 1000.0)

    finally:
        # Motor outputs fail to OFF in software whenever the process exits.
        runtime.shutdown()
        hardware.stop_all_motors()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("")
        logger.info("Foxbody BCM Stopped")
    except Exception as error:
        logger.exception("Fatal Error: %s", error)
        raise
