"""EX 2.6 server implementation
   Author: Yishai Lutvak 304909864
   Date: 23/10/2021
"""

import socket
from ex26 import protocol26


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol26.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("server_socket: " + str(server_socket))
    print("client_socket: " + str(client_socket))
    print("Client connected")

    while True:
        # Get message from socket and check if it is according to protocol
        valid_msg, cmd = protocol26.get_msg(client_socket)
        if valid_msg:
            # 1. Print received message
            print("Client sent: " + cmd)

            # 2. Check if the command is valid
            is_valid_cmd = protocol26.check_cmd(cmd)

            # 3. If valid command - create response
            if is_valid_cmd:
                response = protocol26.create_server_rsp(cmd)
            else:
                response = "Wrong command"
        else:
            response = "Wrong protocol"
            client_socket.recv(1024)  # Attempt to empty the socket from possible garbage
        # Handle EXIT command, no need to respond to the client
        if response is None:
            break
        # Send response to the client
        reply = protocol26.create_msg(response)
        client_socket.send(reply.encode())
    print("Closing\n")

    # Close sockets
    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    main()
