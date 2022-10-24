#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
General Information 

"""

import datetime
import time
import requests
import json
import csv
import click
import tabulate
import urllib3
from requests.auth import HTTPBasicAuth  # for Basic Auth
from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings
import dnac_apis
import pandas
#from getpass import getpass
#from config import DNAC_PASS, DNAC_USER
from env_lab import DNAC_URL, DNAC_PASS, DNAC_USER
#from config import DEPLOY_PROJECT, DEPLOY_TEMPLATE, DEVICE_TYPES
urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

#print ('Please Enter your password to proceed ')
#DNAC_PASSWORD = getpass()
DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)


def pprint(json_data):
    """
    Pretty print JSON formatted data
    :param json_data:
    :return:
    """
    print(json.dumps(json_data, indent=4, separators=(' , ', ' : ')))


def main():

    # the local date and time when the code will start execution
    #date_time = str(datetime.datetime.now().replace(microsecond=0))
    #print('\n\nApplication "get_sites.py" Run Started: ' + date_time)

    # get a Cisco DNA Center auth token
    dnac_auth = dnac_apis.get_dnac_jwt_token(DNAC_AUTH)
    result = dnac_apis.get_device_config_archive(0, dnac_auth)
    #pprint(result)
    for item in result: 
        hostname = item['deviceName']
        #Address = item['ipAddress']
        versions = item['versions']
      
        for item2 in versions: 
            start = item2['startupRunningStatus']           
            if item2['startupRunningStatus'] == 'OUT_OF_SYNC':
               #hostname1 = hostname 
               #print(hostname)
               print ('Hostname : ' +hostname+ '    startupRunningStatus : ' + "Non-Compliant")
            
             
if __name__ == "__main__":
    main()
    
    
    
    
    
    
