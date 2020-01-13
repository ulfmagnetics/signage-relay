import requests
from envparse import env
from time import sleep

from .observation import Observation

class Api:
    def __init__(self, api_key, zip_code, distance_miles=10, read_timeout=60):
        self._api_key = api_key
        self._zip_code = zip_code
        self._distance_miles = distance_miles
        self._read_timeout = read_timeout

    def read_packets(self):
        request = requests.get(self.current_observation_url(), timeout=self.read_timeout)
        observation = Observation.from_json(request.json())
        return observation.to_packet_list()

    def current_observation_url(self):
        return 'http://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode={0}&distance={1}&API_KEY={2}'.format(self.zip_code, self.distance_miles, self.api_key)

    @property
    def api_key(self):
        return self._api_key

    @property
    def zip_code(self):
        return self._zip_code

    @property
    def distance_miles(self):
        return self._distance_miles

    @property
    def read_timeout(self):
        return self._read_timeout
