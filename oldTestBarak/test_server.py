from scapy.all import *
from oldTestBarak.test_protocol import filter_msg, my_cul


def main():
    msg = sniff(count=1, lfilter=filter_msg)
    num = msg[0][Raw].load.decode()
    num = num[2:]
    print("the agent sent: " + str(num))
    res = '00' + str(my_cul(num))
    print("we are sending him back: " + str(res)[2:])
    dst_IP = msg[0][IP].src  # added by Barak, instead of fixed IP for response, use sender's IP
    answer = IP(dst=dst_IP) / ICMP(type=0) / res
    send(answer)


if __name__ == '__main__':
    main()
