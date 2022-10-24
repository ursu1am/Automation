# NAPALM LAB #1

import json
from napalm import get_network_driver
driver = get_network_driver('ios')
iosX = driver('192.168.122.2', 'cisco' , 'cisco')
iosX.open()

ios_output = iosX.get_facts()
print (json.dumps(ios_output, indent=4))

ios_output = iosX.get_interfaces()
print (json.dumps(ios_output, indent=4))

ios_output = iosX.get_mac_address_table()
print (json.dumps(ios_output, indent=4))

iosX.close()



