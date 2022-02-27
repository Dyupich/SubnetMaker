# -*- coding: utf-8 -*-
import random
import ipaddress


class IncorrectDataError(Exception):
    def __init__(self):
        self.txt = "Error!\n" \
                   "In file 'wronglastoctet.txt' must be 2 strings:\n" \
                   "1: N - number of generated subnets;\n" \
                   "2: Ip address - example: 192.168.1.0"


def make_valid_subnet(prefix: int):
    if isinstance(prefix, int):
        if prefix > 32 or prefix < 0:
            raise Exception("Prefix must be in range [0:32]")
            return None
        offset = 32 - prefix
        # Making offsets that will help us to make a validate address
        offset_octets = offset // 8
        offset_octet = 2 ** (offset % 8)
        subnet = []
        # At this moment we have 5 cases
        # Case 1: offset by octets == 0
        # For Example: /30 -> 2 ^ (32 - 30) = 2 ^ 2 * 2 ^ 0  = off_oct * 2 ^ off_octs
        # -> off_oct = 2 ^ 2; off_octs = 0 (0 // 8 = 0)
        # step will be:
        # 0.0.0.0/30
        # 0.0.0.4/30
        # ...
        # 0.0.0.252/30
        # 0.0.1.0/30
        # ...
        # [0-255].[0-255].[0-255].[number % 4 == 0 and in range [0-252]]/30
        if offset_octets == 0:
            for i in range(0, 3):
                subnet.append(random.randint(0, 255))
            # range will be [0,256) -> [0,252] in case /30
            subnet.append(random.randrange(0, 256, offset_octet))
        # Case 2: offset by octets == 1
        # For example: /23 -> 2 ^ (32 - 23) = 2 ^ (9) = 2 ^ 1 * 2 ^ 8 = off_oct * 2 ^ off_octs
        # -> off_oct = 2 ^ 1; off_octs = 1 (8 // 8 = 1)
        # 0.0.0.0/23
        # 0.0.2.0/23
        # ...
        # [0-255].[0-255].[number % 2 == 0 and in range [0-254]].0/23
        if offset_octets == 1:
            for i in range(0, 2):
                subnet.append(random.randint(0, 255))
            # range will be [0,256) with step 2 -> [0,254]
            subnet.append(random.randrange(0, 256, offset_octet))
            subnet.append(0)
        # Case 3: is similar to the case 2, but off_octs == 2:
        # [0-255].[number % offset_octet == 0 and range [0-(256-offset_octet)]].0.0/prefix
        if offset_octets == 2:
            subnet.append(random.randint(0, 255))
            subnet.append(random.randrange(0, 256, offset_octet))
            for i in range(0, 2):
                subnet.append(0)
        # Case 4:
        # [number % offset_octet == 0 and range [0-(256-offset_octet)]].0.0.0/prefix
        if offset_octets == 3:
            subnet.append(random.randrange(0, 256, offset_octet))
            for i in range(0, 3):
                subnet.append(0)
        # Case 5:
        # 0.0.0.0/0
        if offset_octets == 4:
            for i in range(0, 4):
                subnet.append(0)
        return '.'.join(map(str, subnet)) + f"/{prefix}"
    raise TypeError("Prefix must be integer number")
    return None


# O(1)
def get_valid_data(filename):
    with open(filename, "r") as file:
        # Getting two strings from file
        txt = file.read().split("\n")
        # Correctness check of strings in "wronglastoctet.txt" file.
        if len(txt) != 2:
            raise IncorrectDataError
            return None
        # Correctness check of strings in "wronglastoctet.txt" file again.
        try:
            N = int(txt[0])
            ip_address = txt[1]
            octets = list(map(int, txt[1].split(".")))
        except Exception as ex:
            raise IncorrectDataError
            return None
        # Correctness check for octets in ip address
        for octet in octets:
            if octet < 0 or octet > 255:
                raise ValueError("Octet must be in range [0:255]")
                return None
        return N, ip_address


# O(N)
def get_min_subnet(ip_address: str, iter_file: str):
    if isinstance(ip_address, str) and isinstance(iter_file, str):
        with open(iter_file, "r") as file:
            subnets = file.read().split('\n')
            max = ipaddress.IPv4Network('0.0.0.0/0')
            max_prefix = 0
            ip = ipaddress.IPv4Address(ip_address)
            for subnet in subnets:
                # __contains__() method in subnets (instance of IPv4Network)
                # performs bitwise multiplication of ip and mask
                net = ipaddress.IPv4Network(subnet)
                prefix = int(subnet.split('/')[1])
                if ip in net:
                    if max_prefix < prefix:
                        max = net
                        max_prefix = prefix
            return str(max)
    raise TypeError("Arguments must be 'str' instance.")
    return None


if __name__ == '__main__':
    # Reading file and if it has not validate data then raising a Exception
    N, ip_address = get_valid_data("in.txt")
    with open("autogen.txt", "w") as file:
        for i in range(0, N - 1):
            # prefix of valid subnet must be in [/0, /32]
            file.write(f"{make_valid_subnet(random.randint(0, 32))}\n")
        file.write(f"{make_valid_subnet(random.randint(0, 32))}")
    with open("out.txt", "w") as file:
        file.write(f"{ip_address}\n")
        file.write(get_min_subnet(ip_address, 'autogen.txt'))
