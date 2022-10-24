!
ip domain-name cisco.com
ip name-server 10.40.1.83
ip name-server 10.40.1.82
!
interface GigabitEthernet0/1
 description UPLINK Core-Switch
 switchport access vlan 80
 switchport mode access
!
interface GigabitEthernet0/0
 description towards Switch1-Access
 switchport access vlan 81
 switchport mode access
 speed nonegotiate
!
interface GigabitEthernet0/2
 description 1-1 A1/01
 switchport access vlan 82
 switchport mode access
 switchport voice vlan 5
 storm-control broadcast level 5.00
 storm-control multicast level 30.00
 storm-control action shutdown
 storm-control action trap
 spanning-tree portfast
 spanning-tree bpduguard enable
!
!
ip default-gateway 192.168.122.1
ip forward-protocol nd
ip http server
ip http authentication local
ip http secure-server
!
!
logging host 10.0.16.81
logging host 10.96.0.10
logging host 10.99.0.10
logging host 10.40.0.74
!
access-list 60 remark SNMP Ro access
access-list 60 permit 10.99.32.86
access-list 60 permit 10.0.16.91
access-list 60 permit 10.0.16.81
access-list 60 permit 10.96.0.15
access-list 60 permit 10.40.0.64 0.0.0.31
access-list 60 permit 10.99.0.0 0.0.0.31
access-list 60 permit 10.96.0.0 0.0.0.31
access-list 70 remark snmp-RW-access
access-list 70 permit 10.96.0.10
access-list 70 permit 10.40.0.67
access-list 70 permit 10.99.0.10
access-list 70 permit 10.40.0.74
!
!
ntp server 10.96.32.90
!

