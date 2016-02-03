# Example of how to get the interface status and parse results via RestConf

# * THIS SAMPLE APPLICATION AND INFORMATION IS PROVIDED "AS IS" WITHOUT WARRANTY
# * OF ANY KIND BY CISCO, EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED
# * TO THE IMPLIED WARRANTIES OF MERCHANTABILITY FITNESS FOR A PARTICULAR
# * PURPOSE, NONINFRINGEMENT, SATISFACTORY QUALITY OR ARISING FROM A COURSE OF
# * DEALING, LAW, USAGE, OR TRADE PRACTICE. CISCO TAKES NO RESPONSIBILITY
# * REGARDING ITS USAGE IN AN APPLICATION, AND IT IS PRESENTED ONLY AS AN
# * EXAMPLE. THE SAMPLE CODE HAS NOT BEEN THOROUGHLY TESTED AND IS PROVIDED AS AN
# * EXAMPLE ONLY, THEREFORE CISCO DOES NOT GUARANTEE OR MAKE ANY REPRESENTATIONS
# * REGARDING ITS RELIABILITY, SERVICEABILITY, OR FUNCTION. IN NO EVENT DOES
# * CISCO WARRANT THAT THE SOFTWARE IS ERROR FREE OR THAT CUSTOMER WILL BE ABLE
# * TO OPERATE THE SOFTWARE WITHOUT PROBLEMS OR INTERRUPTIONS. NOR DOES CISCO
# * WARRANT THAT THE SOFTWARE OR ANY EQUIPMENT ON WHICH THE SOFTWARE IS USED WILL
# * BE FREE OF VULNERABILITY TO INTRUSION OR ATTACK. THIS SAMPLE APPLICATION IS
# * NOT SUPPORTED BY CISCO IN ANY MANNER. CISCO DOES NOT ASSUME ANY LIABILITY
# * ARISING FROM THE USE OF THE APPLICATION. FURTHERMORE, IN NO EVENT SHALL CISCO
# * OR ITS SUPPLIERS BE LIABLE FOR ANY INCIDENTAL OR CONSEQUENTIAL DAMAGES, LOST
# * PROFITS, OR LOST DATA, OR ANY OTHER INDIRECT DAMAGES EVEN IF CISCO OR ITS
# * SUPPLIERS HAVE BEEN INFORMED OF THE POSSIBILITY THEREOF.-->


import sys, re, argparse, netaddr, requests

requests.packages.urllib3.disable_warnings()

URL  = "https://ios-xe-mgmt.cisco.com:9443"
USER = 'root'
PASS = 'C!sc0123'


url       = URL + "/api/operational/interfaces?deep"
headers   = {'content-type': 'application/vnd.yang.data+json', 'accept': 'application/vnd.yang.data+json'}
try:
	result = requests.get(url, auth=(USER,PASS),headers=headers, verify=False)
	#print (result.text)
	#convert response to json format
	r_json=result.json()
	flagDown=0
	for record in r_json["ietf-interfaces:interfaces"]["interface"]: 
		print ("{0:<40}".format("interface:  " + record["name"]), end="")
		print ("{0:<5}".format("ip:"), end="")
		if('address' in record["ietf-ip:ipv4"]):
			print ("{0:<15}".format(record["ietf-ip:ipv4"]["address"][0]["ip"]), end="")
		else:
			print ("{0:<15}".format("No IPv4"), end="")
		print("{0:<9}".format("status:  "), end="")
		print(str(record["enabled"]))
		if(record["enabled"]==False):
			flagDown=1
	print("")
	if(flagDown):
		print ("At least one interface is down")
	else:
		print ("All interfaces are up")
except:
	print ("Exception: " + str(sys.exc_info()[0]) + "  " + str(sys.exc_info[1]))
	print ("Error: " + str(result.status_code), result.text)


