from dotenv import load_dotenv
from envparse import env
from time import time

from signage_air_quality.air_quality_packet import AirQualityPacket

class Observation:
    @classmethod
    def from_json(cls, json):
        return cls(json)

    def __init__(self, json):
        load_dotenv()
        self._debug = env.bool('DEBUG', default=False)
        self._json = json

    def to_packet_list(self):
        if self.debug:
            print('Observation: json={0}', self.json)
        return list(map(lambda h: AirQualityPacket(h['AQI'], h['ParameterName'], int(time())), self.json))

    @property
    def debug(self):
        return self._debug

    @property
    def json(self):
        return self._json
