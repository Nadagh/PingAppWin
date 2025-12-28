import pytest

from Tools import ip_address_tools


@pytest.mark.parametrize(
        "pattern, expected", (
                ("255.255.255.0", "255.255.255.0"),
                ("256.255.255.0", False),
                ("127.0.0.1", "127.0.0.1")
                )
        )
def test_validate_ip_address(pattern, expected):
    assert ip_address_tools.validate_ip_address(pattern) == expected
