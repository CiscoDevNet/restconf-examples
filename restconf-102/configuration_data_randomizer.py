#!/usr/bin/env python
#
# Randomize a VLAN ID and address to run
# create_subinterface.py against the CSR1000V
# in the Always On SandBox
#
# darien@sdnessentials.com
#

import argparse
import netaddr
import random
import sys

# base prefix to subnet
BASE = '1.0.0.1/19'
# prefix length of resulting subnets
LENGTH = 31


def random_vlan():
    """Return random VLAN ID."""
    return random.choice(range(1, 4095))


def random_address(base, length):
    """Return a random route based on a base prefix and target prefix length."""
    ip = netaddr.IPNetwork(base)
    addresses = list(ip.subnet(length))
    return random.choice(addresses)


def main():
    """Main method to randomize example configuration data."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', '-b', default=BASE, help="base prefix to subnet")
    parser.add_argument('--length', '-l', default=LENGTH, help="prefix length of resulting subnets", type=int)
    args = parser.parse_args()
    print('################################################')
    print('Here is an example way to run the script: ')
    print("python3 create_subinterface.py {v} {r} --insecure".format(v=random_vlan(), r=random_address(args.base, args.length)))
    print('################################################')


if __name__ == '__main__':
    sys.exit(main())
