### Netmiko SDWAN VPN 10 Configuration 
from netmiko import ConnectHandler

with open('DC1_vpn_10_config') as f:
    commands_to_send = f.read().splitlines()

ios_devices = {
    'device_type': 'cisco_ios',
    'ip': '198.18.3.100',
    'username': 'admin',
    'password': 'admin',
}

all_devices = [ios_devices]

for devices in all_devices:
    net_connect = ConnectHandler(**devices)
    output = net_connect.send_config_set(commands_to_send)
    print (output) 