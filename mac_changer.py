#! /usr/bin/env python


#to change mac address of our device

import subprocess
# can by hijacked by the user as we take input and place it straightaway in subprocess
# as the user might give input as "eth0;ls;" which will mark eth0 as one command
# and ls as other and everything after ls as other so the code will be doing whats its not made for
# to avoid this we will use another method
def buggy_func(mac,interface):


    subprocess.call("ifconfig "+interface+" down",shell=True)
    subprocess.call("ifconfig "+interface+" hw ether "+mac,shell=True)
    subprocess.call("ifconfig "+interface+" up",shell=True)
#method 2
# it uses subprocess.call(["ifconfig",interface,"down"])
# basically we have to write all the space separtated words as items of a list.
def not_so_buggy_func(mac,interface):

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac])
    subprocess.call(["ifconfig", interface, "up"])
def manual_input():
    mac = input("new mac > ")
    interface = input("interface > ")
    print("[+] changing MAC addres for " + interface + " to " + mac)
    buggy_func(mac,interface)
    not_so_buggy_func(mac,interface)
#method3
import optparse #to get cli arguments
def cli_args():

    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface of which the MAC address has to be changed")
    parser.add_option("-m", "--mac", dest="mac", help="New MAC address")

    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] please specify the interface use --help for help")
    if not options.mac:
        parser.error("[-] please specify the new mac use --help for help")
    return options
#end method3
#we are checking at the end of every exceution that whether our code was successful in chnagiung mac address or not
# we are going automarte this process as well
import re

def print_mac(interface):
    #not_so_buggy_func(options.mac, options.interface)
    ifcon_out = subprocess.check_output(["ifconfig",interface])
    # now to capture mac address we are going to capture mac address from output
    # to mkae regex rule goto "pythex"
    search_result = re.search(r"/w/w:/w/w:/w/w:/w/w:/w/w:/w/w", ifcon_out)
    if search_result:
        return search_result.group(0)
    else:
        print("could not read mac address")

options = cli_args()
cur_mac = print_mac(options.interface)
print("current mac" + str(cur_mac))
not_so_buggy_func(options.mac, options.interface)
cur_mac = print_mac(options.interface)
if cur_mac == options.mac:
    print("mac address successfully got changed to: "+cur_mac)
else:
    print("could not chnage mac address")