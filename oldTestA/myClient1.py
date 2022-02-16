from sys import argv
from oldTestA.myProtocol1 import *


def main():
    if len(sys.argv) == 1:
        print("No parameters were received")
        return
    msg = argv[STR]
    print(f'Secret message: {msg}')
    my_packet = create_msg(data=msg, icmp_type=8)
    # my_packet.show()
    send(my_packet)
    try:
        ans = sniff(count=1, lfilter=filter_msg, timeout=TIMEOUT)
        print(f'Ack message: {ans[0][Raw].load.decode()}')
    except:
        print('There is no answer')


if __name__ == '__main__':
    main()
