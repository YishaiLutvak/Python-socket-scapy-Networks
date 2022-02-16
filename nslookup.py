import sys
i, o, e = sys.stdin, sys.stdout, sys.stderr
from scapy.all import *
sys.stdin, sys.stdout, sys.stderr = i, o, e

TIMEOUT = 2
COMMANDS = {'A': 1, 'CNAME': 5, 'PTR': 12}
DNS_GOOGLE = "8.8.8.8"
SOURCE_PORT = 54321
DESTINATION_PORT = 53

# Yishai Lutvak 30490864

# tests:
# 1)
# python nslookup.py -type=PTR 10.0.0.0
# *** UnKnown can't find 0.0.0.10.in-addr.arpa.: Non-existent domain
# 2)
# python nslookup.py ssssssssssssssssssss
# *** UnKnown can't find ssssssssssssssssssss: Non-existent domain
# 3)
# python nslookup.py amazon.com
# 54.239.28.85
# 205.251.242.103
# 176.32.103.205
# 4)
# python nslookup.py -type=PTR 205.251.242.103
# s3-console-us-standard.console.aws.amazon.com
# 5)
# python nslookup.py -type=ptr 205.251.242.103
# s3-console-us-standard.console.aws.amazon.com
# 6)
# python nslookup.py 205.251.242.103
# The query is invalid
# 7)
# python nslookup.py -type=ptr 205.251.242
# The query is invalid


def is_valid_ip(str_ip) -> tuple:
    """
    Checks if the IP address is correct,
    returns a tuple of true or false and the list of numbers that make up the IP
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


def get_type(argv) -> str:
    """
    Returns the type of question
    """
    length_argv = len(argv)
    if length_argv > 2 and argv[1] in ('-type=PTR', '-type=ptr'):
        return "PTR"
    return "A"


def handles_request(type_request, question_name) -> tuple:
    """
    Returns a tuple of truth or falsehood,
    the name of the question,
    and the commands that interest us in the request
    """
    valid, ip_list = is_valid_ip(question_name)
    if type_request == "PTR":
        if not valid:
            return False, question_name, []
        question_name = f"{ip_list[3]}.{ip_list[2]}.{ip_list[1]}.{ip_list[0]}.in-addr.arpa"
        my_commands = (COMMANDS['PTR'],)
    else:
        if valid:
            return False, question_name, []
        my_commands = (COMMANDS['A'], COMMANDS['CNAME'])
    return True, question_name, my_commands


def get_res_dns(type_request, question_name):
    """
    Creates a dns query and returns the answer
    """
    pkt = IP(dst=DNS_GOOGLE) /\
          UDP(sport=SOURCE_PORT, dport=DESTINATION_PORT) /\
          DNS(rd=1, qdcount=1) / DNSQR(qtype=type_request, qname=question_name)
    pkt.show()
    try:
        res = sr1(pkt, verbose=0, timeout=TIMEOUT)
        res.show()
    except:
        pass
    return res


def filter_res(res, num_ans, my_commands) -> list:
    """
    Filters the responses according to the appropriate commands
    and returns a list of them
    """
    my_list_after_filter = []
    for num in range(num_ans):
        item = res[DNSRR][num]
        if item.type in my_commands:
            data = item.rdata
            if isinstance(data, bytes):
                data = data.decode()[:-1]
            my_list_after_filter.append(data)
    return my_list_after_filter


def main():
    """
    Runs as nslookup function
    """
    # assert is_valid_ip("255.255.255.255")[0] is True
    # assert is_valid_ip("256.0.0.0")[0] is False
    # assert is_valid_ip("0.0.0")[0] is False

    length_argv = len(sys.argv)
    if length_argv == 1:
        print("No parameters were received")
        return
    question_name = sys.argv[length_argv-1]
    type_request = get_type(sys.argv)
    valid, question_name, my_commands = handles_request(type_request, question_name)
    if not valid:
        print("The query is invalid")
        return
    res = get_res_dns(type_request, question_name)
    if not res:
        print("res is:", res)
        print('There is no answer')
        return
    num_ans = res[DNS].ancount
    if num_ans == 0:
        print(f"*** UnKnown can't find {question_name}: Non-existent domain")
        return
    my_filter_list = filter_res(res, num_ans, my_commands)
    [print(item) for item in my_filter_list]


if __name__ == "__main__":
    main()
