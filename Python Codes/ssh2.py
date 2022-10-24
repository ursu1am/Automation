from netmiko import ConnectHandler                                                                                                  
cisco = { 
     'device_type': 'cisco_ios', 
     'ip': '192.168.122.2', 
     'username': 'cisco', 
     'password': 'cisco', 
}  

net_connect = ConnectHandler(**cisco) 
output = net_connect.send_command("show ip int brief")
print (output)

config_commands = ['interface loopback 1' , 'ip address 10.1.1.1 255.255.255.255']
output = net_connect.send_config_set(config_commands)
print (output)

for vlan in range (40,50):
 	print ("Create vlan from 40 till 50 " + str(vlan))
 	config_commands = ['vlan ' + str(vlan), 'name MY_VLAN_' + str(vlan)]
 	output = net_connect.send_config_set(config_commands)
 	print (output)






