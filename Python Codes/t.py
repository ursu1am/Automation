Policy: Low-IOMEM-Buffer-Capture
!
! I/O Memory Troubleshooting EEM Applet
!
! Stores relevant show commands in flash:low_mem.txt.
! Removes itself from config after completion.
! Requires SNMP be enabled and EEM v2.1

event manager scheduler script thread class default number 1
event manager applet LOW_IO_MEM
 event snmp oid 1.3.6.1.4.1.9.9.48.1.1.1.6.2 get-type exact entry-op lt entry-val 1000000 
 entry-type value exit-op gt exit-val 100000000 exit-type value poll-interval 10

 action 0.0 syslog msg "LOW I/O MEMORY DETECTED. Please wait - logging information to flash:low_mem.txt"

 action 0.1 cli command "enable"
 action 0.2 cli command "term exec prompt timestamp"

 action 1.2 cli command "show memory statistics | append flash:low_mem.txt"
 action 1.3 cli command "show process cpu sorted | append flash:low_mem.txt"
 action 1.5 cli command "show interfaces | append flash:low_mem.txt"
 action 1.6 cli command "show interfaces stat | append flash:low_mem.txt"
 action 1.7 cli command "show ip traffic | append flash:low_mem.txt"

 action 2.2 cli command "show buffers | append flash:low_mem.txt"
 action 2.3 cli command "show buffers failures | append flash:low_mem.txt"
 action 2.4 cli command "show buffers assigned dump | append flash:low_mem.txt"

 action 3.2 cli command "show log | append flash:low_mem.txt"
 action 3.3 cli command "show tech | append flash:low_mem.txt"
 action 3.4 cli command "show start | append flash:low_mem.txt"

 action 4.2 cli command "show interfaces | append flash:low_mem.txt"
 action 4.3 cli command "show interfaces stat | append flash:low_mem.txt"
 action 4.4 cli command "show ip traffic | append flash:low_mem.txt"

 action 5.1 syslog msg "Finished logging information to flash:low_mem.txt..."
 action 5.1 syslog msg "Self-removing applet from configuration..."

 action 9.1 cli command "configure terminal"
 action 9.2 cli command "no event manager applet LOW_IO_MEM"
 action 9.3 cli command "end"
 !
 
 