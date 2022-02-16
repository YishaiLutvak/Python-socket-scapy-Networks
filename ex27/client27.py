#   Ex. 2.7 template - client side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020


import socket
from ex27 import protocol27

IP = '127.0.0.1'
# The path + filename where the copy of the screenshot at the client should be saved
SAVED_PHOTO_LOCATION = r'C:\Networks\work\ex27\screen_copy.jpg'
BUCKET_CAPACITY = 1024


def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    # (8) treat all responses
    is_valid_res, res = protocol27.get_msg(my_socket)
    # 5. If server's response is valid, print it
    if is_valid_res:
        print(res)
    else:
        print("Response not valid\n")

    # (10) treat SEND_PHOTO
    if cmd == 'SEND_PHOTO':
        is_valid_res, res = protocol27.get_msg(my_socket)
        if is_valid_res:
            if res.isdigit():
                counter = int(res)
                output_file = open(SAVED_PHOTO_LOCATION, 'wb')
                while counter > 0:
                    counter = counter - BUCKET_CAPACITY
                    output_file.write(my_socket.recv(BUCKET_CAPACITY))
                output_file.close()
                print("Submitted successfully")
            else:
                print(res)
        else:
            print("Response not valid\n")


def main():
    # open socket with the server
    # (2)
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print('before ', my_socket)
    my_socket.connect((IP, protocol27.PORT))
    # print('after ', my_socket)
    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit
    while True:
        cmd = input("Please enter command:\n")
        if protocol27.check_cmd(cmd):
            packet = protocol27.create_msg(cmd)
            my_socket.send(packet)
            handle_server_response(my_socket, cmd)
            if cmd == 'EXIT':
                break
        else:
            print("Not a valid command, or missing parameters\n")

    my_socket.close()


if __name__ == '__main__':
    main()
