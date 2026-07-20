"""
startup.py

Foxbody BCM Startup Manager

Responsible for:
- Loading configuration
- Initializing logger
- Starting hardware
- Preparing the BCM for module loading
"""

from globals import config, logger
from hardware import hardware


class StartupManager:

    def __init__(self):
        self.ready = False

    def initialize(self):

        logger.info("=" * 50)
        logger.info("Foxbody BCM Startup")
        logger.info("=" * 50)

        logger.info("Loading Configuration...")

        if config.load():
            logger.info("Configuration Loaded")
        else:
            logger.error("Configuration Failed")
            return False

        logger.info("Initializing Hardware...")

        if hardware.initialize():
            logger.info("Hardware Ready")
        else:
            logger.error("Hardware Failed")
            return False

        self.ready = True

        logger.info("Startup Complete")

        return True


startup = StartupManager()
