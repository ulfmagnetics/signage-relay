from itertools import chain
from random import randint, shuffle
from time import sleep

from signage_air_quality.air_quality_packet import AirQualityPacket

from .api import Api

class MockApi(Api):

    def __init__(self):
        pm25_packets = list(map(lambda v: AirQualityPacket(v, 'PM2.5'), [33, 120, 240, 350, 10]))
        o3_packets = list(map(lambda v: AirQualityPacket(v, 'O3'), [10, 90, 300, 240, 75]))
        self._mock_packets = list(chain(pm25_packets, o3_packets))
        shuffle(self._mock_packets)

    def next_packet(self):
        # simulate blocking on network I/O for some amount of time
        sleep(randint(3,10))

        if len(self.mock_packets) < 1:
            return None
        else:
            return self.mock_packets.pop()

    @property
    def mock_packets(self):
        return self._mock_packets
