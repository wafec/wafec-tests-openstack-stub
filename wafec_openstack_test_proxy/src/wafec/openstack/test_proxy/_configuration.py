import platform
import os
import configparser

from .exceptions import UnsupportedOperatingSystemException

__all__ = [
    'interception_config'
]


class InterceptionConfiguration(object):
    def __init__(self):
        self.url = 'http://localhost:6543/'


interception_config = InterceptionConfiguration()
path = ''

if platform.system() == 'Linux':
    path = '/usr/wafec/config.ini'
elif platform.system() == 'Windows':
    path = 'C:/wafec/config.ini'
else:
    raise UnsupportedOperatingSystemException()

if os.path.exists(path):
    config = configparser.ConfigParser()
    config.read(path)
    if 'interception' in config.sections():
        interception = config['interception']
        interception_config.url = interception.get('url', interception_config.url)
