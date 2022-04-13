"""
    Exam1 protocol implementation
    Author: Yishai Lutvak 304909864
    Date: 4/2/2022
"""
from scapy.all import *
import random
import json


DEFAULT_DIR = 'C:/Networks/work/'
READ_FILE = 1
WRITE_FILE = 2
TIMEOUT = 2
BUCKET_CAPACITY = 180
SERVER_IP = "127.0.0.1"
WINDOW = 10
NUM_PROTOCOL = 100
LENGTH_FIELD_SIZE = 5
ERROR_ZERO = 'Error - Division by 0 is impossible'


# TCP
syn = 0x02
ack = 0x10
syn_ack = 0x12

# IP
icmp = 0x01
udp = 0x11
tcp = 0x06


ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}


def is_float(value) -> bool:
    """
    :parameter value is string
    :returns True if converting string to float is possible, else False
    """
    try:
        float(value)
        return True
    except:
        return False


def my_prn(pkt) -> None:
    print("my_prn")


def filter_msg(my_packet) -> bool:
    """
    :parameter my_packet - packet to check
    :returns True if the packet match to our protocol, else False
    """
    if ICMP in my_packet and Raw in my_packet:
        msg = str(my_packet[Raw].load.decode())
        if (my_packet[ICMP].type == 8) and (len(msg) == 9) and (msg[:-1].isdigit()) and (msg[-1] in ops):
            print('filter_message(my_packet) => True')
            return True
        if (my_packet[ICMP].type == 0) and ((is_float(msg)) or (msg == ERROR_ZERO)):
            print('filter_message(my_packet) => True')
            return True
    print('filter_message(my_packet) => False')
    return False


def filter_msg_2(pkt) -> bool:
    if IP in pkt and pkt[IP].proto == NUM_PROTOCOL:
        return True
    return False


def calc(secret) -> str:
    """
    :parameter secret
    :returns solution
    """
    part1 = int(secret[:4])
    part2 = int(secret[4:8])
    operation = secret[8]
    if operation == '/' and part2 == 0:
        return ERROR_ZERO
    return str(ops[operation](part1, part2))


def create_msg(data, icmp_type, ip_dst=SERVER_IP):
    """
    :parameter data
    :parameter icmp_type
    :parameter ip_dst
    :returns pkt
    """
    return IP(dst=ip_dst) / ICMP(type=icmp_type) / Raw(load=data)


def create_msg_2(data, my_tos, ip_dst=SERVER_IP):
    return IP(dst=ip_dst, tos=my_tos, proto=NUM_PROTOCOL) / Raw(load=data)


######################################################################


def get_type_of_file(url) -> str:
    """
    :parameter url is path of file
    slice by the last dot in order to get suffix of file
    :returns suffix of file
    """
    return url[url.rfind('.') + 1:]


def get_file_data(file_name, file_type) -> bytes:
    """
    Get data from file (after conversion to bytes)
    """
    data = None  # if suffix is not recognized return None
    if file_type in ('txt', 'js', 'css'):
        f = open(file_name, 'r')
        file_content = f.read()
        data = file_content.encode()
        f.close()
    elif file_type == 'html':
        f = open(file_name, 'r', encoding='utf-8')
        file_content = f.read()
        data = file_content.encode()
        f.close()
    elif file_type in ('jpg', 'ico'):
        f = open(file_name, 'rb')
        data = f.read()
        f.close()
    return data


def is_valid_ip(str_ip) -> tuple:
    """
    :parameter str_ip - str of ip address
    Checks if the IP address is correct,
    :returns a tuple of true or false and the list of numbers that make up the IP
    """
    def is_valid_item(str_item):
        """
        Checks if the part is a number that matches an IP number
        """
        if str_item.isdigit() and int(str_item) < 256:
            return True
        return False
    ip_list = str_ip.split(".")
    if len(ip_list) == 4 and all([is_valid_item(item) for item in ip_list]):
        return True, ip_list
    return False, ip_list


def create_seq_num(length, data=''):
    zfill_length = (str(length)).zfill(LENGTH_FIELD_SIZE)
    message = zfill_length + data
    return message

######################################################################


def main():
    """
    Area for tests and experiments
    """
    # assert for fun is_valid_ip
    assert is_valid_ip("255.255.255.255")[0] is True
    assert is_valid_ip("256.0.0.0")[0] is False
    assert is_valid_ip("0.0.0")[0] is False


if __name__ == "__main__":
    main()
