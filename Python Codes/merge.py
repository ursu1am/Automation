#  NAPALM with multiple devices config 
import json
from napalm import get_network_driver

list = ['192.168.122.2',
'192.168.122.3'
]

for ip_address in list:
    print ("Connecting to " + str(ip_address))
    driver = get_network_driver('ios')
    iosv_router = driver(ip_address, 'cisco', 'cisco')
    iosv_router.open()

    print ("Putting Line VTY SSH For  " + str(ip_address))
    iosv_router.load_merge_candidate(filename='line.cfg')
    iosv_router.commit_config()
    iosv_router.close()

    iosv_router.close()

