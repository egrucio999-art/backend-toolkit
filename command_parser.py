"""CLI command parser with registry and descriptions."""
import shlex


class CommandParser:
    def __init__(self):
        self.commands = {
            'help': 'Show command list',
            'clients': 'List connected clients',
            'dispatch': 'Send a command to a client',
            'broadcast': 'Send a command to all clients',
            'exit': 'Exit',
            'clear': 'Clear the screen',
            'status': 'Show system status',
        }

    def parse(self, input_string):
        parts = shlex.split(input_string)
        if not parts:
            return None, []
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        return command, args

    def get_description(self, command):
        return self.commands.get(command, 'Unknown command')

    def list_commands(self):
        return self.commands
