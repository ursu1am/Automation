import datetime
import time
import json
import os
import sys 
import re
import ssl
#import csv
#import click
#import tabulate
import urllib3
from requests.auth import HTTPBasicAuth  # for Basic Auth
from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings
import dnac_apis1
#import pandas
#import pandas as pd
#from getpass import getpass
#from config import DNAC_PASSWORD, DNAC_USER
#from config import DNAC_URL, DNAC_USER, DNAC_PASSWORD
from env_lab import DNAC, DNAC_PORT, DNAC_USER, DNAC_PASS, DEVICE_FAMILY

urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

#print ('Please Enter your password to proceed ')
#DNAC_PASSWORD = getpass()
DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)
dnac_auth = dnac_apis1.get_dnac_jwt_token(DNAC_AUTH)


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
    file.to_csv("device_report2.csv", header=headerList, index=False) 
      
    # display modified csv file 
    file2 = pd.read_csv("device_report2.csv") 
    print('\nModified file:') 
    print(file2) 
    
def main():
    """
    This script will take running configuration backup in backupfolder .
    The device family is defined by a list "DEVICE_FAMILY"
    """

    # the local date and time when the code will start execution

    date_time = str(datetime.datetime.now().replace(microsecond=0))

    print('\n\nApplication "backup_all_devices.py" Run Started: ' + date_time)

    # get a Cisco DNA Center auth token
    dnac_auth = dnac_apis1.get_dnac_jwt_token(DNAC_AUTH)

    device_list = dnac_apis1.get_all_device_list(500, dnac_auth)
     
    # create the switches list
    switch_list_reachable = []
    switch_list_unreachable = []

    # create the switches list
    for device in device_list:
        #device_type = device['type']
        device_type = device['family']
        #if device_type in DEVICE_TYPES:
        if device_type in DEVICE_FAMILY:
            hostname = device['hostname']
            ip = device['managementIpAddress']
            device_id = device['id']
            
            if device['reachabilityStatus'] == 'Reachable':
                
                switch_list_reachable.append(hostname)

            else:
                switch_list_unreachable.append(hostname)

    print('\nThe unreachable devices are:', switch_list_unreachable, '\n')
    print('\nThe rechable devices are:', switch_list_reachable)
    print('\nThe number of reachable devices are: ', len(switch_list_reachable))
    print('\nThe number of un-reachable devices are: ', len(switch_list_unreachable))

    first_record = int(input('\nWhat is the device index you want to start with ? (integer between 0 and total number '
                          'of switches)  '))
    device_index = first_record
    for switch in switch_list_reachable[first_record:]:
        dnac_auth = dnac_apis1.get_dnac_jwt_token(DNAC_AUTH)
        device_hostname = switch
        print(switch)
        # device_config = dnac_apis1.get_device_config_new(device_hostname, dnac_auth)
        device_config = dnac_apis1.get_device_config_backup(device_hostname, dnac_auth)
        #print(device_config)
        save_path = os.path.join(os.getcwd(), "config") 
        
        name_of_file = device_hostname
        completeName = os.path.join(save_path, name_of_file+".txt")         
        file1 = open(completeName, "w")
        toFile = ''
        toFile = device_config
        file1.write(toFile)
        file1.close()     
        print('Execuiting show running-config for switch: ', switch, ' with index: ', ', device index: ', device_index)
        device_index += 1        
    print('\n\nEnd of application "backup-host.py" run') 

if __name__ == "__main__":
    main()
