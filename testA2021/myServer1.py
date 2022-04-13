from testA2021.myProtocol1 import *


def main():
    p = sniff(count=1, lfilter=filter_msg)
    p[0].show()
    secret = p[0][Raw].load.decode()
    print("Secret message: " + secret)
    result = calc(secret)
    dst = p[0][IP].src
    print(dst)
    res = create_msg(data=result, icmp_type=0, ip_dst=dst)
    res.show()
    send(res)
    print("Ack message: " + result)


if __name__ == '__main__':
    main()
