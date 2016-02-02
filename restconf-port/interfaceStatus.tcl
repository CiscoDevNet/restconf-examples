#Show interface status and parse results.

set interfaces [regexp -all -line -inline "^(FastEthernet|GigabitEthernet)(\[0-9.\]+) +(\[0-9.\]+).*(up|down)" [exec "show ip int brief"]]

set index 0
set flagDown 0
while {$index < [llength $interfaces]} {
  set interface "[lindex $interfaces [expr $index + 1]] [lindex $interfaces [expr $index + 2]]"
  set ip "[lindex $interfaces [expr $index + 3]]"
  set status "[lindex $interfaces [expr $index + 4]]"
  if {$status == "down"} {
    set flagDown 1
 }
  set index [expr $index + 5]
  puts "interface:  $interface   ip:  $ip    status: $status"
}

if {$flagDown == 0} {
  puts "All interfaces are up"
} else {
  puts "At least one interface is down"
}