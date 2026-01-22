"""
Settings manager for persisting application settings.
Uses a JSON file to store settings between sessions.
"""

import json
import os
from pathlib import Path
from typing import Any


class Settings:
    """
    Manages application settings persistence.
    
    Settings are stored in a JSON file in the user's app data directory
    or alongside the application.
    """
    
    # Default settings file location (in project root)
    _DEFAULT_SETTINGS_FILE = "app_settings.json"
    
    # Singleton instance
    _instance = None
    
    def __new__(cls):
        """Ensure only one instance exists (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize settings manager."""
        if self._initialized:
            return
        
        self._initialized = True
        self._settings_file = self._get_settings_path()
        self._settings: dict[str, Any] = {}
        self._load_settings()
    
    def _get_settings_path(self) -> Path:
        """Get the path to the settings file."""
        # Store settings in the project root directory
        # In production, you might want to use user's app data directory
        return Path(__file__).parent.parent.parent / self._DEFAULT_SETTINGS_FILE
    
    def _load_settings(self):
        """Load settings from file."""
        if self._settings_file.exists():
            try:
                with open(self._settings_file, 'r', encoding='utf-8') as f:
                    self._settings = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._settings = {}
        else:
            self._settings = {}
    
    def _save_settings(self):
        """Save settings to file."""
        try:
            with open(self._settings_file, 'w', encoding='utf-8') as f:
                json.dump(self._settings, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save settings: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a setting value.
        
        Args:
            key: The setting key.
            default: Default value if key doesn't exist.
            
        Returns:
            The setting value or default.
        """
        return self._settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """
        Set a setting value and save to file.
        
        Args:
            key: The setting key.
            value: The value to store.
        """
        self._settings[key] = value
        self._save_settings()
    
    def get_last_directory(self) -> str:
        """
        Get the last used directory.
        
        Returns:
            The last directory path, or the project root if not set.
        """
        last_dir = self.get("last_directory")
        
        if last_dir and os.path.isdir(last_dir):
            return last_dir
        
        # Default to project root
        project_root = Path(__file__).parent.parent.parent
        return str(project_root)
    
    def set_last_directory(self, directory: str):
        """
        Set the last used directory.
        
        Args:
            directory: The directory path to store.
        """
        self.set("last_directory", directory)


# Global settings instance for easy access
settings = Settings()

