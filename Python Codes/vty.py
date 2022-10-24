
import json
from napalm import get_network_driver

list = ['172.28.193.14',
'172.28.193.15',
'172.28.193.49'
]

for ip_address in list:
    print ("Connecting to " + str(ip_address))
    driver = get_network_driver('ios')
    iosv_router = driver(ip_address, '40102501', '@Sonu@143')
    iosv_router.open()

    print ("Putting Line VTY SSH For  " + str(ip_address))
    iosv_router.load_merge_candidate(filename='line.cfg')
    iosv_router.commit_config()
    iosv_router.close()

    iosv_router.close()


# line.cfg
#line vty 0 15
#transport input ssh
#transport output ssh
#!
