"""In-memory notification queue with read/unread tracking."""
import time
import threading


class NotificationManager:
    def __init__(self):
        self.notifications = []
        self.lock = threading.Lock()

    def add(self, title, message, level='info'):
        with self.lock:
            self.notifications.append({
                'title': title,
                'message': message,
                'level': level,
                'timestamp': time.time(),
                'read': False,
            })

    def get_all(self):
        with self.lock:
            return self.notifications.copy()

    def get_unread(self):
        with self.lock:
            return [n for n in self.notifications if not n['read']]

    def mark_read(self, index):
        with self.lock:
            if 0 <= index < len(self.notifications):
                self.notifications[index]['read'] = True

    def clear(self):
        with self.lock:
            self.notifications.clear()
