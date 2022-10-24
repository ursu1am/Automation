# Config Diff with NAPALM

import json
from napalm import get_network_driver
driver = get_network_driver('ios')
iosvl2 = driver('192.168.122.2', 'cisco', 'cisco')
iosvl2.open()

print ('Accessing 192.168.122.2')
iosvl2.load_merge_candidate(filename='snmp1.cfg')

diffs = iosvl2.compare_config()
if len(diffs) > 0:
    print(diffs)
    iosvl2.commit_config()
else:
    print('No changes required.')
    iosvl2.discard_config()

iosvl2.close()
