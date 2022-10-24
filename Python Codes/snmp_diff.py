import json
from napalm import get_network_driver

devicelist = ['192.168.122.2',
           '192.168.122.3'
           ]

for ip_address in devicelist:
    print ("Connecting to " + str(ip_address))
    driver = get_network_driver('ios')
    iosv = driver(ip_address, 'cisco', 'cisco')
    iosv.open()
    iosv.load_merge_candidate(filename='snmp1.cfg')
    diffs = iosv.compare_config()
    if len(diffs) > 0:
        print(diffs)
        iosv.commit_config()
    else:
        print('No SNMP changes required.')
        iosv.discard_config()

    iosv.load_merge_candidate(filename='aaa.cfg')

    diffs = iosv.compare_config()
    if len(diffs) > 0:
        print(diffs)
        iosv.commit_config()
    else:
    	print('No AAA changes required.')
    	iosv.discard_config()

    iosv.close()
