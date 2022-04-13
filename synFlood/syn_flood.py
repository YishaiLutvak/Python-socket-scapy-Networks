# Yishai Lutvak
#
# The identification of the suspicious IP addresses is done according to
# the number of times an address received syn_ack and did not reply afterwards ack

from scapy.all import *

NORMAL_DIFFERENCE = 0


def create_dict_of_ip_and_synack_less_ack(file_name):
    """
    Creates a dictionary of ip and the difference between dst_syn_ack and src_ack
    :parameter file_name - The name of file to read as pcapFile
    :return dict of ip keys and dst_syn_ack Less src_ack number value
    """
    my_dict = {}  # {key = ip: value = dst_syn_ack less src_ack}
    # open pcap file
    pcap_file = rdpcap(file_name)
    # print('opened')
    for pkt in pcap_file:
        if pkt[TCP].flags == 'SA':
            my_dict[pkt[IP].dst] = 1 if pkt[IP].dst not in my_dict else my_dict[pkt[IP].dst] + 1
        if pkt[IP].src in my_dict and pkt[TCP].flags == 'A':
            my_dict[pkt[IP].src] = my_dict[pkt[IP].src] - 1
        # pkt.show()
    return my_dict


def write_list_to_file(file_name, my_list):
    """
    Writes the list to the file
    :parameter file_name - File name to write
    :parameter my_list
    """
    # create text file to write attackers IP
    attacker_list_file = open(file_name, 'w')
    for item in my_list:
        attacker_list_file.write(f'{item}\n')
    attacker_list_file.close()


def main():
    """
    Finds suspected IP addresses in syn_flood attack and writes them to a file
    """
    syn_less_ack_dict = create_dict_of_ip_and_synack_less_ack("SynFloodSample.pcap")
    # print(syn_less_ack_dict)
    ip_filter_list = [k for (k, v) in syn_less_ack_dict.items() if v > NORMAL_DIFFERENCE]
    write_list_to_file("attackersListFiltered.txt", ip_filter_list)


if __name__ == "__main__":
    main()
