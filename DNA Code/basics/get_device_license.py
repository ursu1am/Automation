# !/usr/bin/env python3

import requests
import urllib3
from requests.auth import HTTPBasicAuth  # for Basic Auth
from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings
import dnac_apis1
import csv
import json
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


def get_license_device(deviceid):
    """
    The function will find out the active licenses of the network device with the specified device ID
    API call to sandboxapic.cisco.com/api/v1//license-info/network-device/{id}
    :param deviceid: DNAC  network device id
    :return: license information for the device, as a list with all licenses
    """

    license_info = []
    url = DNAC_URL + '/api/v1/license-info/network-device/' + deviceid
    header = {'accept': 'application/json', 'X-Auth-Token': dnac_auth}
    payload = {'deviceid': deviceid}
    device_response = requests.get(url, params=payload, headers=header, verify=False)
    if device_response.status_code == 200:
        device_json = device_response.json()
        device_info = device_json['response']
        # pprint(device_info)    # use this for printing info about each device
        for licenses in device_info:
            try:  # required to avoid errors due to some devices, for example Access Points,
                # that do not have an "inuse" license.
                if licenses.get('status') == 'INUSE':
                    new_license = licenses.get('name')
                    if new_license not in license_info:
                        license_info.append(new_license)
            except:
                pass
    return license_info


def get_hostname_devicetype_serialnumber(deviceid):
    """
    The function will find out the hostname of the network device with the specified device ID
    API call to sandboxapic.cisco.com/api/v1/network-device/{id}
    :param deviceid: DNAC  network device id
    :return: device hostname, device type, serial number
    """

    url = DNAC_URL + '/api/v1/network-device/' + deviceid
    header = {'accept': 'application/json', 'X-Auth-Token': dnac_auth}
    hostname_response = requests.get(url, headers=header, verify=False)
    hostname_json = hostname_response.json()
    hostname = hostname_json['response']['hostname']
    device_type = hostname_json['response']['type']
    serial_number = hostname_json['response']['serialNumber']
    mgmt_addr = hostname_json['response']['managementIpAddress']
    return hostname, device_type, serial_number, mgmt_addr


def get_input_file():
    """
    The function will ask the user to input the file name to save data to
    The function will append .csv and return the file name with extension
    :return: filename
    """

    filename = input('Input the file name to save data to:  ') + '.csv'
    return filename


def get_device_ids():
    """
    The function will build the ID's list for all network devices
    API call to sandboxapic.cisco.com/api/v1/network-device
    :return: DNAC  devices id list
    """
    device_id_list = []
    url = DNAC_URL + '/api/v1/network-device'
    header = {'accept': 'application/json', 'X-Auth-Token': dnac_auth}
    device_response = requests.get(url, headers=header, verify=False)
    device_json = device_response.json()
    device_info = device_json['response']
    for items in device_info:
        device_id = items.get('id')
        device_id_list.append(device_id)
    return device_id_list


def collect_device_info(device_id_list):
    """
    The function will create a list of lists.
    For each device we will have a list that includes - hostname, Serial Number, and active licenses
    The function will require two values, the list with all device id's and the Auth ticket
    :param device_id_list: DNAC  devices id list
    :return: all devices license file
    """

    all_devices_license_file = [['Hostname', 'Model ','Serial Number', 'Mgmt Address','License 1', 'License 2']]
    for device_id in device_id_list:  # loop to collect data from each device
        license_file = []
        print('device id ', device_id)  # print device id, printing messages will show progress
        host_name = get_hostname_devicetype_serialnumber(device_id)[0]
        serial_number = get_hostname_devicetype_serialnumber(device_id)[1]
        device_type = get_hostname_devicetype_serialnumber(device_id)[2]
        mgmt_addr = get_hostname_devicetype_serialnumber(device_id)[3]
        license_file.append(host_name)
        license_file.append(serial_number)
        license_file.append(device_type)
        license_file.append(mgmt_addr)
        
        device_license = get_license_device(device_id)  # call the function to provide active licenses
        for licenses in device_license:  # loop to append the provided active licenses to the device list
            license_file.append(licenses)
        all_devices_license_file.append(license_file)  # append the created list for this device to the list of lists
    return all_devices_license_file


def main():
    """
    This application will create a list of all the DNAC  discovered network devices, their serial numbers and
    active software licenses.
    We will access a DevNet Sandbox to run this script.
    Changes to the DNAC  url, username and password are required if desired to access a different DNAC  controller.
    :return:
    """
    dnac_auth = dnac_apis1.get_dnac_jwt_token(DNAC_AUTH)

    # build a list with all device id's
    device_id_list = get_device_ids()
    devices_info = collect_device_info(device_id_list)
    pprint(devices_info)  # needed for troubleshooting

    # ask user for filename input and save file
    filename = get_input_file()
    output_file = open(filename, 'w', newline='')
    output_writer = csv.writer(output_file)
    for lists in devices_info:
        output_writer.writerow(lists)
    output_file.close()

    # print to console
    for devices in devices_info:
        print('\t'.join([str(info) for info in devices]))


if __name__ == '__main__':
    main()
