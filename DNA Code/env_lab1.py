# User Input

# Please select the lab environment that you will be using today
#     sandbox - Cisco DevNet Always-On / Reserved Sandboxes
#     express - Cisco DevNet Express Lab Backend
#     custom  - Your Own "Custom" Lab Backend
ENVIRONMENT_IN_USE = "sandbox"

# Set the 'Environment Variables' based on the lab environment in use
#if ENVIRONMENT_IN_USE == "sandbox":
#    dnac = {
#        "host": "sandboxdnac2.cisco.com",
#        "port": 443,
#        "username": "devnetuser",
#        "password": "Cisco123!"
#    }
 
if ENVIRONMENT_IN_USE == "sandbox":
    dnac = {
        "host": "198.18.129.100",
        "port": 443,
        "username": "admin",
        "password": "C1sco12345"
    }
 
#import os
#DNAC= os.getenv("DNAC") or "sandboxdnac2.cisco.com"
##DNAC= os.getenv("DNAC") or "sandboxdnac2.cisco.com"
#DNAC_USER= os.getenv("DNAC_USER") or "devnetuser"
#DNAC_PORT=os.getenv("DNAC_PORT") or 443
##DNAC_PORT=os.getenv("DNAC_PORT") or 8080
#DNAC_PASSWORD= os.getenv("DNAC_PASSWORD") or "Cisco123!"
#DNAC_PASS= os.getenv("DNAC_PASSWORD") or "Cisco123!"
#DNAC_URL= os.getenv("DNAC") or "https://sandboxdnac.cisco.com"


DNAC = '198.18.129.100'
DNAC_IP = '198.18.129.100'
DNAC_URL = 'https://' + DNAC_IP
DNAC_USER = 'admin'
DNAC_USERNAME = 'admin'
DNAC_PASSWORD = 'C1sco12345'
DNAC_PASS = 'C1sco12345'
DNAC_PORT = 443


 
DEVICE_NAME = 'PDX-RN'
DEVICE_TYPES = ['Cisco Catalyst38xx stack-able ethernet switch', 'Cisco Catalyst 9300 Switch' , 'Cisco Catalyst 2960-24PC-L Switch']
#DEVICE_ROLE = ['CORE']
DEVICE_FAMILY = ['Switches and Hubs', 'Routers']
DEVICE_ROLE = ['DISTRIBUTION','ACCESS']

# Proximity API config params
DAYS = 14  # number of days to search for contact tracing
TIME_RESOLUTION = 5  # 15 minutes time resolution

# Proximity API event and subscription
EVENT_ID = 'NETWORK-CLIENTS-3-506'
SUBSCRIPTION_NAME = 'Proximity Event Subscription'

PARAMS = {'interface_number': '101', 'ip_address': '101.100.100.100'}
PROJECT_J2 = 'DayN Template'
MANAGEMENT_INT_J2 = 'management_interface.j2'
NTP_SERVER_J2 = 'ntp_server.j2'
DEPLOY_PROJECT = 'DayN Template'
DEPLOY_TEMPLATE = 'Disable Access Port'

