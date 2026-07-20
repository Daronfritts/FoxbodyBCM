"""
logger.py
Foxbody BCM Logging System

Handles:
- System logging
- Event logging
- Console output
- Log file creation
"""

from pathlib import Path
import logging


class BCMLogger:

    def __init__(self):

        self.log_directory = Path("logs")
        self.log_directory.mkdir(exist_ok=True)

        self.logger = logging.getLogger("FoxbodyBCM")
        self.logger.setLevel(logging.INFO)

        if self.logger.handlers:
            return

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s"
        )

        file_handler = logging.FileHandler(
            self.log_directory / "bcm.log"
        )

        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


logger = BCMLogger()
