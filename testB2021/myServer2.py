from testB2021.myProtocol2 import *


def handles_file_not_found(file_name, ip_dst) -> bool:
    """
    :parameter file_name
    :parameter ip_dst
    :return True if file not found
    """
    if not os.path.isfile(file_name):
        my_msg = ERROR_MESSAGES[ERROR_NOT_FOUND]
        error_pkt = create_msg(my_msg, ERROR_NOT_FOUND, ip_dst)
        send_3_times(error_pkt)
        print(f"Error occurred 😞 {my_msg}")
        return True
    return False


def handles_overflow_sections(num_of_sections, ip_dst) -> bool:
    """
    :parameter num_of_sections
    :parameter ip_dst
    :return True if num of sections big than MAX_NUM_SECTIONS
    """
    if num_of_sections > MAX_NUM_SECTIONS:
        my_msg = ERROR_MESSAGES[ERROR_BIG_FILE]
        error_pkt = create_msg(my_msg, ERROR_BIG_FILE, ip_dst)
        send_3_times(error_pkt)
        print(f"Error occurred 😞 {my_msg}")
        return True
    return False


def round_up(numerator, denominator) -> int:
    """
    :parameter numerator
    :parameter denominator
    :return round up of the result
    """
    return int(numerator/denominator) + (numerator % denominator > 0)


def min_value(num1, num2) -> int:
    """
    :parameter num1
    :parameter num2
    :return minimum
    """
    return num1 if num1 < num2 else num2


def send_control(num_of_sections, list_messages, ip_dst) -> None:
    """
    :parameter num_of_sections
    :parameter list_messages
    :parameter ip_dst
    Responsible for sending the file to the client
    """
    current = 0  # Initializes the package number of packet the client expects to receive to 0
    while True:
        # Gets the maximum packet value that should be sent in the current iteration
        border = min_value(current + WINDOW, num_of_sections)

        # Sends several packages as the window size
        for i in range(current, border):
            special_send(list_messages[i])

        # Trying to get a response from the client
        p = sniff(count=1, lfilter=filter_msg, timeout=TIMEOUT)

        # If no response is received a repeat to the beginning of the loop
        # and a repeat transmission operation
        if len(p) == 0:
            continue

        current = p[0][IP].tos

        # If all the pieces of the file have been sent the loop should end
        if current == num_of_sections:
            send_until_ack(create_msg("Send finish code", MY_FIN, ip_dst))
            print("File is send successfully 🙂")
            return

        # If first ack lost along the way
        if current == SEND_FILE:
            another_ack = create_ack(ip_dst)
            special_send(another_ack)


def main():
    pkt = sniff(count=1, lfilter=filter_msg)
    ip_dst = pkt[0][IP].src
    first_ack = create_ack(ip_dst)
    special_send(first_ack)
    file_name = str(pkt[0][Raw].load.decode())
    if handles_file_not_found(file_name, ip_dst):
        return

    f = open(file_name, 'rb')
    file_content = f.read()
    length = len(file_content)
    num_of_sections = round_up(length, BUCKET_CAPACITY)
    if handles_overflow_sections(num_of_sections, ip_dst):
        return

    list_messages = create_short_messages(file_content, num_of_sections, ip_dst)
    send_control(num_of_sections, list_messages, ip_dst)


if __name__ == '__main__':
    main()
