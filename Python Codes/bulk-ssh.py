from netmiko import ConnectHandler                                                                                                  
cisco_sw1 = { 
     'device_type': 'cisco_ios', 
     'ip': '192.168.122.2', 
     'username': 'cisco', 
     'password': 'cisco', 
}  
cisco_sw2 = { 
     'device_type': 'cisco_ios', 
     'ip': '192.168.122.3', 
     'username': 'cisco', 
     'password': 'cisco', 
}

with open('device_config') as f:
	lines = f.read().splitlines()
print (lines)

all_switches = [cisco_sw1 , cisco_sw2]

for switches in all_switches:
    net_connect = ConnectHandler(**switches) 
    output = net_connect.send_config_set(lines)
 	print (output)
