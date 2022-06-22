#! /usr/bin/env python
import optparse # argparse for newer version
import scapy.all as scapy

# to get the ip and macs connected to same network

def get_args():
    parser = optparse.OptionParser() #argparse.ArgumentParser()
    parser.add_option("-t", "--target", dest="target", help=" Target ip/ip range")
    (options, argumenst) = parser.parse_args()  # options = parser.parse_args()  
    return options

def scan(ip):
    arp_req = scapy.ARP()
    #print(arp_req.summary())
    #arp_req.show()
    arp_req.pdst = ip # or arp_req = scapy.ARP(pdst=ip)
    #scapy.ls(scapy.ARP()) # its just to list all the variabkles and objects that we can access of a particular class
    # scapy.arping(ip);
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_brdcast = broadcast/arp_req
    answered_list, unanswered = scapy.srp(arp_brdcast, timeout=1, verbose=False) #verbose is set t false to hide extra data
    result_list = []
    for i in answered_list:
        dictio = {"ip": i[1].psrc, "mac": i[1].hwsrc}
        result_list.append(dictio)
    return result_list

    # print(answered_list.summary())
    # print("IP\t\t\tMac address")
    # for i in answered_list:
    #     print(i)
    #     print(i[1])
    #     print(i[1].show())
    #     print(i[1].psrc)
    #     print(i[1].hwsrc)

def print_results(result_list):
    print("IP\t\t\tMac address\n-----------------------------------------------------------------------")
    for i in result_list:
        print(i["ip"]+"\t\t"+i["mac"])


options = get_args()
result_list = scan(options.target)
print_results(result_list)
