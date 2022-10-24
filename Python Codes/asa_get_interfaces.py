#!/usr/bin/env python

import requests
import json
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()

if __name__ == "__main__":

    auth = HTTPBasicAuth('admin', 'admin')

    url = 'https://198.18.1.10:443/dataservice/device/ospf/neighbor?deviceId=10.1.0.1'
    response = requests.get(url, verify=False, auth=auth)

    print 'Status Code: ' + str(response.status_code)
    if response.text:
        parse = json.loads(response.text)
        print json.dumps(parse, indent=4)

