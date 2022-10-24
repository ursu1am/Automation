# !/usr/bin/env python3

import requests
import urllib3
from requests.auth import HTTPBasicAuth  # for Basic Auth
from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings
import dnac_apis
import csv
import json
from env_lab import DNAC_URL, DNAC_PASS, DNAC_USER
urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)

dnac_auth = dnac_apis.get_dnac_jwt_token(DNAC_AUTH)

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


def check_client_ip_address(client_ip):
    """
    The function will find out if APIC-EM has a client device configured with the specified IP address.
    API call to /host
    It will print if a client device exists or not.
    :param client_ip: client IP address
    :return: None
    """

    url = DNAC_URL + '/api/v1/host'
    header = {'accept': 'application/json', 'X-Auth-Token': dnac_auth}
    payload = {'hostIp': client_ip}
    host_response = requests.get(url, params=payload, headers=header, verify=False)
    host_json = host_response.json()

    pprint(host_json)  # needed for troubleshooting

    # verification if client found or not

    if not host_json['response']:
        print('The IP address', client_ip, 'is not used by any client devices')
    else:
        print('The IP address', client_ip, 'is used by a client device')
        host_info = host_json['response'][0]
        host_type = host_info['hostType']
        host_vlan = host_info['vlanId']
        host_mac_address = host_info['hostMac']

        # verification required for wireless clients, JSON output is different for wireless vs. wired clients

        if host_type == 'wireless':

            # info for wireless clients

            DNAC_URL_device_id = host_info['connectedNetworkDeviceId']
            hostname = get_hostname_id(DNAC_URL_device_id)[0]
            device_type = get_hostname_id(DNAC_URL_device_id)[1]
            print('The IP address', client_ip, ', is connected to the network device:', hostname, ', model:',
                  device_type, ', interface VLAN:', host_vlan)
        else:

            # info for ethernet connected clients

            interface_name = host_info['connectedInterfaceName']
            DNAC_URL_device_id = host_info['connectedNetworkDeviceId']
            hostname = get_hostname_id(DNAC_URL_device_id)[0]
            device_type = get_hostname_id(DNAC_URL_device_id)[1]
            print('The IP address', client_ip, ', is connected to the network device:', hostname, ', model:',
                  device_type, ', interface:', interface_name, ', VLAN:', host_vlan,', MAC_ADDRESS:', host_mac_address)


def get_hostname_id(device_id):
    """
    The function will find out the hostname of the network device with the specified device ID
    The function will require two values, the Auth ticket and device id
    The function with return the hostname and the device type of the network device
    API call to sandboxapic.cisco.com/api/v1/network-device/{id}
    :param device_id: APIC-EM device id
    :return:
    """

    hostname = None
    url = DNAC_URL + '/api/v1/network-device/' + device_id
    header = {'accept': 'application/json', 'X-Auth-Token': dnac_auth}
    hostname_response = requests.get(url, headers=header, verify=False)
    hostname_json = hostname_response.json()
    hostname = hostname_json['response']['hostname']
    device_type = hostname_json['response']['type']
    return hostname, device_type


def main():
    """
    This simple script will find out if there is a client connected to the Enterprise network
    It will ask the user to input an IP address for a client device.
    It will print information if the input IP address is being used by a client or not
    It will find out information about the client, and the connectivity info, switch and wireless AP,
    interface connectivity, VLAN information
    There is a loop that will allow running the validation multiple times, until user input is 'q'
    """

    dnac_auth = dnac_apis.get_dnac_jwt_token(DNAC_AUTH)

    client_ip_address = None
    while client_ip_address != "q":    # this loop will allow running the validation multiple times, until user input is 'q'
        client_ip_address = get_input_ip()
        print('IP Address to be validated:', client_ip_address)
        if client_ip_address != 'q':
            check_client_ip_address(client_ip_address)  # check if the input IP address is used by network clients


if __name__ == '__main__':
    main()

