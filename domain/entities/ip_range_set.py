from domain.entities.ip_range import IPRange
from domain.entities.ip_address import IPAddress


class IPRangeSet:
    def __init__(self, raw: str) -> None:
        if not raw or not raw.strip():
            raise ValueError("EMPTY_RANGE_SET")

        self.raw = raw

    def expand(self) -> list[IPAddress]:
        seen: set[str] = set()
        result: list[IPAddress] = []

        parts = self.raw.replace(",", ";").split(";")

        for part in parts:
            part = part.strip()
            if not part:
                continue

            ip_range = IPRange(part)

            for ip in ip_range.expand():
                if ip.value not in seen:
                    seen.add(ip.value)
                    result.append(ip)

        return result
