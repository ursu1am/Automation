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

all_switches = [cisco_sw1 , cisco_sw2]

for switches in all_switches
    net_connect = ConnectHandler(**switches) 

for vlan in range (80,90):
 	print ("Create vlan from 80 till 90 " + str(vlan))
 	config_commands = ['vlan ' + str(vlan), 'name MY_VLAN_' + str(vlan)]
 	output = net_connect.send_config_set(config_commands)
 	print (output)






