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
from time import sleep
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
    zip_code = env.str('ZIP_CODE')
    poll_interval = env.int('POLL_INTERVAL', default=300)
    debug = env.bool('DEBUG', default=False)
    print('Initializing API with MOCK_API={0}, AIRNOW_API_KEY={1}, ZIP_CODE={2}'.format(mock_api, api_key, zip_code))
    airnow_api = MockApi() if mock_api else Api(api_key=api_key, zip_code=zip_code)

    try:
        print('Discovering services...')
        UART.discover(device)

        uart = UART(device)

        while True:
            try:
                for packet in airnow_api.read_packets():
                    if debug:
                        print("Sending packet: value={0}, metric={1}, timestamp={2}".format(packet.value, packet.metric, packet.timestamp))
                    uart.write(packet.to_bytes())
            except:
                print("Exception while reading packet from API", sys.exc_info()[0])

            sleep(poll_interval)

    finally:
        device.disconnect()

ble.initialize()
ble.run_mainloop_with(main)
