import urllib3
import datetime
import json
import time
import logging
import dnacentersdk
import os

from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings
from requests.auth import HTTPBasicAuth  # for Basic Auth

from env_lab import DNAC_URL, DNAC_PASS, DNAC_USER
from dnacentersdk import DNACenterAPI
from env_lab import FOLDER_NAME

urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)


def main():
    """
    This application will:
     - create an inventory of all devices managed by Cisco DNA Center
     - make a folder to save the device configuration files to
     - collect the running configuration for each device
     - save each configuration to a file using the name {device_hostname}, in the folder {FOLDER_NAME}
    """

    # logging, debug level, to file {application_run.log}
    logging.basicConfig(
        filename='application_run.log',
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    current_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('\n"device_config_collection.py" App Run Start, ', current_time)

    # Create a DNACenterAPI "Connection Object"
    dnac_api = DNACenterAPI(username=DNAC_USER, password=DNAC_PASS, base_url=DNAC_URL, version='2.1.2', verify=False)

    # find the Cisco DNA Center device count
    devices_count = dnac_api.devices.get_device_count()['response']
    print('\nThe number of devices managed by Cisco DNA Center is:', devices_count)

    # collect the device info for all devices managed by Cisco DNA Center
    devices_list = []
    remaining_device_count = devices_count
    device_offset = 1
    device_limit = 500
    while remaining_device_count > 0:
        device_info = dnac_api.devices.get_device_list(offset=device_offset, limit=device_limit)
        devices_list.extend(device_info['response'])
        device_offset += device_limit
        remaining_device_count -= device_limit

    # create a folder to save the reports to
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)

    # collect device config and save to file
    for device in devices_list:
        device_hostname = device['hostname']
        device_id = device['id']

        filename_path = FOLDER_NAME + '/' + device_hostname
        try:
            # not all Cisco DNA Center devices have a configuration file, for example AP's
            # attempting to read the configuraiton file will create an error
            config_str = dnac_api.devices.get_device_config_by_id(device_id)['response']

            # save the configuration file and path defined
            with open(filename_path, 'w') as filehandle:
                filehandle.write('%s\n' % config_str)
                print('Saved configuration file with the name: ', filename_path)
        except:
            pass

    current_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('\n"device_config_collection.py" App Run End, ', current_time)


if __name__ == '__main__':
    main()