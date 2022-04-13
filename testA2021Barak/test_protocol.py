from scapy.all import *


def filter_msg(my_packet):
    """
    protocol: every raw message starts with 2 zeros
    filters the packets to find the packets of the protocol

    for client message to server:
    we check that the raw size is good
    we check if the first 8 characters are digits
    we check if the last one is one of this operators: +,-,*,/

    :param my_packet: packet to check
    :return: true if its the packet we were waiting for, otherwise returns false
    """
    cul_marks = ['+', '-', '*', '/']
    if Raw in my_packet and ICMP in my_packet:
        msg = str(my_packet[0][Raw].load.decode())
        if msg[:2] != '00':
            return False
        msg = msg[2:]
        if my_packet[0][ICMP].type == 8:
            digits = msg[:7].isdigit()
            length = len(msg) == 9
            mark = str(msg[8]) in cul_marks
            return digits and length and mark
        elif my_packet[0][ICMP].type == 0:
            return True
    return False


def my_cul(str_num):
    """
    culculate the result of 2 numbers and an operator
    :param str_num: string number with 8 digits and an operator
    :return: result
    """
    num1 = int(str_num[:4])
    num2 = int(str_num[4:8])
    if str_num[-1] == '+':
        return num1 + num2
    elif str_num[-1] == '-':
        return num1 - num2
    elif str_num[-1] == '/' and num2 != 0:
        return num1 / num2
    elif str_num[-1] == '*':
        return num1 * num2
    return 'Error'
