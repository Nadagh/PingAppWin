import pytest

from domain.entities.ip_range import IPRange


def test_single_ip_expands_to_one_address():
    r = IPRange("150.102.95.10")
    ips = r.expand()

    assert len(ips) == 1
    assert ips[0].value == "150.102.95.10"


def test_cidr_16_expands_correctly():
    r = IPRange("150.102.0.0/16")
    ips = r.expand()
    assert len(ips) == 65536
    assert ips[0].value == "150.102.0.0"
    assert ips[-1].value == "150.102.255.255"


def test_last_octet_range():
    r = IPRange("150.102.95.5-7")
    ips = r.expand()
    assert [ip.value for ip in ips] == [
            "150.102.95.5",
            "150.102.95.6",
            "150.102.95.7",
            ]


def test_multi_octet_range():
    r = IPRange("150.102.1-2.10-11")
    ips = r.expand()
    assert len(ips) == 4


def test_full_ip_range():
    r = IPRange("150.102.0.0 - 150.102.0.2")
    ips = r.expand()
    assert [ip.value for ip in ips] == [
            "150.102.0.0",
            "150.102.0.1",
            "150.102.0.2",
            ]


@pytest.mark.parametrize(
        "value", [
                "",
                "abc",
                "150.102",
                "150.102.0.10-5",
                "150.102.0.0/99",
                ]
        )
def test_invalid_range_raises(value):
    with pytest.raises(ValueError):
        IPRange(value)
