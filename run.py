# signage-relay
#
# Author: John Berry (ulfmagnetics@gmail.com)
#
# Sends packets to a UART device over a BLE link using the Adafruit_BluefruitLE library.
# Based mostly on `examples/uart_service.py` from the Adafruit_Python_BluefruitLE repository.
#

import os
import sys
from dotenv import load_dotenv
from envparse import env
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART

from airnow.mock_api import MockApi
from airnow.api import Api

load_dotenv()

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

    mock_api = env.bool('MOCK_API', default=False)
    api_key = env.str('AIRNOW_API_KEY')
    print('Initializing API with MOCK_API={0}, AIRNOW_API_KEY={1}'.format(mock_api, api_key))
    airnow_api = MockApi() if mock_api else Api(api_key=api_key)

    try:
        print('Discovering services...')
        UART.discover(device)

        uart = UART(device)

        while True:
            try:
                packet = airnow_api.next_packet()
                print("Sending packet: value={0}, metric={1}".format(packet.value, packet.metric))
                uart.write(packet.to_bytes())
            except:
                print("Exception while waiting for next packet from API", sys.exc_info()[0])

    finally:
        device.disconnect()

ble.initialize()
ble.run_mainloop_with(main)
