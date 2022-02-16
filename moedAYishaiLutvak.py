"""
    Exam1 server implementation
    Author: Yishai Lutvak 304909864
    Date: 4/2/2022
"""


import sys
i, o, e = sys.stdin, sys.stdout, sys.stderr
from scapy.all import *
sys.stdin, sys.stdout, sys.stderr = i, o, e


SOCKET_TIMEOUT = 0.1
MY_IP = "0.0.0.0"
PORT = 8153
HTTP_VERSION = 'HTTP/1.1'
BUCKET = 1024
DNS_TIMEOUT = 2
COMMANDS = {'A': 1, 'CNAME': 5, 'PTR': 12}
DNS_GOOGLE = "8.8.8.8"
SOURCE_PORT = 54321
DESTINATION_PORT = 53

#####################################################################################################


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
        my_commands = (COMMANDS['A'],)  # COMMANDS['CNAME']
    return True, question_name, my_commands


def get_res_dns(type_request, question_name):
    """
    Creates a dns query and returns the answer
    """
    pkt = IP(dst=DNS_GOOGLE) / UDP(sport=SOURCE_PORT, dport=DESTINATION_PORT) / \
          DNS(rd=1, qdcount=1) / DNSQR(qtype=type_request, qname=question_name)
    pkt.show()
    try:
        res1 = sr1(pkt, verbose=0, timeout=DNS_TIMEOUT)
        res1.show()
    except:
        res1 = None
    return res1


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
                data = data.decode()
            my_list_after_filter.append(data)
    return my_list_after_filter


def handle_part_of_dns(resource):
    """
    :parameter resource is a requested resource
    Manages the DNS request
    """
    list_of_resource = resource.split("/")
    print("list_of_resource =", list_of_resource)
    my_length = len(list_of_resource)
    question_name = list_of_resource[my_length-1]
    type_request =\
        "PTR" if (len(list_of_resource) == 2 and list_of_resource[0] in ('REVERSE', 'reverse'))\
        else "A"
    valid, question_name, my_commands = handles_request(type_request, question_name)
    print("type_request:", type_request)
    print("question_name:", question_name)
    if not valid:
        return "The query is invalid"
    res = get_res_dns(type_request, question_name)
    if not res:
        print("res is:", res)
        return 'There is no answer'
    num_ans = res[DNS].ancount
    if num_ans == 0:
        return f"*** UnKnown can't find {question_name}: Non-existent domain"
    my_filter_list = filter_res(res, num_ans, my_commands)
    str_of_my_filter_list = ""
    for item in my_filter_list:
        str_of_my_filter_list += f'{item}<br>'
    return str_of_my_filter_list
#####################################################################################################


def handle_status_500(client_socket):
    """
    get client socket
    and create response of status 500
    and send the response with the client socket
    """
    print('500 Internal Server Error')
    reply = HTTP_VERSION + ' 500 Internal Server Error\r\n\r\n'
    http_response = reply.encode()
    client_socket.send(http_response)


def handle_client_request(resource, client_socket):
    """
    Check the required resource,
    generate proper HTTP response and send to client
    """
    print('resource:', resource)
    data = handle_part_of_dns(resource)
    if not data:
        print('File type not detected')
        handle_status_500(client_socket)
        return
    print('200 OK')
    http_header = HTTP_VERSION + ' 200 OK\r\n'  # if all right return status ok
    # add Content-Length header to the header
    length = len(data)
    http_header += 'Content - Length: ' + str(length) + '\r\n'
    complete_header = http_header + 'Content-Type: text/html; charset=utf-8\r\n' + '\r\n'
    http_response = complete_header.encode() + data.encode()
    client_socket.send(http_response)


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    """
    print(request)
    first_line = request[:request.find("\r\n")]  # slice by first "\r\n" to get first line
    print('first line: ', first_line)
    items = first_line.split(" ")
    print('three items: ', items)
    if len(items) == 3 and items[0] == 'GET' and items[1].startswith('/') and items[2] in ('HTTP/1.1', 'HTTP/1.0'):
        return True, items[1][1:]
    return False, items[1][1:]


def handle_client(client_socket):
    """
    Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests
    """
    print('Client connected')
    while True:
        try:
            client_request = client_socket.recv(BUCKET).decode()
        except socket.timeout:
            print("client_socket was closed because set timeout")
            break
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
            break
        else:
            print('Error: Not a valid HTTP request')
            handle_status_500(client_socket)
            break
    print('Closing connection')
    client_socket.close()

#####################################################################################################


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((MY_IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()
