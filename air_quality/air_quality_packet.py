"""
`signage-relay.air_quality_packet`
====================================================

Data packet containing air quality data, in the style
of Bluefruit Connect packets e.g. ColorPacket and ButtonPacket

* Author: John Berry (ulfmagnetics@gmail.com)

"""

import struct
import adafruit_bluefruit_connect
from adafruit_bluefruit_connect.packet import Packet

class AirQualityPacket(Packet):
    """A packet containing data about the current AQI (PM2.5) in a given location"""

    _FMT_PARSE = '<xxHsx'
    PACKET_LENGTH = struct.calcsize(_FMT_PARSE)
    # _FMT_CONSTRUCT doesn't include the trailing checksum byte.
    _FMT_CONSTRUCT = '<2sHs'
    _TYPE_HEADER = b'!Q'

    METRIC_HEADERS = { 'PM2.5': b'P', 'O3': b'O' }
    VALID_METRICS = list(METRIC_HEADERS.keys())

    def __init__(self, value, metric = 'PM2.5'):
        try:
            assert self.VALID_METRICS.index(metric) >= 0
        except:
            raise ValueError('Must be one of the following supported AQI metrics: {0}'.format(self.VALID_METRICS))

        self._value = value
        self._metric = metric

    @classmethod
    def parse_private(cls, packet):
        """Construct a AirQualityPacket from an incoming packet.
        Do not call this directly; call Packet.from_bytes() instead.
        pylint makes it difficult to call this method _parse(), hence the name.
        """
        metric = None
        value, metric_code = struct.unpack(cls._FMT_PARSE, packet)
        for m, c in cls.METRIC_HEADERS.items():
            if c == metric_code:
                metric = m
        return cls(value, metric)

    def to_bytes(self):
        """Return the bytes needed to send this packet."""
        metric_code = self.METRIC_HEADERS[self._metric]
        partial_packet = struct.pack(self._FMT_CONSTRUCT, self._TYPE_HEADER, self._value, metric_code)
        return self.add_checksum(partial_packet)

    @property
    def metric(self):
        """ The AQI metric represented by this packet """
        return self._metric

    @property
    def value(self):
        """ The value of the AQI metric """
        return self._value

# Register this class with the superclass. This allows the user to import only what is needed.
AirQualityPacket.register_packet_type()
