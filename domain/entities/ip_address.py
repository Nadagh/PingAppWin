# domain/entities/ip_address.py

import ipaddress


class IPAddress:
    """
    Domain Entity: IP address.

    Гарантирует, что IP корректен.
    """

    def __init__(self, value: str) -> None:
        try:
            self._ip = ipaddress.ip_address(value)
        except ValueError:
            raise ValueError("INVALID_IP")


    @property
    def value(self) -> str:
        return str(self._ip)

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IPAddress):
            return False
        return self._ip == other._ip
