# !/usr/bin/env python3

import requests
import urllib3
from requests.auth import HTTPBasicAuth  # for Basic Auth
from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings
import dnac_apis1
import utils
from env_lab import DNAC_URL, DNAC_PASS, DNAC_USER
urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)

#dnac_auth = dnac_apis1.get_dnac_jwt_token(DNAC_AUTH)
#print (dnac_auth)


def main():
    """
    This simple script will find out if there is a client connected to the Enterprise network
    It will ask the user to input an IP address for a client device.
    It will print information if the input IP address is being used by a client or not
    """

    dnac_auth = dnac_apis1.get_dnac_jwt_token(DNAC_AUTH)
    # input IP address for client

    client_ip_address = utils.get_input_ip()
    print('IP Address to be validated:', client_ip_address)

    # check if the input IP address is used by network clients

    dnac_apis1.check_client_ip_address(client_ip_address)



if __name__ == '__main__':
    main()
