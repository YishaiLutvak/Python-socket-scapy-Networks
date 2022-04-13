from sys import argv
from testB2021.myProtocol2 import *
SAVED_FILE_LOCATION = r'C:\Networks\work\testB2021\my_secret_copy.png'


# parameter for test: C:\Networks\work\testB2021\my_secret.png


def acceptance_control(file_name) -> tuple:
    """
    Manages the receipt of the file
    :parameter file_name - name of file
    :return tuple of (bool, int),
    bool - if all file is accepted,
    int - tos field - value of status of the sending
    """
    current = 0
    output_file = open(file_name, 'wb')
    while True:
        # Sends to server the package number it expects to receive
        response = create_msg(f"Expected packet: {current}", current, SERVER_IP)
        special_send(response)

        # Trying to get pieces from the server
        packets = sniff(count=WINDOW, lfilter=filter_msg, timeout=TIMEOUT)
        length_sniff = len(packets)

        # If no messages are received return to the beginning of the loop
        # and resend the package number he expects to receive
        if length_sniff == 0:
            continue

        for i in range(length_sniff):
            tos_value = packets[i][IP].tos
            print("tos_value:", tos_value)

            # If an error code was received
            if tos_value in (ERROR_BIG_FILE, ERROR_NOT_FOUND):
                output_file.close()
                return False, tos_value

            # If a sending end code was received
            if tos_value == MY_FIN:
                output_file.close()
                return True, tos_value

            # If the package received is the package we expected to receive
            if tos_value == current:
                output_file.write(packets[i][Raw].load)
                current += 1
                print("current:", current)

            # If the package received is the package we expected to receive
            elif tos_value > current:
                print("Break loop because current packet lost")
                break


def main():
    if len(argv) == 1:
        print("No parameter was received")
        return

    file_name = argv[READ_FILE]
    pkt = create_msg(file_name, SEND_FILE, SERVER_IP)
    is_received_ack = send_until_ack(pkt)
    if not is_received_ack:
        print("The server is not responding 😞")
        return

    successfully, my_tos = acceptance_control(SAVED_FILE_LOCATION)
    if not successfully:
        print(f"Error occurred 😞 {ERROR_MESSAGES[my_tos]}")
        return

    my_ack = create_ack(SERVER_IP)
    send_3_times(my_ack)
    print("File is received successfully 🙂")


if __name__ == '__main__':
    main()
