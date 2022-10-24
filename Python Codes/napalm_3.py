## Use of NAPALM to do the configuration 

import json
from napalm import get_network_driver
driver = get_network_driver('ios')
iosvl2 = driver('192.168.122.2', 'cisco', 'cisco')
iosvl2.open()

print ('Accessing 192.168.122.2')
iosvl2.load_merge_candidate(filename='line.cfg')
iosvl2.commit_config()
iosvl2.close()