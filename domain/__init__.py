# domain/__init__.py

from .entities.ip_address import IPAddress
from .value_objects.ping_status import PingStatus

__all__ = [
    "IPAddress",
    "PingStatus",
]
