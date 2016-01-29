#!/usr/bin/python
#
# Get configured interfaces using RESTconf
#
# darien@sdnessentials.com
#
import requests
import sys


requests.packages.urllib3.disable_warnings()

HOST = 'ios-xe-mgmt.cisco.com'
PORT = 9443
USER = 'root'
PASS = 'C!sc0123'


def get_configured_interfaces():
    """Retrieving state data (routes) from RESTconf."""
    url = "https://{h}:{p}/api/running/interfaces".format(h=HOST, p=PORT)
    # RESTconf media types for REST API headers
    headers = {'Content-Type': 'application/vnd.yang.data+json',
               'Accept': 'application/vnd.yang.data+json'}
    # this statement performs a GET on the specified url
    response = requests.get(url, auth=(USER, PASS),
                            headers=headers, verify=False)

    # return the json as text
    return response.text


def main():
    """Simple main method calling our function."""
    interfaces = get_configured_interfaces()

    # print the json that is returned
    print(interfaces)

if __name__ == '__main__':
    sys.exit(main())
