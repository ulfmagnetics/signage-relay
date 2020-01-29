from collections import namedtuple

from dotenv import load_dotenv
from envparse import env

class Configuration:
    def Struct(**kwargs):
        return namedtuple('Struct', ' '.join(kwargs.keys()))(**kwargs)

    @classmethod
    def generate(cls):
        load_dotenv()
        return cls.Struct(
            mock_api=env.bool('MOCK_API', default=False),
            api_key=env.str('AIRNOW_API_KEY'),
            zip_code=env.str('ZIP_CODE'),
            poll_interval=env.int('POLL_INTERVAL', default=300),
            debug = env.bool('DEBUG', default=False)
        )
