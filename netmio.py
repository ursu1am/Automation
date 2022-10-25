from unittest import expectedFailure
from netmiko import ConnectHandler 

router = { 
    "host": "ios-xe-mgmt-latest.cisco.com", 
    "port": 8181, 
    "username": "root", 
    "password": "D_Vay!_10&", 
    "device_type": "cisco_ios" 
} 

try:
    c = ConnectHandler(**router)
    c.enable() 
    response = c.send_command("show run") 
    c.disconnect()
except Exception as ex:
    print(ex)
else:
    print(response)
    