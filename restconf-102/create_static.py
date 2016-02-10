#!/usr/bin/python
#
# Create a static route on CSR1000V
# given parameters in code as global vars
# and route / nexthop or interface names as arguments
#
# darien@sdnessentials.com
#
import argparse
import netaddr
import requests
import sys


HOST = 'ios-xe-mgmt.cisco.com'
PORT = 9443
USER = 'root'
PASS = 'C!sc0123'
BASE = 'GigabitEthernet3'


def create_static(host, port, user, password, route, nexthop, insecure):
    """Function to create a static route on CSR1000V."""

    url = "https://{h}:{p}/api/running/native/ip/route".format(h=HOST, p=PORT)
    headers = {'content-type': 'application/vnd.yang.data+json',
               'accept': 'application/vnd.yang.data+json'}
    try:
        result = requests.patch(url, auth=(USER, PASS), data=data,
                                headers=headers, verify=not insecure)
    except Exception:
        print(str(sys.exc_info()[0]))
        return -1

    return result.text

    if result.status_code == 201:
        return 0

    # somethine went wrong
    print(result.status_code, result.text)
    return -1


def main():
    """Main method to create static route."""
    parser = argparse.ArgumentParser()
    parser.add_argument('route', help="static route (IPv4)")
    parser.add_argument('nexthop', help="nexthop for (Interface or IPv4)")
    parser.add_argument('--insecure', '-k', action='store_true', help="relax SSL verification")
    parser.add_argument('--user', '-u', default=USER, help="user name on remote host")
    parser.add_argument('--password', '-p', default=PASS, help="password on remote host")
    parser.add_argument('--port', '-P', default=PORT, help="port on remote host")
    parser.add_argument('--host', '-H', default=HOST, help="remote host")
    args = parser.parse_args()

    # check for valid prefix
    try:
        ip = netaddr.IPNetwork(args.route)
    except netaddr.core.AddrFormatError as e:
        parser.print_usage()
        print(e)
        return -1

    # insecure?
    if args.insecure:
        requests.packages.urllib3.disable_warnings()

        return create_static(args.host, args.port, args.user, args.password,
                             args.route, args.nexthop, args.insecure)

if __name__ == '__main__':
    sys.exit(main())
