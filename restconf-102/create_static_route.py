#!/usr/bin/python

import argparse
import netaddr
import re
import requests
import sys

# disable warnings from SSL/TLS certificates
requests.packages.urllib3.disable_warnings()


HOST = 'ios-xe-mgmt.cisco.com'
PORT = 9443
USER = 'root'
PASS = '1vtG@lw@y'
BASE = 'GigabitEthernet3'

HOST = '172.16.126.250'
PORT = 8888
USER = 'cisco'
PASS = 'cisco'
BASE = 'GigabitEthernet3'


def create_static(host, port, user, password, interface, ip, insecure):
    """Function that configures static routes on CSR1000V."""
    intfc = re.compile(r'^(\D+)(\d+)$')
    m = intfc.match(interface)
    if m is None:
        print("invalid interface name. Valid example: ", BASE)
        return -1

	data = '''
    {
        "ned:%s": {
            "ip-route-interface-forwarding-list": [
                {
                    "prefix": "%s",
                    "mask": "%s",
                    "interface-name": {
                        "intf": "%s"
                        }
                    }
            ],
            "static": {}
        }
    }
    '''
    print(m.group(1))
    print(m.group(2))
    data = data % (m.group(1), m.group(2))
    print(data)


# create a main() function
def main():
    """Main method that configures static routes on CSR1000V."""
    # url = "https://{h}:{p}/api/running/native/ip/route".format(h=HOST, p=PORT)

    # RESTconf media types for REST API headers
    # headers = {'Content-Type': 'application/vnd.yang.data+json',
    #            'Accept': 'application/vnd.yang.data+json'}

    # this statement performs a PUT on the specified url
    # response = requests.put(url, auth=(USER, PASS), headers=headers, verify=False)
    # print the json that is returned
    # print(response.text)

    parser = argparse.ArgumentParser()
    parser.add_argument('prefix', help="IPv4 or IPv6 Prefix")
    parser.add_argument('--insecure', '-k', action='store_true', help="relax SSL verification")
    parser.add_argument('--interface', '-i', default=BASE, help="interface name to use")
    parser.add_argument('--user', '-u', default=USER, help="user name on remote host")
    parser.add_argument('--password', '-p', default=PASS, help="password on remote host")
    parser.add_argument('--port', '-P', default=PORT, help="port on remote host")
    parser.add_argument('--host', '-H', default=HOST, help="remote host")
    args = parser.parse_args()
    print(args)

    # check for valid prefix
    try:
        ip = netaddr.IPNetwork(args.prefix)
    except netaddr.core.AddrFormatError as e:
        parser.print_usage()
        print(e)
        return -1

    if args.insecure:
        requests.packages.urllib3.disable_warnings()

    return create_static(args.host, args.port, args.user, args.password, args.interface, ip, args.insecure)

if __name__ == '__main__':
    sys.exit(main())
