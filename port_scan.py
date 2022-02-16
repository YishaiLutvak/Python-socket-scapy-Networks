from scapy.all import *

SERVER_IP = 'www.google.com'
START_PORT = 440  # 75
END_PORT = 450  # 84

open_ports = []
p = IP(dst=SERVER_IP)/TCP(flags='S')
for port in range(START_PORT, END_PORT + 1):
    p[TCP].dport = port
    print(f'Testing port: {port}')
    r = sr1(p, timeout=0.5, verbose=False)
    try:
        if r[TCP].flags == 'SA':
            print(f'Found open port {port}')
            open_ports.append(port)
    except:
        print("pass")
        pass

print(open_ports)
