# Ex. 2.7 template - server side
# Author: Barak Gonen, 2017
# Modified for Python 3, 2020

import socket
from ex27 import protocol27
import glob
import os
import subprocess
import shutil
import pyautogui

IP = "0.0.0.0"
# The path + filename where the screenshot at the server should be saved
PHOTO_PATH = r'C:\Networks\work\ex27\screen.jpg'


def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    # (6)
    # Use protocol.check_cmd first
    my_list = cmd.split(" ")
    valid = protocol27.check_cmd(cmd)
    command = my_list[0]
    params = my_list[1:]

    if not valid:
        return False, command, params

    elif command in ("TAKE_SCREENSHOT", "SEND_PHOTO", "EXIT"):
        return True, command, params

    # Then make sure the params are valid
    elif command == "DIR":
        if os.path.isdir(params[0]):
            return True, command, params
        else:
            return False, command, params

    elif command in ("DELETE", "COPY", "EXECUTE"):
        if os.path.isfile(params[0]):
            # Check if the destination folder does not exist
            if command == 'COPY' and not os.path.isdir(params[1][:params[1].rfind('\\')]):
                return False, command, params
            return True, command, params
        else:
            return False, command, params


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data
    """
    # (7)
    response = ''

    if command == 'DIR':
        files_list = glob.glob(params[0] + r'\*.*')
        response = str(files_list)

    elif command == 'DELETE':
        os.remove(params[0])
        response = 'The file deleted'

    elif command == 'COPY':
        try:
            shutil.copy(params[0], params[1])
            response = 'The copy was successful'
        except OSError:
            response = 'Copy failed'

    elif command == 'EXECUTE':
        try:
            subprocess.call(params[0])
            response = 'The execution was successful'
        except OSError:
            response = 'Execution failed'

    elif command == 'TAKE_SCREENSHOT':
        image = pyautogui.screenshot()
        image.save(PHOTO_PATH)
        response = 'The execution of screenshot successful'

    elif command == 'SEND_PHOTO':
        response = 'Your request has been accepted'

    return response


def main():
    # open socket with client
    # (1)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, protocol27.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")
    # handle requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = protocol27.get_msg(client_socket)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:
                # (6)
                # prepare a response using "handle_client_request"
                response = handle_client_request(command, params)
                # add length field using "create_msg"
                reply = protocol27.create_msg(response)
                # send to client
                client_socket.send(reply)
                if command == 'SEND_PHOTO':
                    # (9)
                    try:
                        # Send the data itself to the client
                        f = open(PHOTO_PATH, 'rb')
                        file_content = f.read()
                        # print('file content: ', file_content)
                        length = len(file_content)
                        reply = protocol27.create_msg(str(length))
                        # send to client
                        client_socket.send(reply)
                        client_socket.send(file_content)
                        f.close()
                    except FileNotFoundError:
                        reply = protocol27.create_msg("The screenshot operation must be performed first")
                        client_socket.send(reply)
                if command == 'EXIT':
                    break
            else:
                # prepare proper error to client
                response = 'Bad command or parameters'
                # send to client
                reply = protocol27.create_msg(response)
                client_socket.send(reply)
        else:
            # prepare proper error to client
            response = 'Packet not according to protocol'
            # send to client
            reply = protocol27.create_msg(response)
            client_socket.send(reply)
            # Attempt to clean garbage from socket
            client_socket.recv(1024)

    # close sockets
    print("Closing connection")
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()
