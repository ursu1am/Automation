#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
General Information 

"""
import os
import pandas as pd 
import datetime
import time
import json
import csv
import click
import tabulate
import urllib3
from requests.auth import HTTPBasicAuth  # for Basic Auth
from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings
import dnac_apis
from env_lab import DNAC_PASS, DNAC_USER , DNAC_URL
#from config import DEPLOY_PROJECT, DEPLOY_TEMPLATE, DEVICE_TYPES
urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

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

    date_time = str(datetime.datetime.now().replace(microsecond=0))

    print('\n\nApplication "get_discovery.py" Run Started: ' + date_time)

    # get a Cisco DNA Center auth token
    dnac_auth = dnac_apis.get_dnac_jwt_token(DNAC_AUTH)

    # find all devices managed by Cisco DNA C, that are "switches and hubs"
    #startIndex = 1
    #recordsToReturn = 328
    all_device_list = dnac_apis.get_discovery1(dnac_auth)
    pprint(all_device_list)
    #write_header()
    output_file = open('IP_Range2.csv', 'w', newline='') 
    output_writer = csv.writer(output_file)

    # loop through all devices list to collect the information needed in the report
    #headers = ["Name", "IP-Pool"]
 
    for device in all_device_list:
    
        Discovery_Name = device['name']
        IP_Pool = device['ipAddressList']
        
        
        device_info = [Discovery_Name, IP_Pool]
        output_writer.writerow(device_info)         
    output_file.close()
    print('\n\nFile "device_report.csv" saved')
        
    print('\n\nEnd of application "test-host.py" run') 

if __name__ == "__main__":
    main()
