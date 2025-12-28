import os
import subprocess


def ping(ip: str, num: int = 1) -> subprocess.CompletedProcess:
    ping_limit = 10
    if (num <= 0):
        num = 1
    elif (num > ping_limit):
        num = ping_limit

    result = subprocess.run(
            ["ping", "-n", f"{num}", ip],
            encoding = "cp866",
            capture_output = True,
            text = True
            )
    return result


def ping_to_int(ip: str, num: int = 1) -> int:
    result = ping(ip, num)
    return result.returncode


def ping_to_bool(ip: str, num: int = 1) -> bool:
    result = ping(ip, num)
    code = result.returncode
    if (code == 0):
        return True
    elif (code == 1):
        return False


def batch_ping_to_int_list(ips: list, num: int = 1) -> list:
    list = []
    for ip in ips:
        list.append(ping_to_int(ip, num))
    return list


def batch_ping_to_bool_list(ips: list, num: int = 1) -> list:
    list = []
    for ip in ips:
        list.append(ping_to_bool(ip, num))
    return list


def batch_ping_to_int_dict(ips: list, num: int = 1) -> dict:
    dict = {}
    for ip in ips:
        dict[ip] = ping_to_int(ip, num)
    return dict


def batch_ping_to_bool_dict(ips: list, num: int = 1) -> dict:
    dict = {}
    for ip in ips:
        dict[ip] = ping_to_bool(ip, num)
    return dict


def main():
    print(ping("127.0.0.1",3).stdout)


if (__name__ == '__main__'):
    main()
