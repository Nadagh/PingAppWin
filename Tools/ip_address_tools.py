import ipaddress


def validate_ip_address(ip_address: str):
    try:
        ipaddress.ip_address(ip_address)
        return ip_address
    except ValueError:
        return False



def main():
    print(validate_ip_address("127.0.0.1"))


if (__name__ == '__main__'):
    main()
