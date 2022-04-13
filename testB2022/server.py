"""
Networks 44
"""

# Ex 4.4 - HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files
# or other utilities, for educational purpose
# Usage: Fill the missing functions and constants

# TO DO: import modules
import socket
import os

# TO DO: set constants
IP = "0.0.0.0"
PORT = 8200
SOCKET_TIMEOUT = 0.1
FIXED_RESPONSE = '' \
    'HTTP/1.1 200 OK\r\n' \
    'Content-Length: 12\r\n' \
    'Content-Type: text/html\r\n\r\n<i>hello</i>'
DEFAULT_BUFLEN = 1024
DEFAULT_URL = '/'
REDIRECTION_DICTIONARY = {}
ERROR404 = '/NOT_FOUND.html'
ERROR403 = '/FORBIDDEN.html'
ERROR500 = '/INTERNAL_SERVER_ERROR.html'
FORBIDDEN = []


def get_file_data(filename):
    """ Get data from file """
    path = "./webroot" + filename
    if not os.path.isfile(path):
        raise FileNotFoundError
    fin = open(path, 'rb')
    size = os.path.getsize(path)
    data = fin.read(size)
    return data


def protocol_answer(request):
    """
    answers request according to secret protocol
    """
    if (request[0] != '/'):
        return False, ''
    request = request[1:]
    request = request.split('/')
    if len(request) != 3:
        return False, ''
    if not request[0].isdigit() or not request[1].isdigit() or not request[2].isdigit():
        return False, ''
    op = int(request[0])
    n1 = int(request[1])
    n2 = int(request[2])
    if op == 1:
        return True, str(n1 + n2)
    elif op == 2:
        return True, str(n1 - n2)
    elif op == 3:
        return True, str(n1 * n2)
    elif op == 4:
        if n2 == 0:
            return False, ''
        return True, str(n1 / n2)
    else:
        return False, ''


def handle_client_request(resource, client_socket):
    """ Check the required resource,
    generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters)
    # generates the proper response
    status = '200 OK'
    if resource == '/':
        url = DEFAULT_URL
    else:
        url = resource

    # TO DO: check if URL had been
    # redirected, not available or other error code
    if url in REDIRECTION_DICTIONARY:
        # TO DO: send 302 redirection response
        url = REDIRECTION_DICTIONARY[url]
        status = '302 Moved Temporarily'
        response = f'HTTP/1.1 {status}\r\nLocation:{url}\r\n\r\n'
        client_socket.send(response.encode())
        return
    valid, data = protocol_answer(url)
    if not valid:
        data = "Error"
        status = '404 Not Found'
    if url in FORBIDDEN:
        data = "Forbidden"
        status = '403 Forbidden'
    if url == ERROR500:
        data = "Server Error"
        status = '500 Internal Server Error'

    # TO DO: extract requested file type from URL (html, jpg etc)
    filetype = url.split('.')[-1]
    http_header = '' \
        f'HTTP/1.1 {status}\r\n' \
        'Content-Type: {}\r\n' \
        f'Content-Length: {len(data)}\r\n\r\n'
    if filetype == 'html':
        http_header = http_header.format('text/html; charset=utf-8')
    elif filetype == 'jpg':
        http_header = http_header.format('image/jpeg')
    elif filetype == 'js':
        http_header = http_header.format('text/javascript; charset=UTF-8')
    elif filetype == 'css':
        http_header = http_header.format('text/css')
    elif filetype == 'ico':
        http_header = http_header.format('image/x-icon')
    # TO DO: handle all other headers
    client_socket.send(http_header.encode())
    client_socket.send(data.encode())


def validate_http_request(request):
    """ Check if request is a valid HTTP request and returns TRUE / FALSE
    and the requested URL """
    # TO DO: write function
    request = request.split('\r\n')
    request_type = request[0].split(' ')
    if len(request_type) != 3:
        return False, ""
    method, url, version = request_type
    if method != 'GET' or version != 'HTTP/1.1':
        return False, ""
    return True, url


def handle_client(client_socket):
    """
    Handles client requests:
    verifies client's requests are legal HTTP,
    calls function to handle the requests∏
    """
    print('Client connected')
    client_request = client_socket.recv(DEFAULT_BUFLEN).decode()
    valid_http, resource = validate_http_request(client_request)
    if valid_http:
        print('Got a valid HTTP request: ', resource)
        handle_client_request(resource, client_socket)
    else:
        print('Error: Not a valid HTTP request')
        handle_client_request('/INTERNAL_SERVER_ERROR.html', client_socket)
    print(f'Closing connection: {client_socket.getpeername()}')
    client_socket.close()


def main():
    """ main function """
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print(f"Listening for connections on port {PORT}")

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f'New connection received: {client_address}')
            client_socket.settimeout(SOCKET_TIMEOUT)
            handle_client(client_socket)
        except socket.error:
            print('ERROR OCCURRED')

if __name__ == "__main__":
    # Call the main handler function
    main()
