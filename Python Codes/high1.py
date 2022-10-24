
EEM Script some error: For HighCPU 
conf t
process cpu threshold type total rising 20 interval 5 switch 1

event manager scheduler script thread class default number 1
event manager applet HighCPU
event syslog pattern " %SYS-1-CPURISINGTHRESHOLD"
action 0.1 syslog msg "high CPU detected"
action 0.2 cli command "enable"
action 1.0 cli command "show process cpu sorted | append flash:highcpu.txt"
action 1.1 cli command "show processes cpu monitor | append flash:highcpu.txt"
action 1.2 cli command "show processes cpu history | append flash:highcpu.txt"
action 1.3 cli command "show processes cpu sorted | ex 0.00 | append flash:highcpu.txt"
action 1.4 cli command "show processes cpu extended history | append flash:highcpu.txt"
action 1.5 cli command "show interfaces counters | append flash:highcpu.txt"
action 2.1 cli command "show logging | append flash:highcpu.txt"
!