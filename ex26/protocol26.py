"""EX 2.6 protocol implementation
   Author: Yishai Lutvak 304909864
   Date: 23/10/2021
"""


from datetime import datetime
import random

LENGTH_FIELD_SIZE = 2
PORT = 8820


def check_cmd(data):
    """Check if the command is defined in the protocol (e.g RAND, NAME, TIME, EXIT)"""
    if data in ('RAND', 'NAME', 'TIME', 'EXIT'):
        return True
    return False


def create_msg(data):
    """Create a valid protocol message, with length field"""
    length = str(len(data))
    zfill_length = length.zfill(2)
    message = zfill_length + data
    return message


def get_msg(my_socket):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """
    length = my_socket.recv(2).decode()
    if length.isdigit():
        message = my_socket.recv(int(length)).decode()
        return True, message
    return False, "Error"


def create_server_rsp(cmd):
    """Based on the command, create a proper response"""
    if cmd == 'EXIT':
        return
    elif cmd == 'NAME':
        return "Name of server = Super_server"
    elif cmd == 'TIME':
        now = datetime.now()  # datetime object containing current date and time
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")  # dd/mm/YY H:M:S
        return "date and time = " + dt_string
    else:
        return "random integer = " + str(random.randrange(10)+1)
