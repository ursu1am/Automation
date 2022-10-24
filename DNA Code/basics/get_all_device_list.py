#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
General Information 

"""

__author__ = "Ratnesh"
__email__ = ""
__version__ = "0.1.0"
__copyright__ = ""
__license__ = "Cisco Sample Code License, Version 1.1"
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
import dnac_apis1
from env_lab import DNAC_URL, DNAC_PASS, DNAC_USER
urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)


def pprint(json_data):
    """
    Pretty print JSON formatted data
    :param json_data:
    :return:
    """
    print(json.dumps(json_data, indent=4, separators=(' , ', ' : ')))

def add_header():
    # read contents of csv file 
    file = pd.read_csv("device_report.csv") 
    print("\nOriginal file:") 
    print(file) 
      
    # adding header 
    headerList = ["device_hostname", "device_type", "device_software_version", "device_management_ip", "device_sn", "device_mem", 
        "device_mgmt_state", "device_reach_fail", "device_support"] 
      
    # converting data frame to csv 
    file.to_csv("device_report.csv", header=headerList, index=False) 
      
    # display modified csv file 
    file2 = pd.read_csv("device_report.csv") 
    print('\nModified file:') 
    print(file2) 
def main():
    """
    This script will deploy a config file to a number of devices based on device family.
    The device family is defined by a list "DEVICE_TYPES"
    It will collect all the devices that match the device types, identify those that are reachable, and those that are
    not reachable.
    The script will deploy the configuration template to each reachable device.
    There are some optional commands included that will allow to test the template deployment to a small number of
    devices first.
    """

    # the local date and time when the code will start execution

    date_time = str(datetime.datetime.now().replace(microsecond=0))

    print('\n\nApplication "get_all_devices.py" Run Started: ' + date_time)

    # get a Cisco DNA Center auth token
    dnac_auth = dnac_apis1.get_dnac_jwt_token(DNAC_AUTH)

    # find all devices managed by Cisco DNA C, that are "switches and hubs"
    all_device_list = dnac_apis1.get_all_device_list(500, dnac_auth)
    pprint(all_device_list)
    switch_list_reachable = []
    switch_list_unreachable = []
    for device in all_device_list:
        device_type = device['family']
        #if device_type in DEVICE_TYPES:
        hostname = device['hostname']
        device_id = device['id']
        if device['reachabilityStatus'] == 'Reachable':
            switch_list_reachable.append(hostname)
            print(hostname)
        else:
            switch_list_unreachable.append(hostname)
    
    device_count = len(all_device_list)
  
    if device_count == [0]:
        print('\nCisco DNA Center does not manage any devices')
    else:
        print('\nCisco DNA Center manages this number of devices: ', device_count)

        #write_header()
        output_file = open('device_report.csv', 'w', newline='') 
        output_writer = csv.writer(output_file)

        # loop through all devices list to collect the information needed in the report
        headers = ["hostname", "managementIpAddress","managementState","Reachability","SupportLevel"]
        table = list()
        i=0
        for item in all_device_list:
            i+=1 
            tr = [i,item['hostname'], item['managementIpAddress'], item['managementState'], item['reachabilityFailureReason'], 
            item['deviceSupportLevel']]
            table.append(tr)
        try:
            click.echo(tabulate.tabulate(table, headers, tablefmt="fancy_grid"))
        except UnicodeEncodeError:
            click.echo(tabulate.tabulate(table, headers, tablefmt="grid"))
        #print ("*** Please note that some devices may not be able to show configuration for various reasons. ***\n")
        
        for device in all_device_list:
        
            device_hostname = device['hostname']
            device_type = device['type']
            device_software_version = device['softwareVersion']
            device_management_ip = device['managementIpAddress']
            device_sn = device['serialNumber']
            device_mem = device['memorySize']
            device_mgmt_state = device['managementState']
            device_reach_fail = device['reachabilityFailureReason']
            device_support = device['deviceSupportLevel']
            #device_family = device['family']
            device_info = [device_hostname, device_type, device_software_version, device_management_ip, device_sn,
            device_mem, device_mgmt_state, device_reach_fail, device_support]
            output_writer.writerow(device_info)         
        output_file.close()
        print('\n\nFile "device_report.csv" saved')
        
    add_header()
    print('\n\nEnd of application "device_report.py" run') 

if __name__ == "__main__":
    main()
