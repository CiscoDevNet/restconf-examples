# Example of the old way to get the interface status and parse results

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

#regular expression to call the CLI command 'show ip interface brief', capture and parse the returned data for interfaces with assign IP addresses.
set interfaces [regexp -all -line -inline "^(FastEthernet|GigabitEthernet)(\[0-9.\]+) +(\[0-9.\]+).*(up|down)" [exec "show ip int brief"]]

#variable to walk through the interfaces array of returned data.
set index 0
#variable to flag if an interface in 'down' status has been found.
set flagDown 0
#Loop through the interfaces array to the end.
while {$index < [llength $interfaces]} {
  #Assign the interface name and number to variable named interface
  set interface "[lindex $interfaces [expr $index + 1]] [lindex $interfaces [expr $index + 2]]"
  #Assign the interface IP and number to variable named ip
  set ip "[lindex $interfaces [expr $index + 3]]"
  #Assign the interface status and number to variable named status
  set status "[lindex $interfaces [expr $index + 4]]"
  #if an interface status is down set the flag
  if {$status == "down"} {
    set flagDown 1
 }
  #increment the counter to the next interface data
  set index [expr $index + 5]
  #write captured interface data to the screen.
  puts "interface:  $interface   ip:  $ip    status: $status"
}
#Report final status of all reviewed interfaces
if {$flagDown == 0} {
  puts "All interfaces are up"
} else {
  puts "At least one interface is down"
}