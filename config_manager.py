"""JSON config loader with dotted-key get/set."""
import os
import json


class ConfigManager:
    def __init__(self, config_path=None):
        self.config_path = config_path or os.path.expanduser('~/portfolio/config.json')
        self.config = self.load()

    def load(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        return self.default_config()

    def default_config(self):
        return {
            'server': {
                'host': '127.0.0.1',
                'port': 8095,
                'use_ssl': False,
            },
            'app': {
                'theme': 'default',
                'language': 'en',
            },
        }

    def save(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def set(self, key, value):
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
        self.save()
