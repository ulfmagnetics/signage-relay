# signage-relay
#
# Author: John Berry (ulfmagnetics@gmail.com)
#
# Sends packets to a UART device over a BLE link using the Adafruit_BluefruitLE library.
# Based mostly on `examples/uart_service.py` from the Adafruit_Python_BluefruitLE repository.
#

from itertools import chain
from time import sleep
from random import randint, shuffle
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART
from signage_air_quality.air_quality_packet import AirQualityPacket

ble = Adafruit_BluefruitLE.get_provider()

def main():
    ble.clear_cached_data()

    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using adapter: {0}'.format(adapter.name))

    print('Disconnecting any connected UART devices...')
    UART.disconnect_devices()

    print('Searching for UART device...')
    try:
        adapter.start_scan()
        device = UART.find_device()
        if device is None:
            raise RuntimeError('Failed to find UART device!')
    finally:
        adapter.stop_scan()

    print('Connecting to device...')
    device.connect()

    try:
        print('Discovering services...')
        UART.discover(device)

        uart = UART(device)

        print('Sending mock packets...')
        pm25 = list(map(lambda v: AirQualityPacket(v, 'PM2.5'), [33, 120, 240, 350, 10]))
        o3 = list(map(lambda v: AirQualityPacket(v, 'O3'), [10, 90, 300, 240, 75]))
        mock_packets = list(chain(pm25, o3))
        shuffle(mock_packets)
        for packet in mock_packets:
            print("Sending packet: value={0}, metric={1}".format(packet.value, packet.metric))
            uart.write(packet.to_bytes())
            sleep(randint(1,5))

    finally:
        device.disconnect()

ble.initialize()
ble.run_mainloop_with(main)
