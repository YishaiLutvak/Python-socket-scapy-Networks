"""
    Exam1 server implementation
    Author: Yishai Lutvak 304909864
    Date: 4/2/2022
"""

from myTest2022.myTestProtocol import *


def func1(param1):
    """:parameter"""
    pass


def func2(param1):
    """:parameter"""
    pass


def func3(param1):
    """:parameter"""
    pass


def main():
    """
    """
    p = sniff(count=1, lfilter=filter_msg)
    # p[0].show()
    secret = str(p[0][Raw].load.decode())
    print("Secret message: " + secret)
    ack = calc(secret)
    dst = p[0][IP].src
    res = create_msg(data=ack, icmp_type=0, ip_dst=dst)
    # res.show()
    send(res)
    print("Ack message: " + ack)


if __name__ == "__main__":
    main()
