import urllib3
import datetime
import json
import time
import logging
import dnacentersdk

from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings
from requests.auth import HTTPBasicAuth  # for Basic Auth

from env_lab import DNAC_URL, DNAC_PASS, DNAC_USER
from dnacentersdk import DNACenterAPI

urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)


def main():
    """
    This application will identify all Cisco DNA Center devices that are in one of these 'un-x' states:
    - un-claimed in the PnP inventory
    - un-assigned to a site
    - un-reachable by Cisco DNA Center
    It will create a report with the hostname and platform Id for these devices
    """

    # logging, debug level, to file {application_run.log}
    logging.basicConfig(
        filename='application_run.log',
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    current_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('\n"un-x_devices_report.py" App Run Start, ', current_time)

    # Create a DNACenterAPI "Connection Object"
    dnac_api = DNACenterAPI(username=DNAC_USER, password=DNAC_PASS, base_url=DNAC_URL, version='2.1.2', verify=False)

    # find all devices that are unclaimed in the PnP inventory
    devices_unclaimed = []
    devices_unclaimed_info = dnac_api.device_onboarding_pnp.get_device_list(state='Unclaimed')

    if devices_unclaimed_info == []:
        print('\nNo unclaimed devices found')
    else:
        for device in devices_unclaimed_info:
            devices_unclaimed.append({'hostname': device['deviceInfo']['hostname'], 'pid': device[
                'deviceInfo']['pid']})
        print('\n\nUnclaimed devices found:')
        print('{0:30} {1:30}'.format('Device Hostname', 'Device PID'))
        for device in devices_unclaimed:
            print('{0:30} {1:30}'.format(device['hostname'], device['pid']))

    # find all devices that are unreachable
    devices_unreachable = []
    devices_unreachable_info = dnac_api.devices.get_device_list(reachability_status='Unreachable')
    devices_unreachable_json = devices_unreachable_info['response']

    if devices_unreachable_json == []:
        print('\nNo unreachable devices found')
    else:
        for device in devices_unreachable_json:
            devices_unreachable.append({'hostname': device['hostname'], 'pid': device['platformId']})
        print('\n\nUnreachable devices found:')
        print('{0:30} {1:30}'.format('Device Hostname', 'Device PID'))
        for device in devices_unreachable:
            print('{0:30} {1:30}'.format(device['hostname'], device['pid']))

    # find all devices that are unassigned to a site
    # we will find this information from the site membership API using the {Global} site id
    global_site_info = dnac_api.sites.get_site(name='Global')
    global_site_id = global_site_info['response'][0]['id']

    site_membership_info = dnac_api.sites.get_membership(site_id=global_site_id)

    devices_unassigned = []
    devices_unassigned_info = site_membership_info['device'][0]['response']

    if devices_unassigned_info == []:
        print('\nNo unassigned devices found')
    else:
        for device in devices_unassigned_info:
            devices_unassigned.append({'hostname': device['hostname'], 'pid': device['platformId']})
        print('\n\nUnassigned devices found:')
        print('{0:30} {1:30}'.format('Device Hostname', 'Device PID'))
        for device in devices_unassigned:
            print('{0:30} {1:30}'.format(device['hostname'], device['pid']))

    current_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('\n"un-x_devices_report.py" App Run End, ', current_time)


if __name__ == '__main__':
    main()