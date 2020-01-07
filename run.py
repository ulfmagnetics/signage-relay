# signage-relay
#
# Author: John Berry (ulfmagnetics@gmail.com)
#
# Sends packets to a UART device over a BLE link using the Adafruit_BluefruitLE library.
# Based mostly on `examples/uart_service.py` from the Adafruit_Python_BluefruitLE repository.
#

import Adafruit_BluefruitLE
import adafruit_bluefruit_connect
from Adafruit_BluefruitLE.services import UART
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.button_packet import ButtonPacket
from signage_air_quality.air_quality_packet import AirQualityPacket
from time import sleep

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

        print('Sending packets...')
        color = (200,200,0)
        color_packet = ColorPacket(color)
        uart.write(color_packet.to_bytes())

        i = 0
        while i < 10:
            button_packet = ButtonPacket(b'8', True)
            uart.write(button_packet.to_bytes())

            sleep(0.1)

            button_packet = ButtonPacket(b'8', False)
            uart.write(button_packet.to_bytes())

            sleep(0.5)

            i = i + 1

    finally:
        device.disconnect()

ble.initialize()
ble.run_mainloop_with(main)
