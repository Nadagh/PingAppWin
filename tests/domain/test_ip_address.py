# tests/domain/test_ip_address.py

import pytest

from domain.entities.ip_address import IPAddress


class TestIPAddress:
    """Domain tests for IPAddress entity."""

    @pytest.mark.parametrize(
        "value",
        [
            "127.0.0.1",
            "8.8.8.8",
            "192.168.0.1",
            "10.0.0.1",
            "255.255.255.255",
            "0.0.0.0",
        ],
    )
    def test_valid_ip_addresses_are_accepted(self, value: str):
        ip = IPAddress(value)
        assert ip.value == value

    @pytest.mark.parametrize(
        "value",
        [
            "",
            " ",
            "abc",
            "127.0.0",
            "127.0.0.1.1",
            "256.0.0.1",
            "192.168.0.999",
            "-1.0.0.0",
            "127.0.0.one",
            "127.0.0.01",   # ведущий ноль — потенциальная двусмысленность
            "127.0.0.1 ",
            " 127.0.0.1",
        ],
    )
    def test_invalid_ip_addresses_raise_value_error(self, value: str):
        with pytest.raises(ValueError):
            IPAddress(value)

    def test_ip_address_is_immutable(self):
        ip = IPAddress("127.0.0.1")
        with pytest.raises(AttributeError):
            ip.value = "8.8.8.8"

    def test_string_representation(self):
        ip = IPAddress("8.8.8.8")
        assert str(ip) == "8.8.8.8"

    def test_equality_by_value(self):
        ip1 = IPAddress("1.1.1.1")
        ip2 = IPAddress("1.1.1.1")
        ip3 = IPAddress("8.8.8.8")

        assert ip1 == ip2
        assert ip1 != ip3
