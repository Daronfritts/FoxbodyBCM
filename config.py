"""
config.py
Foxbody BCM Configuration Manager

Handles:
- Loading configuration files
- Saving configuration files
- Automatic configuration backups
- Configuration validation
"""

from pathlib import Path
import json
import shutil


class ConfigManager:
    """Manages BCM configuration files."""

    CONFIG_DIR = Path("config")

    CURRENT = CONFIG_DIR / "bcm_settings.json"
    PREVIOUS = CONFIG_DIR / "settings_previous.json"
    PREVIOUS2 = CONFIG_DIR / "settings_previous2.json"
    VEHICLE = CONFIG_DIR / "vehicle_profile.json"

    def __init__(self):
        self.settings = {}
        self.vehicle = {}

    def load(self):
        """Load all configuration files."""

        self.settings = self._load_json(self.CURRENT)
        self.vehicle = self._load_json(self.VEHICLE)

        return True

    def save(self):
        """Save configuration with automatic backup rotation."""

        self._rotate_backups()

        self._save_json(self.CURRENT, self.settings)

        return True

    def _rotate_backups(self):
        """Keep the two previous configuration versions."""

        if self.PREVIOUS.exists():
            shutil.copy2(self.PREVIOUS, self.PREVIOUS2)

        if self.CURRENT.exists():
            shutil.copy2(self.CURRENT, self.PREVIOUS)

    @staticmethod
    def _load_json(path):

        if not path.exists():
            return {}

        with open(path, "r") as file:
            return json.load(file)

    @staticmethod
    def _save_json(path, data):

        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as file:
            json.dump(data, file, indent=4)

    def validate(self):
        """
        Future:
            Validate settings before saving.
        """

        return True
