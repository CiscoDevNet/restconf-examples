#!/usr/bin/python

import re


def main():
    """Open a file called static-routes.txt and print each line that matches a REGEX for a static route."""
    with open('static-routes.txt', 'r') as static_routes:
        for route in static_routes:
            if re.match('^ip route (\d{1,3}\.){3}\d{1,3} '
                        '(\d{1,3}\.){3}\d{1,3} (\d{1,3}\.){3}\d{1,3}$', route):
                print(route.rstrip())

if __name__ == '__main__':
    main()
