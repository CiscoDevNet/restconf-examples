# Create VLAN Interfaces on IOS XE


## What it does
This script uses the IOS XE NED model to achieve something 'useful'. The idea here is to provision (or delete) a VLAN interface on an existing (physical) interface that is connected to an upstream switch via a 802.1Q trunk.

This could be used, for example, to provision a /30 subnet to run a virtual machine or a container e.g. running a NFV on a host that is connected to the router (or a switch) that will get the VLAN interface provisioned using this script.


## IP Address Configuration
It will create IP addresses on the new interface and configure the OSPF routing process to include the new interface. IP addresses can be both IPv4 and IPv6 prefixes. They have to be given as the address for the actual interface plus a prefix length e.g. `192.168.27.1/24` or `2001:db8:100::1/64`.

If multiple IPv4 addresses are provided the script uses the first in the list as the 'primary' IP address and the others as 'secondaries. If multiple IPv6 addresses are provided then all of them will be configured as prefixes for the interface.

Note that due to a defects CSCuy49650 and CSCuy49658 secondary IP addresses are somewhat dysfunctional at the moment.


## OSPF Configuration
OSPF process configuration might or might not be useful, for a service VLAN provisioning the redistribution of connected networks is probably sufficient by itself (e.g. no additional configuration needed in that case.

IPv6 / OSPFv3 configuration assumes that IPv6 unicast-routing is on (otherwise you will get an error). The script will create OSPFv3 interface configuration if the interface is configured with IPv6 prefixes. The script will create OSPF process configuration for the `interface-ip-address/32` with a `0.0.0.0` (host) mask for the process ID and area ID given.


## Options and Parameters
All parameters can be configured via command line. However, for ease of use / convenience, the following are hard-coded into the script (see the very top) but can be overriden:

- **Host.** (*HOST*) This is the IP or FQDN of the box we want to talk to
- **Port.** (*PORT*) The RESTCONF port (HTTP defaults to 8008, HTTPS to 8888)
- **Username.** (*USER*) The priviledge level 15 user on the box
- **Password.** (*PASS*) The associated password
- **Base Interface Name.** (*BASE*) The base interface name where the VLAN subinterfaces should be created for
- **OSPF Process ID.** (*OSPF*) The ID of the OSPF process for which the networks statements should be created for
- **OSPF Area ID.** (*AREA*) The ID of the OSPF area the networks should be put into

Other options are:

- `--delete` remove the given VLAN interface
- `--ssl` use SSL / TLS to connect to the RESTCONF agent
- `--insecure` when using SSL, relax security checks (certificates etc.)
- `--verbose` show what is being done (methhod, URL, body, return code and responses)

## Help Provided


~~~~
$ ./xe-vlan.py -h
usage: xe-vlan.py [-h] [--verbose] [--delete] [--defaults] [--ssl]
                  [--insecure] [--user USER] [--password PASSWORD]
                  [--host HOST] [--port PORT] [--interface INTERFACE]
                  [--ospf OSPF] [--area AREA]
                  [vlan] [prefix [prefix ...]]

xe-vlan.py uses RESTCONF to create or delete a 802.1Q subinterface
on an IOS XE device. There are a few default values at the top
of the script which can be overriden via command line arguments.

At least a VLAN ID must be provided. One or more Interface IP
address(es) are optional (IPv4 or IPv6).

positional arguments:
  vlan                  VLAN number (1-4094)
  prefix                IPv4 or IPv6 prefixes

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v         be verbose, print requests and responses
  --delete, -d          delete interface, given prefix(es) ignored
  --defaults            show defaults
  --ssl, -s             use SSL
  --insecure, -k        relax SSL verification, only with --ssl
  --user USER, -u USER  user name on remote host
  --password PASSWORD, -p PASSWORD
                        password on remote host
  --host HOST, -H HOST  remote host
  --port PORT, -P PORT  port on remote host
  --interface INTERFACE, -i INTERFACE
                        interface name to use
  --ospf OSPF, -o OSPF  OSPF process ID
  --area AREA, -a AREA  OSPF area

Examples:
xe-vlan.py 100 172.16.0.1/24
xe-vlan.py 100 172.16.0.1/24 172.16.1.1/24
xe-vlan.py 200 2001:db8:100::1/64
xe-vlan.py 200 2001:db8:100::1/64 2001:db8:200::1/64
xe-vlan.py 200 172.16.0.1/24 2001:db8:100::1/64
xe-vlan.py 300 --delete --verbose
xe-vlan.py --defaults
$
~~~~