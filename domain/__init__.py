# domain/__init__.py

from .entities.ip_address import IPAddress
from .value_objects.ping_result_status import PingResultStatus

__all__ = [
    "IPAddress",
    "PingResultStatus"
]
