#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
General Information 

"""

__author__ = "Ali & Ratnesh"
__email__ = ""
__version__ = "0.1.0"
__copyright__ = ""
__license__ = "Cisco Sample Code License, Version 1.1"

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

    dnac_auth = dnac_apis.get_dnac_jwt_token(DNAC_AUTH) 
    #site_id = 'ac65775a-e0ca-4304-beb4-19b51aacc7ed'
    with open('sites_to_be_deleted.txt') as f:
        ip_list = f.read().splitlines()
    i=0
    for site_id in ip_list: 
        print('site id for audit purpose '+ site_id)
        dnac_apis.delete_site(site_id, dnac_auth)

  
if __name__ == "__main__":
    main()
    
    
    
    
    
    
