from envparse import env
from time import sleep

from signage_air_quality.air_quality_packet import AirQualityPacket

class Api:
    def __init__(self, api_key=None, read_timeout=60):
        self._api_key = api_key
        self._read_timeout = read_timeout

    def next_packet(self):
        sleep(self.read_timeout)
        return None

    @property
    def read_timeout(self):
        return self._read_timeout
