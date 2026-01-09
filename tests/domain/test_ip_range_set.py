from domain.entities.ip_range_set import IPRangeSet


def test_overlapping_ranges_do_not_duplicate_ips():
    s = IPRangeSet("150.102.95.10-15; 150.102.95.14-18")
    ips = [ip.value for ip in s.expand()]

    assert ips == [
        "150.102.95.10",
        "150.102.95.11",
        "150.102.95.12",
        "150.102.95.13",
        "150.102.95.14",
        "150.102.95.15",
        "150.102.95.16",
        "150.102.95.17",
        "150.102.95.18",
    ]

def test_fully_duplicate_ranges():
    s = IPRangeSet("10.0.0.1-3, 10.0.0.1-3")
    ips = [ip.value for ip in s.expand()]

    assert ips == [
        "10.0.0.1",
        "10.0.0.2",
        "10.0.0.3",
    ]

def test_single_ip_duplicated_by_range():
    s = IPRangeSet("10.0.0.1; 10.0.0.1-3")
    ips = [ip.value for ip in s.expand()]

    assert ips == [
        "10.0.0.1",
        "10.0.0.2",
        "10.0.0.3",
    ]

def test_empty_segments_are_ignored():
    s = IPRangeSet("10.0.0.1;;10.0.0.2")
    ips = [ip.value for ip in s.expand()]

    assert ips == [
        "10.0.0.1",
        "10.0.0.2",
    ]
