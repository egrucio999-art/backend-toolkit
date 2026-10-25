"""Realtime connection manager with command/result dispatch."""
import time


class ConnectionManager:
    def __init__(self):
        self.connections = {}
        self.command_callbacks = {}
        self.result_callbacks = {}

    def add_connection(self, client_id, connection):
        self.connections[client_id] = {
            'connection': connection,
            'connected_at': time.time(),
            'last_activity': time.time(),
        }

    def remove_connection(self, client_id):
        self.connections.pop(client_id, None)

    def get_connection(self, client_id):
        return self.connections.get(client_id, {}).get('connection')

    def get_all_connections(self):
        return list(self.connections.keys())

    def register_command_callback(self, command, callback):
        self.command_callbacks[command] = callback

    def register_result_callback(self, callback):
        self.result_callbacks[len(self.result_callbacks)] = callback

    def dispatch(self, client_id, command):
        handler = self.command_callbacks.get(command)
        return handler(client_id, command) if handler else None

    def on_result(self, client_id, result):
        for callback in self.result_callbacks.values():
            callback(client_id, result)

    def get_connection_count(self):
        return len(self.connections)
