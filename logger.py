"""Thread-safe JSON-lines logger with daily rotation."""
import os
import time
import json
import threading


class Logger:
    def __init__(self, log_dir=None):
        self.log_dir = log_dir or os.path.expanduser('~/portfolio/logs')
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, f'app_{time.strftime("%Y%m%d")}.log')
        self.lock = threading.Lock()

    def log(self, level, message, data=None):
        entry = {
            'timestamp': time.time(),
            'level': level,
            'message': message,
            'data': data,
        }
        with self.lock:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(entry) + '
')

    def info(self, message, data=None):
        self.log('INFO', message, data)

    def warning(self, message, data=None):
        self.log('WARNING', message, data)

    def error(self, message, data=None):
        self.log('ERROR', message, data)

    def critical(self, message, data=None):
        self.log('CRITICAL', message, data)

    def read_logs(self, lines=100):
        if not os.path.exists(self.log_file):
            return []
        with open(self.log_file, 'r') as f:
            all_lines = f.readlines()
        return all_lines[-lines:]
