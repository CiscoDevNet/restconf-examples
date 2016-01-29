#!/usr/bin/python

# import the requests library
import requests
import sys

# disable warnings from SSL/TLS certificates
requests.packages.urllib3.disable_warnings()

# use the IP address or hostname of your CSR1000V
HOST = 'ios-xe-mgmt.cisco.com'
# use the HTTPS port for RESTconf on your CSR1000V
PORT = 9443
# use your user credentials to access the CSR1000V
USER = 'root'
PASS = 'C!sc0123'


# create a main() method
def main():
    '''
    Main method that retrieves the hostname from CSR1000V via RESTconf
    '''

    # url string to issue GET request
    url = "https://{h}:{p}/api/running/native/hostname".format(h=HOST, p=PORT)

    # RESTconf media types for REST API headers
    headers = {'Content-Type': 'application/vnd.yang.data+json',
               'Accept': 'application/vnd.yang.data+json'}
    # this statement performs a GET on the specified url
    response = requests.get(url, auth=(USER, PASS),
                            headers=headers, verify=False)

    # print the json that is returned
    print(response.text)

if __name__ == '__main__':
    sys.exit(main())
