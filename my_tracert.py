from scapy.all import *

# input to text: www.themarker.com

LIMIT = 128
destination = sys.argv[1]
print(f"destination:{destination}")
i = 1
while True:
    print(f"ttl={i}")
    print()
    packet = IP(ttl=i, dst=destination) / ICMP() / Raw(load='Yishai Lutvak')
    packet.show()
    print()
    print(str(packet[Raw].load.decode()))
    try:
        res = sr1(packet, verbose=0, timeout=2)
        res.show()
        print()
        print(res[IP].src)
        print()
        if res[ICMP].type == 0 or i == LIMIT:
            break
    except:
        print("no response")
    i += 1
