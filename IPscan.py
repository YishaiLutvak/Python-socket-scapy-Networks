from scapy.all import *

NETWORK_ID = '192.168.43.'

for i in range(255):
    print(i)
    address = NETWORK_ID + str(i)
    p = ARP(pdst=address)
    try:
        r = sr1(p, verbose=0, timeout=0.5)
        print(str(r[ARP].psrc), str(r[ARP].hwsrc))
    except:
        pass
