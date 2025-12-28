# domain/value_objects/ping_status.py

from enum import Enum, auto


class PingStatus(Enum):
    PENDING = auto()
    SUCCESS = auto()
    FAILURE = auto()
    ERROR = auto()
