from requests import get, post
import json
from base64 import b64encode
from argparse import ArgumentParser
from re import match
import csv
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_endpoint_details(endpoint, headers, ise_address):
    endpoint_href = endpoint["link"]["href"]
    endpoint_mac, endpoint_group_id = get_endpoint_by_id(endpoint_href, headers)
    endpoint_group_name = get_endpoint_group_name(endpoint_group_id, headers, ise_address)    
    return([endpoint_mac, endpoint_group_name])

def get_endpoint_by_id(url, headers):
    response = get(url, headers=headers, verify=False)
    endpoint_mac = response.json()["ERSEndPoint"]["mac"]
    endpoint_group_id = response.json()["ERSEndPoint"]["groupId"]
    return([endpoint_mac, endpoint_group_id])

def get_endpoint_group_name(group_id, headers, ise_address):
    url = f"https://{ise_address}:9060/ers/config/endpointgroup/{group_id}"
    response = get(url, headers=headers, verify=False)
    group_name = response.json()["EndPointGroup"]["name"]
    return(group_name)

if __name__ == '__main__':

    # script arguments
    parser: ArgumentParser = ArgumentParser(description='Export desired endpoints from Cisco ISE Server to a ready to import csv')
    parser.add_argument('--ise', help='IP Address or FQDN of ISE Server', type=str, required=True)
    parser.add_argument('-u', '--user', help='username to authenticate on ISE', type=str, required=True)
    parser.add_argument('-p', '--password', help='password to authenticate on ISE', type=str, required=True)
    parser.add_argument('-f', '--filter', help='collect info only for endpoint groups containing this (optional)', default="", type=str, required=False)
    args = parser.parse_args()
    
    # Basic Authentication is required
    credentials = b64encode((args.user + ":" + args.password).encode()).decode()
    # header with authentication
    headers = {"Content-Type": "application/json", 'Accept': 'application/json', 'Authorization': "Basic "+ credentials}
    url = f"https://{args.ise}:9060/ers/config/endpoint"
            
    # GET Request to get all endpoints from ISE Server        
    response = get(url, data="", headers=headers, verify=False)
    
    if response.status_code == 200:
        with open('export_endpoints.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, lineterminator="\r\n", delimiter=',')
            csv_writer.writerow(["MAC","Endpoint Policy","Endpoint Identity Group"])
            # Continue as long as there is a next page of endpoints :)
            while True:
                endpoint_list = response.json()["SearchResult"]["resources"]            
                for endpoint in endpoint_list:
                    endpoint_mac, endpoint_group_name = get_endpoint_details(endpoint, headers, args.ise)
                    if match(args.filter, endpoint_group_name):
                        print(f'[-] Collecting info for endpoint named {endpoint["name"]}')
                        print(f'\tEndpoint MAC Address: {endpoint_mac}\n\tEndpoint Group: {str(endpoint_group_name)}')
                        csv_writer.writerow([endpoint_mac,"", endpoint_group_name])
                # Check if there is a next page of endpoints
                try:
                    url = response.json()["SearchResult"]["nextPage"]["href"]
                except:
                    break
                response = get(url, data="", headers=headers, verify=False)