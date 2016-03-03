#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=0 noexpandtab
#
# Create or delete a 802.1Q subinterface on top 
# of a physical interface given parameters in code 
# or via command line. 
#
# - interface name 
# - VLAN ID 
# - prefixes (IPv4 or IPv6)
# - username / password
# - enable / disable SSL
# - insecure (SSL checks on / off)
#
# as arguments. See --help
#
# rschmied@cisco.com
#


from __future__ import print_function
from collections import OrderedDict
import sys, re, argparse, netaddr, requests, json, textwrap


HOST = '192.168.27.10'
PORT = 8008
USER = PASS = 'cisco'
BASE = 'GigabitEthernet3'
AREA = 0
OSPF = 100


def processRequest(cfg, uri, body, what):
	""" do the actual request to the device
		- cfg has all the configuration data (hostname, port, user, ...)
		- uri 
		- body has the data structure or None
		- what is the verb (e.g. GET, PATCH, PUT, ... as a string)
	"""

	if cfg['ssl'] == True:
		proto = 'https' 
	else:
		proto = 'http'

	headers = {
		'content-type': 'application/vnd.yang.data+json', 
		'accept': 'application/vnd.yang.data+json'
	}
	url = "%s://%s:%d%s" % (proto, cfg['host'], cfg['port'], uri)

	if cfg['verbose']:
		print(">>>", what, url)
		if body is not None:
			print(">>>", json.dumps(body, indent=2, sort_keys=False))

	data = None
	if body is not None:
		data=json.dumps(body)

	try:
		r = requests.request(what, url, auth=cfg['auth'], 
			data=data, headers=headers, verify=not cfg['insecure'])
	except requests.exceptions.RequestException as e:
		print(e.message)
		r = requests.Response()
		r.status_code = 500
	else:
		if cfg['verbose']:
			print("<<<", r.status_code)
			if len(r.text) > 0:
				print("<<<", r.text)
	return r


def getV4Prefix(cfg):
	""" get IPv4 prefixes for given interface
		note that current implementation does not give any 
		masks for secondaries except when run with ?deep
	"""

	uri = "/api/running/native/interface/%s/%d.%d/ip/address?deep" % (cfg['name'], cfg['number'], cfg['vlan'])
	r = processRequest(cfg, uri, None, 'GET')
	if r.status_code // 100 == 2:
		return r.json()
	else:
		return None


def createOSPF(cfg):
	""" Create network statements in OSPF process for the provided IPv4 prefixes
		limiting to interface IP as a best practice e.g. 
			'network 192.168.100.1 mask 0.0.0.0 area 0'
		not 'network 192.168.100.0 mask 0.0.0.255 area 0'
	"""

	uri = "/api/running/native/router/ospf"
	networks = list()
	for prefix in cfg['v4prefixes']:
		e = dict(zip(['ip', 'mask', 'area'], [str(prefix.ip), '0.0.0.0', cfg['area-id']]))
		networks.append(e)
	return processRequest(cfg, uri, {'ned:ospf': {'id': cfg['process-id'], 'network': networks}}, 'PATCH')


def deleteOSPF(cfg):
	""" try to delete prefixes by
		- reading IPv4 interface configuration
		- remove prefixes from OSPF config
		- PATCH back

		we do not really care if this fails...
	"""

	addresses = getV4Prefix(cfg)
	if addresses is not None:
		uri = "/api/running/native/router/ospf/%d/network/%s,0.0.0.0"
		if addresses['ned:address'].has_key('primary'):
			prefix = addresses['ned:address']['primary']
			r = processRequest(cfg, uri % (cfg['process-id'], 
				prefix['address']), None, 'DELETE')

		if addresses['ned:address'].has_key('secondary'):
			for prefix in addresses['ned:address']['secondary']:
				r = processRequest(cfg, uri % (cfg['process-id'], 
					prefix['address']), None, 'DELETE')


def createVLAN(cfg):
	""" IOS XE implementation wants keys first in JSON data
		need OrderedDict for this:
		1) key 'name' must come first in JSON data
		2) secondary addresses must have address before mask
	"""

	data = OrderedDict([
		('name', str(cfg['number'])+'.'+str(cfg['vlan'])),
		('encapsulation', { 'dot1Q': { 'vlan-id': cfg['vlan']}})
	])

	if len(cfg['v4prefixes']) > 0:
		prefixes = dict()
		for idx, prefix in enumerate(cfg['v4prefixes']):
			d = OrderedDict(zip(['address', 'mask'], [str(prefix.ip), str(prefix.netmask)]))
			if idx == 0:
				prefixes['primary'] = d
			else:
				if not prefixes.has_key('secondary'):
					prefixes['secondary'] = list()
				prefixes['secondary'].append(d)
		data.update({'ip': {'address': prefixes}})

	if len(cfg['v6prefixes']) > 0:
		prefixes = list()
		for prefix in cfg['v6prefixes']:
			prefixes.append({'prefix': str(prefix)})		
		data.update({'ipv6': {'address': {'prefix-list': prefixes}, 
			'ospf': {'process': [{'id': cfg['process-id'], 'area': cfg['area-id']}]}}})

	uri = "/api/config/native/interface/%s" % (cfg['name'])
	result = processRequest(cfg, uri, {'ned:'+cfg['name']: data}, 'PATCH')
	if result.ok and len(cfg['v4prefixes']) > 0:
		result = createOSPF(cfg)
	return result


def deleteVLAN(cfg):
	""" delete the VLAN interface
	"""

	deleteOSPF(cfg)
	uri = "/api/config/native/interface/%s/%d.%d" % (cfg['name'], cfg['number'], cfg['vlan'])
	return processRequest(cfg, uri, None, 'DELETE')


def main():
	description = textwrap.dedent('''\
	%(prog)s uses RESTCONF to create or delete a 802.1Q subinterface
	on an IOS XE device. There are a few default values at the top
	of the script which can be overriden via command line arguments.

	At least a VLAN ID must be provided. One or more Interface IP 
	address(es) are optional (IPv4 or IPv6).
	''')

	epilog = textwrap.dedent('''\
	Examples:
	%(prog)s 100 172.16.0.1/24
	%(prog)s 100 172.16.0.1/24 172.16.1.1/24
	%(prog)s 200 2001:db8:100::1/64
	%(prog)s 200 2001:db8:100::1/64 2001:db8:200::1/64
	%(prog)s 200 172.16.0.1/24 2001:db8:100::1/64
	%(prog)s 300 --delete --verbose
	%(prog)s --defaults
	''')

	parser = argparse.ArgumentParser(description=description, epilog=epilog, 
		formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('vlan', help="VLAN number (1-4094)", type=int, nargs='?')
	parser.add_argument('prefix', help="IPv4 or IPv6 prefixes", nargs='*')

	parser.add_argument('--verbose', '-v', action='store_true', help="be verbose, print requests and responses")
	parser.add_argument('--delete', '-d', action='store_true', help="delete interface, given prefix(es) ignored")
	parser.add_argument('--defaults', action='store_true', help="show defaults")

	parser.add_argument('--ssl', '-s', action='store_true', help="use SSL")
	parser.add_argument('--insecure', '-k', action='store_true', help="relax SSL verification, only with --ssl")

	parser.add_argument('--user', '-u', default=USER, help="user name on remote host")
	parser.add_argument('--password', '-p', default=PASS, help="password on remote host")

	parser.add_argument('--host', '-H', default=HOST, help="remote host")
	parser.add_argument('--port', '-P', default=PORT, help="port on remote host", type=int)

	parser.add_argument('--interface', '-i', default=BASE, help="interface name to use")
	parser.add_argument('--ospf', '-o', default=OSPF, help="OSPF process ID", type=int)
	parser.add_argument('--area', '-a', default=AREA, help="OSPF area", type=int)
	args = parser.parse_args()

	# show the defaults
	if args.defaults:
		print(textwrap.dedent('''
			Configured defaults are:

			Hostname:        '%s'
			Port:            %d
			Username:        '%s'
			Password:        '%s'
			Interface:       '%s'
			OSPF Process ID: %d
			OSPF Area ID:    %d
			''') % (HOST, PORT, USER, PASS, BASE, OSPF, AREA))
		return 0

	# check for valid VLAN ID
	if args.vlan < 1 or args.vlan > 4094:
		parser.print_usage()
		print("invalid VLAN ID %s" % str(args.vlan))
		return -1

	# check for valid prefixes
	v6prefixes = []
	v4prefixes = []
	for p in args.prefix:
		try:
			ip = netaddr.IPNetwork(p)
		except netaddr.core.AddrFormatError, e:
			parser.print_usage()
			print(e)
			return -1
		if ip.version == 6:
		  v6prefixes.append(ip)
		else:
		  v4prefixes.append(ip)

	# insecure?
	if args.ssl and args.insecure:
		requests.packages.urllib3.disable_warnings()

	# interface name
	m = re.compile(r'^(\D+)(\d+)$').match(args.interface)
	if m is None:
		print("invalid interface name. Valid example: ", BASE)
		return -1

	config = {
		'auth': requests.auth.HTTPBasicAuth(args.user, args.password),
		'ssl': args.ssl, 'insecure': args.insecure, 'verbose': args.verbose,
		'host': args.host, 'port': args.port,
		'name': m.group(1), 'number': int(m.group(2)),
		'vlan': args.vlan, 'v6prefixes': v6prefixes, 'v4prefixes': v4prefixes, 
		'area-id': args.area, 'process-id': args.ospf
	}
	
	if args.delete == True:
		result = deleteVLAN(config)
	else:
		result = createVLAN(config)

	# check status code
	if result is not None and result.status_code // 100 == 2:
		return 0
	else:
		return -1


if __name__ == '__main__':
	sys.exit(main())
