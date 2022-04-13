from scapy.all import *
import random

LENGTH_FIELD_SIZE = 5
READ_FILE = 1
TIMEOUT = 5
BUCKET_CAPACITY = 180
SERVER_IP = "127.0.0.1"
WINDOW = 10
NUM_PROTOCOL = 100

MAX_NUM_SECTIONS = 250
SEND_FILE = 251
MY_ACK = 252
ERROR_BIG_FILE = 253
ERROR_NOT_FOUND = 254
MY_FIN = 255
MAX_TIMES = 40

ERROR_MESSAGES = {ERROR_BIG_FILE: "File is very big", ERROR_NOT_FOUND: "File not found"}


def create_short_messages(file_content, num_of_sections, ip_dst) -> list:
    """
    :parameter file_content
    :parameter num_of_sections - The amount of parts that need to divide the data
    :parameter ip_dst
    Divides the contents of the file into pieces and produces a list of small messages
    :return list of packages
    """
    my_list = []
    for i in range(num_of_sections):
        start = i * BUCKET_CAPACITY
        end = start + BUCKET_CAPACITY
        my_pkt = create_msg(file_content[start: end], i, ip_dst)
        my_list.append(my_pkt)
    print("num_of_sections =", len(my_list))
    return my_list


def special_send(pkt) -> None:
    """
    :parameter pkt - package to send
    Sends a package in a way that it can get lost
    """
    fail = random.randint(1, 10)
    if not (fail == 1):
        pkt.show()
        send(pkt)
    else:
        print("Oops\n")


# def send_until_response(pkt, max_times=MAX_TIMES) -> bool:
#     """
#     :parameter pkt - package to send
#     :parameter max_times - max times to send
#     Sends a package until a response is received from the recipient,
#     or reaching the max_times
#     :return True if any response has been received
#     """
#     counter = 0
#     while True:
#         special_send(pkt)
#         counter += 1
#         p = sniff(count=1, lfilter=filter_msg, timeout=TIMEOUT)
#         if len(p) > 0:
#             return True
#         elif counter > max_times:
#             return False


def send_until_ack(pkt, max_times=MAX_TIMES) -> bool:
    """
    :parameter pkt - packet to send
    :parameter max_times - max times to send
    Sends a package until "ack" is received from the recipient,
    or reaching the max_times
    :return True if ack has been received
    """
    counter = 0
    while True:
        special_send(pkt)
        counter += 1
        p = sniff(count=1, lfilter=filter_msg, timeout=TIMEOUT)
        if len(p) > 0 and IP in p[0] and p[0][IP].tos == MY_ACK:
            return True
        elif counter > max_times:
            return False


def send_3_times(my_msg, difference=10) -> None:
    """
    :parameter my_msg - massage to send
    :parameter difference - The time difference between the sending
    Sends package 3 times
    """
    special_send(my_msg)
    time.sleep(difference)
    special_send(my_msg)
    time.sleep(difference)
    special_send(my_msg)


def filter_msg(pkt) -> bool:
    """
    :parameter pkt - massage to send
    Filter packets according to the IP protocol field
    """
    if IP in pkt and pkt[IP].proto == NUM_PROTOCOL:
        return True
    return False


def create_msg(data, my_tos, ip_dst):
    """
    :parameter data - Raw.load of the message
    :parameter my_tos - The value of the tos field in the IP protocol
    :parameter ip_dst - Destination IP address
    Generates a packet with the data, tos number, and ip_dst destination address
    :return a built-in package ready for launch
    """
    return IP(dst=ip_dst, tos=my_tos, proto=NUM_PROTOCOL) / Raw(load=data)


def create_ack(ip_dst, data="ack"):
    """
    :parameter ip_dst - Destination IP address
    :parameter data - Raw.load of the message
    Generates a packet with the "ack" data, tos number of ack, and ip_dst destination address
    :return a built-in package of ack ready for launch
    """
    return create_msg(data, MY_ACK, ip_dst)


# ######################################################################
#
# # not in using
#
#
# def get_file_data(file_name):
#     """
#     Get data from file (after conversion to bytes)
#     """
#     file_type = file_name.split(".")[-1]
#     print("file type:", file_type)
#     data = None  # if suffix is not recognized return None
#     if file_type in ('txt', 'js', 'css'):
#         f = open(file_name, 'r')
#         file_content = f.read()
#         data = file_content.encode()
#     elif file_type == 'html':
#         f = open(file_name, 'r', encoding='utf-8')
#         file_content = f.read()
#         data = file_content.encode()
#     elif file_type in ('jpg', 'ico'):
#         f = open(file_name, 'rb')
#         data = f.read()
#     return data
#
#
# def create_seq_num(length, data=''):
#     zfill_length = (str(length)).zfill(LENGTH_FIELD_SIZE)
#     message = zfill_length + data
#     return message
#
# ######################################################################
#
# # Area for experiments
#
#
# import json
#
#
# def main():
#     t_string = '{"syn": 1, "ack": 0, "ack_num":0, "seq_num":1, "type":"file_name", "file_name":"my_secret.png"}'
#     res = json.loads(t_string)
#     print(res)  # <dict>  {"Prajot" : 1, "Kuvalekar" : 3}
#     print(type(res))
#     json_object = json.dumps(res)
#     print(json_object)
#     print(type(json_object))
#
#
# if __name__ == '__main__':
#     main()
#
#
# # TCP
# syn = 0x02
# ack = 0x10
# syn_ack = 0x12
#
# # IP
# icmp = 0x01
# udp = 0x11
# tcp = 0x06