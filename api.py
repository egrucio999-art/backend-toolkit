"""Generic endpoint router with structured responses."""
import time


class APIRouter:
    def __init__(self):
        self.endpoints = {}

    def register_endpoint(self, name, handler):
        self.endpoints[name] = handler

    def handle_request(self, endpoint, data):
        if endpoint in self.endpoints:
            return self.endpoints[endpoint](data)
        return {'error': 'Endpoint not found'}

    def create_response(self, status, data=None, message=''):
        return {
            'status': status,
            'data': data,
            'message': message,
            'timestamp': time.time(),
        }

    def list_endpoints(self):
        return list(self.endpoints.keys())
