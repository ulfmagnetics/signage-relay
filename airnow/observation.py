from signage_air_quality.air_quality_packet import AirQualityPacket

class Observation:
    @classmethod
    def from_json(cls, json):
        return cls(json)

    def __init__(self, json):
        self._json = json

    def to_packet_list(self):
        return list(map(lambda h: AirQualityPacket(h['AQI'], h['ParameterName']), self.json))

    @property
    def json(self):
        return self._json
