#!/usr/bin/env python

import argparse
import netaddr
import random
import sys

FILE = 'configuration_data.py'
BASE = '1.0.0.0/19'
LENGTH = 31


def randomizer(filename):
    """Function to randomize example configuration data."""
    pass


def random_vlan():
    """Return random VLAN ID."""
    return random.choice(range(1, 4095))


def random_address(base, length):
    """Return a random route based on a base prefix and prefix length."""
    ip = netaddr.IPNetwork(base)
    addresses = list(ip.subnet(length))
    return random.choice(addresses)


def main():
    """Main method to randomize example configuration data."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default=FILE, help="name of file to which we write data")
    parser.add_argument('--base', '-b', default=BASE, help="base prefix to subnet")
    parser.add_argument('--length', '-l', default=LENGTH, help="prefix length of resulting subnets")
    args = parser.parse_args()
    # with open(args.filename, 'w') as f:
    #     print(f)
    print('################################################')
    print('Here is an example way to run the script: ')
    print("python create_subinterface.py {v} {r} --insecure".format(v=random_vlan(), r=random_address(BASE, LENGTH)))
    print('################################################')


if __name__ == '__main__':
    sys.exit(main())
