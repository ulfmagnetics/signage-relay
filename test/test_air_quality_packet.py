import unittest
from air_quality.air_quality_packet import AirQualityPacket

class TestAirQualityPacket(unittest.TestCase):

    def test_to_bytes(self):
        packet = AirQualityPacket(56, 'O3').to_bytes()
        self.assertEqual(chr(packet[0]) + chr(packet[1]), "!Q")
        self.assertEqual(packet[2], 56) # little-endian
        self.assertEqual(packet[3], 0) # little-endian
        self.assertEqual(chr(packet[4]), "O")

    def test_from_bytes(self):
        bs = b'!Q:\x00O\x04'
        packet = AirQualityPacket.from_bytes(bs)
        self.assertEqual(packet.metric, 'O3')
        self.assertEqual(packet.value, 58)

if __name__ == '__main__':
    unittest.main()
