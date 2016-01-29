#!/usr/bin/env python
#
# Create a VLAN interface on top of a physical interface
# given parameters in code as global vars
# and VLAN / prefix / interface names as arguments
#
# rschmied@cisco.com
#

import argparse
import netaddr
import re
import requests
import sys


HOST = 'ios-xe-mgmt.cisco.com'
PORT = 9443
USER = 'root'
PASS = '1vtG@lw@y'
BASE = 'GigabitEthernet3'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('vlan', help="VLAN number (1-4094)", type=int)
    parser.add_argument('prefix', help="IPv4 or IPv6 prefix")
    parser.add_argument('--insecure', '-k', action='store_true', help="relax SSL verification")
    parser.add_argument('--interface', '-i', default=BASE, help="interface name to use")
    parser.add_argument('--user', '-u', default=USER, help="user name on remote host")
    parser.add_argument('--password', '-p', default=PASS, help="password on remote host")
    parser.add_argument('--port', '-P', default=PORT, help="port on remote host")
	parser.add_argument('--host', '-H', default=HOST, help="remote host")
    args = parser.parse_args()

	# check for valid VLAN ID
	if args.vlan < 1 or args.vlan > 4094:
		parser.print_usage()
		print("invalid VLAN ID %s" % str(args.vlan))
		return -1

	# check for valid prefix
	try:
		ip = netaddr.IPNetwork(args.prefix)
	except netaddr.core.AddrFormatError as e:
		parser.print_usage()
		print(e)
		return -1

	# insecure?
	if args.insecure:
		requests.packages.urllib3.disable_warnings()

	return create_vlan(args.host, args.port, args.user, args.password, args.interface, args.vlan, ip, args.insecure)


if __name__ == '__main__':
	sys.exit(main())
