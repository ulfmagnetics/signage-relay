# signage-relay
#
# Author: John Berry (ulfmagnetics@gmail.com)
#
# Sends packets to a UART device over a BLE link using the Adafruit_BluefruitLE library.
# Based mostly on `examples/uart_service.py` from the Adafruit_Python_BluefruitLE repository.
#

import os
import sys
from time import sleep
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART

from signage_relay.configuration import Configuration
from signage_relay.packet_source import PacketSource

ble = Adafruit_BluefruitLE.get_provider()

config = Configuration.generate()

def debug(msg):
    if config.debug:
        print(msg)

def main():
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using adapter: {0}'.format(adapter.name))

    packet_source = PacketSource(config)

    UART.disconnect_devices()

    device = None

    while True:
        try:
            print('Connecting to device...')
            adapter.start_scan()
            device = UART.find_device()
            if device is None:
                raise RuntimeError('Failed to find UART device!')

            device.connect()

            UART.discover(device)
            uart = UART(device)

            for packet in packet_source.read_packets():
                debug('Sending packet: value={0}, metric={1}, timestamp={2}'.format(packet.value, packet.metric, packet.timestamp))
                uart.write(packet.to_bytes())

        except Exception as e:
            print('Caught exception of type {0} in main loop: {1}'.format(sys.exc_info()[0], str(e)))

        finally:
            print('Going to sleep for {0} seconds...'.format(config.poll_interval))
            sleep(config.poll_interval)
            print('Disconnecting devices before restarting main loop...')
            device.disconnect()
            adapter.stop_scan()

ble.initialize()
ble.run_mainloop_with(main)
