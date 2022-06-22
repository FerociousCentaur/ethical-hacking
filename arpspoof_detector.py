#! /usr/bin/env python
#import optparse # argparse for newer version
import scapy.all as scapy
# we wil have to use pip install scapy_http to filter http requests

def get_mac(ip):
    arp_req = scapy.ARP()
    #print(arp_req.summary())
    #arp_req.show()
    arp_req.pdst = ip # or arp_req = scapy.ARP(pdst=ip)
    #scapy.ls(scapy.ARP()) # its just to list all the variabkles and objects that we can access of a particular class
    # scapy.arping(ip);
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_brdcast = broadcast/arp_req
    answered_list, unanswered = scapy.srp(arp_brdcast, timeout=1, verbose=False) #verbose is set t false to hide extra data
    return answered_list[0][1].hwsrc


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_packets)#, filter="port 80")#filter="udp" # or tcp or arp # it doesnt allow http
    # we wil have to use pip install scapy_http to filter http requests


def process_packets(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = get_mac(packet[scapy.ARP].hwsrc)
            if real_mac != response_mac:
                print("[+] You are under attack!!!!!!")
        except IndexError:
            pass


sniff("etho")


#todo ~echo 1 > /proc/sys/net/ipv4/ip_forward to allow kali forward the requests