"""IP geolocation with multi-service failover."""
import requests


class GeoLocator:
    def __init__(self):
        self.services = [
            'http://ip-api.com/json/{}',
            'http://ipinfo.io/{}/json',
            'https://freegeoip.app/json/{}',
        ]

    def locate(self, ip):
        for service in self.services:
            try:
                response = requests.get(service.format(ip), timeout=10)
                if response.status_code == 200:
                    return response.json()
            except requests.RequestException:
                continue
        return None

    def format_location(self, data):
        if not data:
            return 'UNKNOWN'
        parts = []
        if data.get('lat') and data.get('lon'):
            parts.append(f"{data['lat']},{data['lon']}")
        if data.get('city'):
            parts.append(data['city'])
        if data.get('country'):
            parts.append(data['country'])
        if data.get('isp'):
            parts.append(f"ISP: {data['isp']}")
        return ' | '.join(parts)
