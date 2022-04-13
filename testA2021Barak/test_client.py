from scapy.all import *
import sys
from oldTestBarak.test_protocol import filter_msg


def main():
    my_code = sys.argv[1]
    my_code = '00' + my_code
    p = IP() / ICMP() / my_code
    send(p)
    try:
        ans = sniff(count=1, lfilter=filter_msg, timeout=3)
        print(str(ans[0][Raw].load.decode())[2:])
    except:
        print("no answer :(")


if __name__ == '__main__':
    main()
