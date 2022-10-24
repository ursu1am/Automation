# Cisco DNA sandbox login details 
DNAC= "sandboxdnac.cisco.com"
DNAC_USER= "devnetuser"
DNAC_PORT= 443
DNAC_PASS= "Cisco123!"
DNAC_URL= "https://sandboxdnac.cisco.com"


## dcloud login details 
#DNAC = '198.18.129.100'
#DNAC_IP = '198.18.129.100'
#DNAC_URL = 'https://' + DNAC_IP
#DNAC_USER = 'admin'
##DNAC_USERNAME = 'admin'
#DNAC_PASSWORD = 'C1sco12345'
#DNAC_PASS = 'C1sco12345'
#DNAC_PORT = 443

# folder name
FOLDER_NAME = 'device_configs'


DEVICE_NAME = 'PDX-RN'
DEVICE_TYPES = ['Cisco Catalyst38xx stack-able ethernet switch', 'Cisco Catalyst 9300 Switch' , 'Cisco Catalyst 2960-24PC-L Switch']
#DEVICE_ROLE = ['CORE']
DEVICE_FAMILY = ['Switches and Hubs', 'Routers']
DEVICE_ROLE = ['DISTRIBUTION','ACCESS']


# Set the 'Environment Variables' based on the lab environment in use
ENVIRONMENT_IN_USE = "sandbox"
if ENVIRONMENT_IN_USE == "sandbox":
    apicem = {
        "host": "sandboxdnac.cisco.com",
        "port": 443,
        "username": "devnetuser",
        "password": "Cisco123!"
    }