"""EX 2.6 client implementation
   Author: Yishai Lutvak 304909864
   Date: 23/10/2021
"""

import socket
from ex26 import protocol26


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("my_socket: " + str(my_socket))
    my_socket.connect(("127.0.0.1", protocol26.PORT))
    print("my_socket: " + str(my_socket))

    while True:
        user_input = input("Enter command\n")
        # Check if user entered a valid command as defined in protocol
        valid_cmd = protocol26.check_cmd(user_input)

        if valid_cmd:  # If the command is valid:
            # 1. Add length field ("RAND" -> "04RAND")
            message = protocol26.create_msg(user_input)
            # 2. Send it to the server
            my_socket.send(message.encode())
            # 3. If command is EXIT, break from while loop
            if user_input == 'EXIT':
                break
            # 4. Get server's response
            is_valid_res, res = protocol26.get_msg(my_socket)
            # 5. If server's response is valid, print it
            if is_valid_res:
                print(res)
            else:
                print("Response not valid\n")
        else:
            print("Not a valid command")

    print("Closing\n")
    my_socket.close()


if __name__ == "__main__":
    main()
