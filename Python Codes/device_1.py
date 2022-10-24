import requests

login_url = 'https://10.10.20.90:8443/j_security_check'
login_credentials = {'j_username':'admin', 'j_password':'admin'}

session = requests.session()

response = session.post(url=login_url, data=login_credentials, verify=False)

if b'<html>' in response.content:
    print('Login Failed')
else:
    print('Login Success')

---------------------------
import json

device_list_url = 'https://10.10.20.90:8443/dataservice/device'

response = session.get(url=device_list_url, verify=False)
response = json.loads(response.content)

for device in response['data']:
    print(device['host-name'], device['local-system-ip'], device['uuid'])