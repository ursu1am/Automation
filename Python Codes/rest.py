## rest 
import requests 
import json from requests.auth 
import HTTPBasicAuth 
 
 
    auth = HTTPBasicAuth('admin', 'admin')     
    headers = { 'Accept': 'application/json'}     
    url = 'https://198.18.1.10:443/dataservice/device/ospf/neighbor?deviceId=10.1.0.1’     
    response = requests.get(url, verify=False, headers=headers, auth=auth)     print (response.status_code)     
    print (response.text)
