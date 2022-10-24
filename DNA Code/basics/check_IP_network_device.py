# !/usr/bin/env python3

import requests
import urllib3
from requests.auth import HTTPBasicAuth  # for Basic Auth
from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings
import dnac_apis1
from env_lab import DNAC_URL, DNAC_PASS, DNAC_USER
urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)

dnac_auth = dnac_apis1.get_dnac_jwt_token(DNAC_AUTH)

def pprint(json_data):
    """
    Pretty print JSON formatted data
    :param json_data:
    :return:
    """

    print(json.dumps(json_data, indent=4, separators=(' , ', ' : ')))


def get_input_ip():
    """
    This function will ask the user to input the IP address. The format x.x.x.x of the IP address is not validated
    The function will return the IP address
    :return: the IP address
    """

    ip_address = input('Input the IP address to be validated?  ')
    return ip_address


def check_device(interface_ip):
    """
    This function will find out if there is a network device interface configured with an IP address
    The function will call two APIs:
    /interface/ip-address/{ip-address} - required for most of the network devices
    /network-device/ip-address/{ip-address} - required for access points
    :param interface_ip: ip address to be validated if configured on any network devices
    :return: 
    """

    url = DNAC_URL + '/api/v1/interface/ip-address/' + interface_ip
    header = {'accept': 'application/json', 'X-Auth-Token': dnac_auth}
    interface_response = requests.get(url, headers=header, verify=False)
    if not interface_response:
        url = DNAC_URL + '/api/v1/network-device/ip-address/' + interface_ip  # verification required for wireless AP's IP address
        header = {'accept': 'application/json', 'X-Auth-Token': dnac_auth}
        device_response = requests.get(url, headers=header, verify=False)
        if not device_response:
            print('The IP address ', interface_ip, ' is not configured on any network devices')
        else:
            print('The IP address ', interface_ip, ' is configured on a wireless access point')
    else:
        print('The IP address ', interface_ip, ' is configured on a network device')


def main():
    """
    This simple script will find out if there is a network device interface configured with an IP address
    It will ask the user to input an IP address to be validated
    It will print information if the input IP address is configured on a network device interface or not
    """

    # create an auth dnac_auth for DNAC 

    dnac_auth = dnac_apis1.get_dnac_jwt_token(DNAC_AUTH)
    
    device_ip_address = get_input_ip()
    print('IP Address to be validated:', device_ip_address)

    # check if the input IP address is used by a network device

    check_device(device_ip_address)



if __name__ == '__main__':
    main()

