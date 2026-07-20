"""
globals.py
Foxbody BCM Shared Objects

Anything the whole BCM needs goes here.
"""

from config import ConfigManager
from logger import logger


config = ConfigManager()

SYSTEM_NAME = "Foxbody BCM"
VERSION = "1.0.0"

START_TIME = None

SYSTEM_READY = False
SAFE_MODE = False
