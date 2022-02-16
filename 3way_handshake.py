from scapy.all import *
syn_segment = TCP(dport=80,sport=55555,seq=123456,flags='S')
syn_packet = IP(dst='www.google.com')/syn_segment
syn_ack_packet = sr1(syn_packet)
ack_num = syn_ack_packet[TCP].seq + 1
ack_segment = TCP(dport=80,sport=55555,seq=123457,ack=ack_num,flags='A')
ack_packet = IP(dst='www.google.com')/ack_segment
send(ack_packet)