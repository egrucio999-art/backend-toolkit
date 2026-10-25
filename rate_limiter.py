"""Sliding-window rate limiter, thread-safe."""
import time
import threading
from collections import defaultdict


class RateLimiter:
    def __init__(self, max_requests=10, window=60):
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)
        self.lock = threading.Lock()

    def allow(self, key):
        current_time = time.time()
        with self.lock:
            requests = [r for r in self.requests[key] if current_time - r < self.window]
            self.requests[key] = requests
            if len(requests) < self.max_requests:
                requests.append(current_time)
                return True
            return False

    def reset(self, key):
        with self.lock:
            self.requests.pop(key, None)

    def get_remaining(self, key):
        current_time = time.time()
        with self.lock:
            requests = [r for r in self.requests[key] if current_time - r < self.window]
            return self.max_requests - len(requests)
