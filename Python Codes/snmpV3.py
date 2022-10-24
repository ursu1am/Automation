#ABI SNMP

snmp-server group SNMPv3 v3 priv read SNMPv3-VIEW write SNMPv3-VIEW access SNMPv3
snmp-server view SNMPv3-VIEW iso included
snmp-server community iseISEB4by RO
snmp-server community ABI RO
snmp-server trap-source Vlan2
snmp-server enable traps cpu threshold
snmp-server enable traps vtp
snmp-server enable traps vlancreate
snmp-server enable traps vlandelete
snmp-server enable traps envmon fan shutdown supply temperature status
snmp-server enable traps config-copy
snmp-server enable traps bridge newroot topologychange
snmp-server enable traps mac-notification threshold
snmp-server host 172.18.42.163 version 2c ABI
snmp-server host 172.18.42.164 version 2c ABI
snmp-server host 172.18.42.184 version 2c ABI
snmp-server host 172.18.42.198 version 2c ABI
snmp-server host 172.18.42.207 version 2c ABI
snmp-server host 172.27.6.186 version 2c ABI
snmp-server host 172.27.6.187 version 2c ABI
snmp-server host 172.28.194.188 version 2c ABI
snmp-server host 172.28.194.189 version 2c ABI
snmp-server host 172.28.194.28 version 2c ABI
snmp-server host 172.28.194.70 ABI
snmp-server host 172.18.208.227 version 3 priv SNMPv3
snmp-server enable traps tty
snmp-server enable traps wireless
snmp-server enable traps trustsec
snmp-server enable traps stackwise
snmp-server enable traps vstack
snmp-server enable traps hsrp

--------------
import json
from napalm import get_network_driver
driver = get_network_driver('ios')
iosvl2 = driver('172.28.193.61', '40102501', '@Sonu@143')
iosvl2.open()

print ('Accessing 172.28.193.61')
iosvl2.load_merge_candidate(filename='snmp.cfg')

diffs = iosvl2.compare_config()
if len(diffs) > 0:
   print ('-----Code Developed by Ratnesh for AB-inBev Automation Project Config-Diff-----------\n')
   print ('===================== Diff Strats from here ============================\n')
   print(diffs)
   #iosvl2.commit_config()
else:
   print('No changes required.')
   iosvl2.discard_config()

iosvl2.close()


