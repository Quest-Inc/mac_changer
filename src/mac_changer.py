#!/usr/bin/env python

import subprocess
# Get arguments and parse them to the user
import optparse
# ReGex expressions
import re


def get_arguments():
    # Parser Obj/ entity that handles user input
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface",
                      help="Interface to change Mac address")

    parser.add_option("-m", "--mac", dest="new_mac",
                      help="new Mac address")

    (options, arguments) = parser.parse_args()

    if not options.interface:
        # code to handle err if no interface
        parser.error("[-] Please specify an interface, "
                     "use --help for more info")
    elif not options.new_mac:
        # code to handle err if no mac
        parser.error("[-] Please specify a new mac, "
                     "use --help for more info")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing Mac address for " + interface + " to " + new_mac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    # capture / read output
    ifconfig_result = subprocess.check_output(["ifconfig",
                                               interface])

    # search through output for alphanumeric(\w) i.e our mac
    mac_address_search_result = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_result)

    if mac_address_search_result:
        # return first result
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read Mac address")


# return and capture
options = get_arguments()

current_mac = get_current_mac(options.interface)
# print current Mac before changing
print("Current Mac = " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] Mac address was successfully changed to " + current_mac)
else:
    print("[-] Mac address did not get changed")
