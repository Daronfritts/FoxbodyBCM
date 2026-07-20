"""
main.py

Foxbody BCM

Main Entry Point
"""

import time

from logger import logger
from startup import startup


def main():

    logger.info("")
    logger.info("========================================")
    logger.info("Starting Foxbody BCM")
    logger.info("========================================")

    #
    # Initialize System
    #

    if not startup.initialize():

        logger.critical("Startup Failed")

        return

    logger.info("")
    logger.info("========================================")
    logger.info("SYSTEM READY")
    logger.info("========================================")
    logger.info("")

    #
    # Main Loop
    #

    while True:

        #
        # Modules will run here later.
        #

        time.sleep(0.05)


if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        logger.info("")
        logger.info("Foxbody BCM Stopped")

    except Exception as error:

        logger.critical(f"Fatal Error: {error}")
