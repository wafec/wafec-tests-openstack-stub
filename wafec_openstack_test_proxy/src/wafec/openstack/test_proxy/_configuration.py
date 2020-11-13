import platform
import os
import configparser

__all__ = [
    'interception_config',
    'BASE_CONFIG_DIR'
]

BASE_CONFIG_DIR = '/usr/wafec'


class InterceptionConfiguration(object):
    def __init__(self):
        self.url = 'http://localhost:7654/'
        self.dat_file = f'{BASE_CONFIG_DIR}/interception.dat'


interception_config = InterceptionConfiguration()


path = f'{BASE_CONFIG_DIR}/proxy.ini'
if os.path.exists(path):
    config = configparser.ConfigParser()
    config.read(path)
    interception_config.url = config.get('interception', 'url', fallback=interception_config.url)
    interception_config.dat_file = config.get("interception", 'dat_file', fallback=interception_config.dat_file)
