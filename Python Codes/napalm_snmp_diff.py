## Config Diff via NAPALM 

import json
from napalm import get_network_driver
driver = get_network_driver('ios')
iosvl2 = driver('198.18.1.104', 'admin', 'admin')
iosvl2.open()

print ('Accessing 198.18.1.104')
iosvl2.load_merge_candidate(filename='snmp1.cfg')

diffs = iosvl2.compare_config()
if len(diffs) > 0:
    print(diffs)
    iosvl2.commit_config()
else:
    print('No changes required.')
    iosvl2.discard_config()

iosvl2.close()
