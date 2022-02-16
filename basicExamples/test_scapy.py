from scapy.all import *

p = sniff(2)
p[0].show()

