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
 