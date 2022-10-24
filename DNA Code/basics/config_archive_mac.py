import json
import requests
import time
import pprint
from dnacentersdk import DNACenterAPI
from dnacentersdk.exceptions import ApiError
from env_lab import dnacurl , username , passwd 
from env_lab import DNAC, DNAC_PORT, DNAC_USER, DNAC_PASSWORD
#Suppressing warning due to lack of certificate verificaton in https connection
requests.packages.urllib3.disable_warnings() 

##open rat file for dnac connection establishment
#with open('rat.json') as json_file:
#    data = json.load(json_file)


#Create DNA api object "dnac"
dnac = DNACenterAPI(base_url=DNAC, username=DNAC_USER, password=DNAC_PASSWORD, verify=True)
#base_url=DNAC, username=DNAC_USER, password=DNAC_PASSWORD, verify_cert=True

#Get All Devices
devs=dnac.devices.get_device_list()
devlist=[x['id'] for x in devs['response']]

#Start task to create configuration files
mypayload={"deviceId":devlist,"password":"Cisco123#"}
headers={"content-type" : "application/json"}
url="/dna/intent/api/v1/network-device-archive/cleartext"
response = dnac.custom_caller.call_api(method="POST", resource_path=url, headers=headers, json=mypayload)

#Wait for task to complete and then retrieve task details
time.sleep(5)
mytaskid=response["response"]["taskId"]
response = dnac.task.get_task_by_id(mytaskid)

#Parse response to get URL and call the URL to download zip file of configs
url =response["response"]["additionalStatusURL"]
response = dnac.custom_caller.call_api(method="GET", resource_path=url, original_response=True)

#Response is in bytes, write bytes to file.
with open("dnacconfall.zip","wb") as r:
    r.write(response.content)