#acl_wlc
config
ip access-list extended PYTHON-ACL
permit ip host 1.1.1.1 host 2.2.2.2
permit ip host 2.2.2.2 host 1.1.1.1
---
no ip access-list extended PYTHON-ACL
---
show ap summary
---

from netmiko import ConnectHandler
#IN-BLR-GCC-SWS-12-14#
cisco_sw1 = {
     'device_type': 'cisco_ios',
     'ip': '172.28.193.61',
     'username': '40102501',
     'password': '@Sonu@143',
}

with open('acl') as f:
     lines = f.read().splitlines()
     print ('-----Code Developed by Ratnesh for AB-inBev Automation Project Config-Anything to Devices-----------\n')
     print ('----- ACL Lines are below ------\n')
     print (lines)

all_switches = [cisco_sw1]

for switches in all_switches:
    net_connect = ConnectHandler(**switches)
    output = net_connect.send_config_set(lines)
    print (output)


print (' now its time to remove the config file ----- Raise change before configuration -------\n')

with open('acl1') as f:
     lines = f.read().splitlines()
     print ('-----  Removing the config files ------\n')
     print (lines)

all_switches = [cisco_sw1]

for switches in all_switches:
    net_connect = ConnectHandler(**switches)
    output = net_connect.send_config_set(lines)
    print (output)
