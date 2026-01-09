import ipaddress
from domain.entities.ip_address import IPAddress


class IPRange:
    def __init__(self, raw: str) -> None:
        if not raw or not raw.strip():
            raise ValueError("EMPTY_RANGE")

        raw = raw.strip()

        # --- предварительная валидация ---
        try:
            if " - " in raw:
                start_str, end_str = raw.split(" - ", 1)
                ipaddress.ip_address(start_str)
                ipaddress.ip_address(end_str)

            elif "/" in raw:
                ipaddress.ip_network(raw, strict=False)

            elif "-" in raw:
                # октетные диапазоны проверятся глубже, но формат должен быть IP-подобным
                parts = raw.split(".")
                if len(parts) != 4:
                    raise ValueError

                for part in parts:
                    if "-" in part:
                        a, b = part.split("-", 1)
                        a_i = int(a)
                        b_i = int(b)
                        if a_i > b_i:
                            raise ValueError

                    else:
                        int(part)

            else:
                # одиночный IP
                ipaddress.ip_address(raw)

        except Exception:
            raise ValueError("INVALID_RANGE")

        self.raw = raw

    def expand(self) -> list[IPAddress]:
        # 1. Полный диапазон: IP - IP
        if " - " in self.raw:
            start_str, end_str = self.raw.split(" - ", 1)
            start = ipaddress.ip_address(start_str)
            end = ipaddress.ip_address(end_str)

            if start > end:
                raise ValueError("INVALID_RANGE")

            return [
                IPAddress(str(ipaddress.ip_address(int(start) + i)))
                for i in range(int(end) - int(start) + 1)
            ]

        # 2. CIDR
        if "/" in self.raw:
            try:
                net = ipaddress.ip_network(self.raw, strict=False)
            except ValueError:
                raise ValueError("INVALID_CIDR")

            return [IPAddress(str(ip)) for ip in net]

        # 3. Диапазоны октетов (150.102.1-2.10-11)
        if "-" in self.raw:
            return self._expand_octet_ranges()

        # 4. Одиночный IP
        try:
            ip = ipaddress.ip_address(self.raw)
        except ValueError:
            raise ValueError("INVALID_IP")

        return [IPAddress(str(ip))]

    def _expand_octet_ranges(self) -> list[IPAddress]:
        parts = self.raw.split(".")
        if len(parts) != 4:
            raise ValueError("INVALID_IP_RANGE")

        ranges: list[list[int]] = []

        for part in parts:
            if "-" in part:
                start, end = part.split("-", 1)
                start_i = int(start)
                end_i = int(end)
                if start_i > end_i:
                    raise ValueError("INVALID_OCTET_RANGE")
                ranges.append(list(range(start_i, end_i + 1)))
            else:
                ranges.append([int(part)])

        ips: list[IPAddress] = []

        for a in ranges[0]:
            for b in ranges[1]:
                for c in ranges[2]:
                    for d in ranges[3]:
                        try:
                            ip = ipaddress.ip_address(f"{a}.{b}.{c}.{d}")
                        except ValueError:
                            raise ValueError("INVALID_IP_RANGE")
                        ips.append(IPAddress(str(ip)))

        return ips
