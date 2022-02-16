import socket

my_input = input("Enter something\n")
my_socket = socket.socket()
my_socket.connect(("127.0.0.1", 8820)) # "192.168.43.95"
my_socket.send(my_input.encode())
data = my_socket.recv(1024).decode()
if data == '':
    print("There is no connection")
else:
    print("The server sent " + data)

my_socket.close()
