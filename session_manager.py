"""Session lifecycle manager with TTL cleanup."""
import time
import uuid
import threading


class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.lock = threading.Lock()

    def create_session(self, user_id=None):
        session_id = str(uuid.uuid4())
        with self.lock:
            self.sessions[session_id] = {
                'id': session_id,
                'user_id': user_id,
                'created_at': time.time(),
                'last_activity': time.time(),
            }
        return session_id

    def get_session(self, session_id):
        with self.lock:
            session = self.sessions.get(session_id)
            if session:
                session['last_activity'] = time.time()
            return session

    def delete_session(self, session_id):
        with self.lock:
            return self.sessions.pop(session_id, None) is not None

    def cleanup_sessions(self, timeout=3600):
        current_time = time.time()
        with self.lock:
            to_remove = [sid for sid, s in self.sessions.items()
                         if current_time - s['last_activity'] > timeout]
            for sid in to_remove:
                del self.sessions[sid]
        return len(to_remove)
