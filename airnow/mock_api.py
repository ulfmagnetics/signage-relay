from itertools import chain
from random import randint, shuffle
from time import sleep

from signage_air_quality.air_quality_packet import AirQualityPacket

from .api import Api

class MockApi(Api):

    def __init__(self):
        self._pm25_packets = list(map(lambda v: AirQualityPacket(v, 'PM2.5'), [33, 120, 240, 350, 10]))
        self._o3_packets = list(map(lambda v: AirQualityPacket(v, 'O3'), [10, 90, 300, 240, 75]))
        shuffle(self._pm25_packets)
        shuffle(self._o3_packets)

    def read_packets(self):
        # simulate blocking on network I/O for some amount of time
        sleep(randint(3,10))

        if len(self.pm25_packets) < 1 or len(self.o3_packets) < 1:
            return []
        else:
            return [self.pm25_packets.pop(), self.o3_packets.pop()]

    @property
    def pm25_packets(self):
        return self._pm25_packets

    @property
    def o3_packets(self):
        return self._o3_packets
