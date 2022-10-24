#!/usr/bin/env python2

import requests
import json
from env_lab import DNAC, DNAC_PORT, DNAC_USER
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()

import json
import os
import os.path
import pandas as pd 
import time
import re  # needed for regular expressions matching
import select
import socket  # needed for IPv4 validation
import sys
import urllib3
import getpass
import requests
import subprocess  # needed for the ping function
import ipaddress  # needed for IPv4 address validation
import datetime, time  # needed for epoch time conversion
from requests.auth import HTTPBasicAuth  # for Basic Auth
from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings
urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings
import warnings
warnings.filterwarnings("ignore")
requests.packages.urllib3.disable_warnings()
#os.system('cls')

def pprint(json_data):
    """
    Pretty print JSON formatted data
    :param json_data:
    :return:
    """

    print(json.dumps(json_data, indent=4, separators=(' , ', ' : ')))


def get_input_ip():
    """
    This function will ask the user to input the IP address. The format of the IP address is not validated
    The function will return the IP address
    :return: the IP address
    """

    ip_address = input('Input the IP address to be validated, (or q to exit) ?  ')
    return ip_address

def get_username():
    """
    This function will ask the user to input the IP address. The format of the IP address is not validated
    The function will return the IP address
    :return: the IP address
    """

    username = input('Input the username to proceed, (or q to exit) ?  ')
    return username


def get_input_mac():
    """
    This function will ask the user to input the IP address. The format of the IP address is not validated
    The function will return the IP address
    :return: the IP address
    """

    mac_address = input('Input the MAC address to be validated, (or q to exit) ?  ')
    return mac_address


def get_input_timeout(message, wait_time):
    """
    This function will ask the user to input the value requested in the {message}, in the time specified {time}
    :param message: message to provide the user information on what is required
    :param wait_time: time limit for the user input
    :return: user input as string
    """

    print(message + ' in ' + str(wait_time) + ' seconds')
    i, o, e = select.select([sys.stdin], [], [], wait_time)
    if i:
        input_value = sys.stdin.readline().strip()
        print('User input: ', input_value)
    else:
        input_value = None
        print('No user input in ', wait_time, ' seconds')
    return input_value


def validate_ipv4_address(ipv4_address):
    """
    This function will validate if the provided string is a valid IPv4 address
    :param ipv4_address: string with the IPv4 address
    :return: true/false
    """
    try:
        ipaddress.ip_address(ipv4_address)
        return True
    except:
        return False


def identify_ipv4_address(configuration):
    """
    This function will return a list of all IPv4 addresses found in the string {configuration}.
    It will return only the IPv4 addresses found in the {ip address a.b.c.d command}
    :param configuration: string with the configuration
    :return: list of IPv4 addresses
    """
    ipv4_list = []
    pattern = re.compile('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    split_lines = configuration.split('\n')  # split configuration file in individual commands'
    for line in split_lines:
        if 'ip address' in line:  # check if command includes the string 'ip address'
            split_config = line.split(' ')  # split the command in words
            try:
                split_config.remove('')  # remove the first ' ' if existing in the command
            except:
                pass
            line_begins = split_config[0:3]  # select the three items in the list
            for word in line_begins:
                check_ip = pattern.match(word)  # match each word with the pattern from regex
                if check_ip:
                    if validate_ipv4_address(word):  # validate if the octets are valid IP addresses
                        ipv4_list.append(word)
    return ipv4_list


def ping_return(hostname):
    """
    Use the ping utility to attempt to reach the host. We send 5 packets
    ('-c 5') and wait 250 milliseconds ('-W 250') for a response. The function
    returns the return code from the ping utility.
    It will also save the output to the file {ping_hostname}
    :param hostname: hostname or the IPv4 address of the device to ping
    """
    ret_code = subprocess.call(['ping', '-c', '5', '-W', '250', hostname], stdout=open('ping_' + hostname, 'w'))
    if ret_code == 0:
        return_code = 'Success'
    elif ret_code == 2:
        return_code = 'Failed'
    else:
        return_code = 'Unknown'
    return return_code


def get_epoch_current_time():
    """
    This function will return the epoch time for the {timestamp}, UTC time format, for current time
    :return: epoch time including msec
    """
    epoch = time.time()*1000
    return int(epoch)


def time_sleep(time_sec):
    """
    This function will wait for the specified time_sec, while printing a progress bar each second
    :param time_sec: time, in seconds
    :return: none
    """
    for i in range(time_sec):
        print('!', end="")
        time.sleep(1)
    return

def get_input_device_name():

    device_name = input('Input the Device Name to be validated, (or q to exit) ?  ')
    return device_name

def get_input_file():
    """
    The function will ask the user to input the file name to save data to
    The function will append .csv and return the file name with extension
    :return: filename
    """

    filename = input('Input the file name to save data to:  ') + '.csv'
    return filename

   
def get_dnac_jwt_token(dnac_auth, url):
    url = url + '/dna/system/api/v1/auth/token'
    header = {'content-type': 'application/json'}
    response = requests.post(url, auth=dnac_auth, headers=header, verify=False)
    dnac_jwt_token = response.json()['Token']
    return dnac_jwt_token

def get_dnac_jwt_getToken(dnac_auth, url):
    print
    dnac_ip     = input('IP Address or Hostname: ')
    username 	= input('Username: ')
    password 	= getpass.getpass('Password: ')
    #DNAC_AUTH = HTTPBasicAuth(username, password)
    
    post_url = "https://" + dnac_ip + "/api/system/v1/auth/token"
    headers = {'content-type': 'application/json'}
    response = requests.post(post_url,
    auth=HTTPBasicAuth(username=username,password=password),
    headers=headers,verify=False)
    if response.status_code != 200:
        print ("Verify Login \t\t\t\t \033[1;31;40m FAIL \033[0;0m")
        sys.exit()
    print
    print ("Verify Login \t\t\t\t \033[1;32;40m PASS \033[0;0m")
    print ("Retrieve Token ID \t\t\t \033[1;32;40m PASS \033[0;0m")
    r_json=response.json()
    token = r_json["Token"]
    return token 
    
def getToken():
    print
    dnac_ip     = input('IP Address or Hostname: ')
    username 	= input('Username: ')
    password 	= getpass.getpass('Password: ')

    
    post_url = "https://" + dnac_ip + "/api/system/v1/auth/token"
    headers = {'content-type': 'application/json'}
    response = requests.post(post_url,
    auth=HTTPBasicAuth(username=username,password=password),
    headers=headers,verify=False)
    if response.status_code != 200:
        print ("Verify Login \t\t\t\t \033[1;31;40m FAIL \033[0;0m")
        sys.exit()
    print
    print ("Verify Login \t\t\t\t \033[1;32;40m PASS \033[0;0m")
    print ("Retrieve Token ID \t\t\t \033[1;32;40m PASS \033[0;0m")
    r_json=response.json()
    token = r_json["Token"]
    return token  
    
def get_all_device_list(dnac_jwt_token, url):
    all_devices_info = []
    offset = 1
    limit = 500
    url_dev = url + '/dna/intent/api/v1/network-device/count'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    count_response = requests.get(url_dev, headers=header, verify=False)
    total_devices = count_response.json()['response']

    while offset < total_devices:
        url_dev = url + '/dna/intent/api/v1/network-device?offset=' + str(offset) + '&limit=' + str(limit)
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        all_devices_response = requests.get(url_dev, headers=header, verify=False)
        all_devices_json = all_devices_response.json()['response']
        all_devices_info += all_devices_json
        offset += 500

    return all_devices_info
    
def add_header_all_csv():
    # read contents of csv file
    filename = get_input_file()
    file = pd.read_csv(filename) 
    print("\nOriginal file:") 
    print(file) 
      
    # adding header 
    headerList = ["device_hostname", "device_type", "device_management_ip", "device_sn",
                               "device_mgmt_state", "device_support", "device_reachability", "device_location", "device_uptime"]
      
    # converting data frame to csv 
    file.to_csv(filename, header=headerList, index=False) 
      
    # display modified csv file 
    file2 = pd.read_csv(filename) 
    print('\nModified file:') 
    print(file2) 
   
def audit_log_csv():
    # read contents of csv file
    filename = get_input_file()
    file = pd.read_csv(filename) 
    print("\nOriginal file:") 
    print(file) 
      
    # adding header 
    headerList = ["Timestamp", "DeviceIP", "Requester", "Task_Completion", "Description"]
      
    # converting data frame to csv 
    file.to_csv(filename, header=headerList, index=False) 
      
    # display modified csv file 
    file2 = pd.read_csv(filename) 
    print('\nModified file:') 
    print(file2) 
    
def get_all_device_list(dnac_jwt_token, url):
    all_devices_info = []
    offset = 1
    limit = 500
    url_dev = url + '/dna/intent/api/v1/network-device/count'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    count_response = requests.get(url_dev, headers=header, verify=False)
    total_devices = count_response.json()['response']
    while offset < total_devices:
        url_dev = url + '/dna/intent/api/v1/network-device?offset=' + str(offset) + '&limit=' + str(limit)
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        all_devices_response = requests.get(url_dev, headers=header, verify=False)
        all_devices_json = all_devices_response.json()['response']
        all_devices_info += all_devices_json
        offset += 500
    return all_devices_info
 
def get_network_health(limit, dnac_jwt_token, url):
    all_devices_info = []
    offset = 1
    limit = 500
    url_dev = url + '/dna/intent/api/v1/network-device/count'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    count_response = requests.get(url_dev, headers=header, verify=False)
    total_devices = count_response.json()['response']
    while offset < total_devices:
        #all_devices_info = ''
        #url = DNAC_URL + '/dna/intent/api/v1/network-health'
        url_dev = url + '/dna/intent/api/v1/network-health?offset=' + str(offset) + '&limit=' + str(limit)
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        all_devices_response = requests.get(url_dev, headers=header, verify=False)
        all_devices_json = all_devices_response.json()
        #all_devices_info = all_devices_json['response']
        #all_devices_list += all_devices_info
        offset += limit
    return all_devices_json   
          
def get_all_issues_info(limit, dnac_jwt_token, url):
    """
    """
    all_devices_info = []
    offset = 1
    limit = 500
    url_dev = url + '/dna/intent/api/v1/network-device/count'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    count_response = requests.get(url_dev, headers=header, verify=False)
    total_devices = count_response.json()['response']
    while offset < total_devices:
        url_dev = url + '/dna/intent/api/v1/issues?offset=' + str(offset) + '&limit=' + str(limit)
        #url = DNAC_URL + '/dna/intent/api/v1/issues'
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        all_devices_response = requests.get(url_dev, headers=header, verify=False)
        all_devices_json = all_devices_response.json()
        #all_devices_info = all_devices_json['response']
        #all_devices_list += all_devices_info
        offset += limit
    return all_devices_json  
       
# -------------------------------------------------------------------
# Custom exception definitions
# -------------------------------------------------------------------
class TaskTimeoutError(Exception):
    pass

class TaskError(Exception):
    pass

# API ENDPOINTS
ENDPOINT_TICKET = "ticket"
ENDPOINT_TASK_SUMMARY ="task/%s"
RETRY_INTERVAL=2

# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------
def create_url(path, controller_ip=DNAC):
    """ Helper function to create a DNAC API endpoint URL
    """

    return "https://%s:%s/api/v1/%s" % (controller_ip, DNAC_PORT, path)


def get_auth_token(controller_ip=DNAC, username=DNAC_USER, password=DNAC_PASSWORD):
    """ Authenticates with controller and returns a token to be used in subsequent API invocations
    """

    login_url = "https://{0}:{1}/api/system/v1/auth/token".format(controller_ip, DNAC_PORT)
    result = requests.post(url=login_url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASSWORD), verify=False, timeout=20)
    result.raise_for_status()

    token = result.json()["Token"]
    return {
        "controller_ip": controller_ip,
        "token": token
    }

def get(dnac, url):
    geturl = create_url(url)
    headers = {'x-auth-token': dnac['token']}
    response = requests.get(geturl, headers=headers, verify=False)
    response.raise_for_status()
    return response

def post(dnac, url, payload):
    posturl = create_url(url)
    headers = {'x-auth-token': dnac['token'], "content-type" : "application/json"}
    response = requests.post(posturl, headers=headers, data=json.dumps(payload), verify=False)
    response.raise_for_status()
    return response

def put(dnac, url, payload):
    puturl = create_url(url)

    headers = {'x-auth-token': dnac['token'], "Content-Type" : "application/json"}
    response = requests.put(puturl, headers=headers, data=payload, verify=False)
    response.raise_for_status()
    return response

def delete(dnac, url):
    deleteurl = create_url(url)
    headers = {'x-auth-token': dnac['token']}
    response = requests.delete(deleteurl, headers=headers, verify=False)
    response.raise_for_status()
    return response

def login():
    return get_auth_token()
