"""
Settings Manager for AI Terminal Desktop
"""

import json
import os
from pathlib import Path


class SettingsManager:
    def __init__(self):
        # Use XDG config directory
        config_dir = os.getenv('XDG_CONFIG_HOME', 
                              os.path.join(Path.home(), '.config'))
        self.config_path = os.path.join(config_dir, 'aiterminal-desktop')
        self.settings_file = os.path.join(self.config_path, 'settings.json')
        
        # Create config directory if it doesn't exist
        os.makedirs(self.config_path, exist_ok=True)
    
    def load_settings(self):
        """Load settings from file"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f'Error loading settings: {e}')
                return {}
        return {}
    
    def save_settings(self, settings):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            return True
        except Exception as e:
            print(f'Error saving settings: {e}')
            return False
