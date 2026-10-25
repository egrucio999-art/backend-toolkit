"""Registry of connected clients with heartbeat tracking."""
import time
import threading


class ClientManager:
    def __init__(self):
        self.clients = {}
        self.lock = threading.Lock()

    def add_client(self, client_id, ip, hostname='', os_info=''):
        with self.lock:
            self.clients[client_id] = {
                'id': client_id,
                'ip': ip,
                'hostname': hostname,
                'os': os_info,
                'last_seen': time.time(),
                'online': True,
            }

    def remove_client(self, client_id):
        with self.lock:
            self.clients.pop(client_id, None)

    def update_last_seen(self, client_id):
        with self.lock:
            if client_id in self.clients:
                self.clients[client_id]['last_seen'] = time.time()
                self.clients[client_id]['online'] = True

    def get_client(self, client_id):
        with self.lock:
            return self.clients.get(client_id)

    def get_all_clients(self):
        with self.lock:
            return list(self.clients.values())

    def get_online_clients(self):
        online = []
        current_time = time.time()
        with self.lock:
            for client in self.clients.values():
                client['online'] = (current_time - client['last_seen']) < 30
                if client['online']:
                    online.append(client)
        return online

    def get_client_count(self):
        with self.lock:
            return len(self.clients)

    def cleanup(self, timeout=60):
        current_time = time.time()
        with self.lock:
            to_remove = [cid for cid, c in self.clients.items()
                         if current_time - c['last_seen'] > timeout]
            for cid in to_remove:
                del self.clients[cid]
        return len(to_remove)
