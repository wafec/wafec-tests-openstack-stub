from .default_proxy import DefaultProxy

__all__ = [
    'DefaultProxy',
    'create_proxy'
]

create_proxy = DefaultProxy.of
