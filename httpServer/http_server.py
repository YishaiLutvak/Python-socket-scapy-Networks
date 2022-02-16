# Ex 4.4 - HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants
# Yishai Lutvak 304909864


# tests:
# 200 : "localhost" or "localhost/index.html"
# 302 : "localhost/folder1/inner_index.html" or "localhost/folder2/inner_index.html"
# 403 : "localhost/forbidden1.html" or "localhost/forbidden2.html"
# 404 : "localhost/there_is_no.html"
# 500 : "localhost/BPR.rar"


# TO DO: import modules - V
import socket
import os

# TO DO: set constants - V
SOCKET_TIMEOUT = 0.1
IP = "0.0.0.0"
PORT = 80
DEFAULT_DIR = 'C:/Networks/work/httpServer/webroot/'
DEFAULT_URL = DEFAULT_DIR + 'index.html'
REDIRECTION_DICTIONARY = {
    'folder1/inner_index.html': 'index.html',
    'folder2/inner_index.html': 'index.html'
}
FORBIDDEN_PAGES = ('forbidden1.html', 'forbidden2.html')
HTTP_VERSION = 'HTTP/1.1'
BUCKET = 1024


def header_content_type(file_type: str):
    """
    Get Content-type header according to the suffix of file
    """
    if file_type in ('html', 'txt'):
        return 'Content-Type: text/html; charset=utf-8\r\n'
    elif file_type in ('jpg', 'ico'):
        return'Content-Type: image/jpeg\r\n'
    elif file_type == 'js':
        return 'Content-Type: text/javascript; charset=UTF-8\r\n'
    elif file_type == 'css':
        return 'Content-Type: text/css\r\n'


def get_file_data(file_name, file_type):
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
    # TO DO : add code that given a resource (URL and parameters) generates the proper response - V
    if resource == '':
        url = DEFAULT_URL
    else:
        url = DEFAULT_DIR + resource  # add "C:/Networks/work/webroot/" before url
        print('resource:', resource)
    print('url:', url)
    # check if URL had been redirected, not available or other error code - V
    if resource in REDIRECTION_DICTIONARY:
        print('302 Moved Temporarily')
        reply = HTTP_VERSION + ' 302 Found\r\nLocation: /' + REDIRECTION_DICTIONARY[resource] + '\r\n\r\n'
        http_response = reply.encode()
        client_socket.send(http_response)
        return
    if not os.path.isfile(url):
        print('404 Not Found')
        reply = HTTP_VERSION + ' 404 Not Found\r\n\r\n'
        http_response = reply.encode()
        client_socket.send(http_response)
        return
    if resource in FORBIDDEN_PAGES:
        print('403 Forbidden')
        reply = HTTP_VERSION + ' 403 Forbidden\r\n\r\n'
        http_response = reply.encode()
        client_socket.send(http_response)
        return
    # extract requested file tupe from URL (html, jpg etc) - V
    file_type = url[url.rfind('.') + 1:]  # slice by the last dot in order to get suffix of file
    print('file type: ', file_type)
    # TO DO: read the data from the file - V
    data = get_file_data(url, file_type)
    if not data:  # if suffix of file is unrecognized data is None
        print('File type not detected')
        handle_status_500(client_socket)
        return
    print('200 OK')
    http_header = HTTP_VERSION + ' 200 OK\r\n'  # if all right return status ok
    # add Content-Length header to the header
    length = len(data)
    http_header += 'Content - Length: ' + str(length) + '\r\n'
    complete_header = http_header + header_content_type(file_type) + '\r\n'
    http_response = complete_header.encode() + data
    client_socket.send(http_response)


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    """
    first_line = request[:request.find("\r\n")]  # slice by first "\r\n" to get first line
    print('first line: ', first_line)
    items = first_line.split()
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
        # TO DO: insert code that receives client request - V
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


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
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
