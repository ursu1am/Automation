from netmiko import ConnectHandler                                                                                                  
#IN-BLR-GCC-SWS-12-14#
cisco_sw1 = { 
     'device_type': 'cisco_ios', 
     'ip': '172.28.193.49', 
     'username': '40102501', 
     'password': '@Sonu@143', 
}  

with open('device_config') as f:
	lines = f.read().splitlines()
print (lines)

all_switches = [cisco_sw1]

for switches in all_switches:
    net_connect = ConnectHandler(**switches) 
    output = net_connect.send_config_set(lines)
 	print (output)
