#   Ex. 2.7 template - protocol


LENGTH_FIELD_SIZE = 4
PORT = 8820


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\\work\\file.txt is good, but DELETE alone is not
    """
    # (3)
    my_list = data.split(" ")
    if my_list[0] in ("DIR", "DELETE", "EXECUTE") and len(my_list) == 2:
        return True
    elif my_list[0] == "COPY" and len(my_list) == 3:
        return True
    elif my_list[0] in ("TAKE_SCREENSHOT", "SEND_PHOTO", "EXIT") and len(my_list) == 1:
        return True
    return False


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """
    # (4)
    length = str(len(data))
    zfill_length = length.zfill(LENGTH_FIELD_SIZE)
    # print (data)
    message = zfill_length + data
    # print (message)
    return message.encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """
    # (5)
    length = my_socket.recv(LENGTH_FIELD_SIZE).decode()
    if length.isdigit():
        try:
            message = my_socket.recv(int(length)).decode()
            return True, message
        except UnicodeDecodeError:
            print('Path must be only in English\n')
            return False, "Error"
    return False, "Error"
