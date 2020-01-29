from airnow.mock_api import MockApi
from airnow.api import Api

# For now this is just a very thin wrapper around the Airnow API,
# with the goal of making it easier to plug into a real source of
# air quality data at some point in the near future.

class PacketSource:
    def __init__(self, config):
        self._airnow_api = MockApi() if config.mock_api else Api(api_key=config.api_key, zip_code=config.zip_code)
        self._config = config

    def read_packets(self):
        return self.airnow_api.read_packets()

    @property
    def config(self):
        return self._config

    @property
    def airnow_api(self):
        return self._airnow_api
