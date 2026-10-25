"""JSON report generation for entities and system state."""
import json
import time
import os


class ReportGenerator:
    def __init__(self, report_dir=None):
        self.report_dir = report_dir or os.path.expanduser('~/portfolio/reports')
        os.makedirs(self.report_dir, exist_ok=True)

    def generate_entity_report(self, entity_id, entity_data, actions):
        report = {
            'entity_id': entity_id,
            'entity_data': entity_data,
            'actions': actions,
            'generated_at': time.time(),
        }
        filename = f'entity_report_{entity_id[:8]}.json'
        path = os.path.join(self.report_dir, filename)
        with open(path, 'w') as f:
            json.dump(report, f, indent=2)
        return path

    def generate_general_report(self):
        report = {
            'timestamp': time.time(),
            'total_entities': 0,
            'total_actions': 0,
            'success_rate': 0,
        }
        path = os.path.join(self.report_dir, f'general_report_{int(time.time())}.json')
        with open(path, 'w') as f:
            json.dump(report, f, indent=2)
        return path
