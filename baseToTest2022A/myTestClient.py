"""
    Exam1 client implementation
    Author: Yishai Lutvak 304909864
    Date: 4/2/2022
"""

from myTest2022.myTestProtocol import *


def main():
    length_argv = len(sys.argv)
    print("length_argv:", length_argv)
    print("sys.argv:", sys.argv)
    if length_argv == 1:
        print("No parameters were received")
        return
    msg = sys.argv[READ_FILE]
    print(f'Secret message: {msg}')
    my_packet = create_msg(data=msg, icmp_type=8)
    # my_packet.show()
    send(my_packet)
    try:
        ans = sniff(count=1, lfilter=filter_msg, timeout=TIMEOUT, prn=my_prn)
        print(f'Ack message: {str(ans[0][Raw].load.decode())}')
    except:
        print('There is no answer')


if __name__ == '__main__':
    main()
