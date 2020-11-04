import psutil

from ._configuration import interception_config
from ._common import safe_run_async
from .utility import Utility

__all__ = [
    'Interception'
]


class Interception(object):
    @staticmethod
    def add_proxy_interception_info(name, x=None, trace=None):
        p = psutil.Process()
        ps = p.name()
        data = {'ps': ps, 'name': name, 'x': Utility.fullname(x), 'trace': trace}
        safe_run_async(url=f'{interception_config.url}api/proxy/interception/add', json=data)
