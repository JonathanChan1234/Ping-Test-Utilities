import socket
import re


def check_valid_ip(ip: str) -> bool:
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


# reference: https://stackoverflow.com/questions/45010810/check-for-valid-domain-name-in-a-string
# check whether the host is a valid domain name
# valid domain name: {not more than 63 characters (including hyphen)}.{not more than 63 characters (including hyphen)}
def check_valid_host(host: str) -> bool:
    if re.match(r'[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63})*', host):
        return True
    else:
        return False