import sys
import requests
import json
import time
import urllib3
import http.client
#import utils
#from getpass import getpass
from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings
from requests.auth import HTTPBasicAuth  # for Basic Auth
#from dnac_config import DNAC, DNAC_PORT, DNAC_USER, DNAC_PASSWORD
from env_lab import DNAC_URL, DNAC_USER, DNAC_PASS
#from env_lab import DNAC_URL, DNAC_PORT, DNAC_USER, DNAC_PASS

urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings
#print ('Please Enter your password to proceed ')
#DNAC_PASS = getpass()
DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)


def pprint(json_data):
    """
    Pretty print JSON formatted data
    :param json_data: data to pretty print
    :return:
    """
    print(json.dumps(json_data, indent=0, separators=(',', ':'))) #<-- this used for logs & tasks programms 
    #print(json.dumps(json_data, indent=4, separators=(' , ', ' : ')))
    

def get_dnac_jwt_token(dnac_auth):
    """
    Create the authorization token required to access DNA C
    Call to DNA C - /api/system/v1/auth/login
    :param dnac_auth - DNA C Basic Auth string
    :return: DNA C JWT token
    """

    url = DNAC_URL + '/api/system/v1/auth/token'
    header = {'content-type': 'application/json'}
    response = requests.post(url, auth=dnac_auth, headers=header, verify=False)
    dnac_jwt_token = response.json()['Token']
    return dnac_jwt_token


def get_all_device_info(dnac_jwt_token):
    """
    The function will return all network devices info
    :param dnac_jwt_token: DNA C token
    :return: DNA C device inventory info
    """
    url = DNAC_URL + '/api/v1/network-device'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    all_device_response = requests.get(url, headers=header, verify=False)
    all_device_info = all_device_response.json()
    return all_device_info['response']


def get_device_info(device_id, dnac_jwt_token):
    """
    This function will retrieve all the information for the device with the DNA C device id
    :param device_id: DNA C device_id
    :param dnac_jwt_token: DNA C token
    :return: device info
    """
    url = DNAC_URL + '/api/v1/network-device?id=' + device_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    device_response = requests.get(url, headers=header, verify=False)
    device_info = device_response.json()
    return device_info['response'][0]

def get_device_info(device_id, dnac_jwt_token):
    """
    This function will retrieve all the information for the device with the DNA C device id
    :param device_id: DNA C device_id
    :param dnac_jwt_token: Cisco DNA Center token
    :return: device info
    """
    url = DNAC_URL + '/dna/intent/api/v1/network-device?id=' + device_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    device_response = requests.get(url, headers=header, verify=False)
    device_info = device_response.json()
    return device_info['response'][0]


def delete_device(device_id, dnac_jwt_token):
    """
    This function will delete the device with the {device_id} from the DNA Center inventory
    :param device_id: DNA C device_id
    :param dnac_jwt_token: Cisco DNA Center token
    :return: delete status
    """
    url = DNAC_URL + '/dna/intent/api/v1/network-device/' + device_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.delete(url, headers=header, verify=False)
    delete_response = response.json()
    delete_status = delete_response['response']
    return delete_status


def get_project_id(project_name, dnac_jwt_token):
    """
    This function will retrieve the CLI templates project id for the project with the name {project_name}
    :param project_name: CLI project name
    :param dnac_jwt_token: Cisco DNA Center token
    :return: project id
    """
    url = DNAC_URL + '/dna/intent/api/v1/template-programmer/project?name=' + project_name
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    project_json = response.json()
    project_id = project_json[0]['id']
    return project_id


def create_project(project_name, dnac_jwt_token):
    """
    This function will create a new project with the name {project_name}.
    - if the project exists, return the project id
    - if the project does not exist it will create a new project, waiting for the task to be completed
     and return the project id
    :param project_name: project name
    :param dnac_jwt_token: Cisco DNA Center token
    :return: project id, or none if creating a new project fails
    """

    # check if project exists
    url = DNAC_URL + '/dna/intent/api/v1/template-programmer/project?name=' + project_name
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    project_json = response.json()
    # if project does not exist, project_json value is []. We need to create the project
    if project_json == []:
        # project does not exist
        payload = {'name': project_name}
        url = DNAC_URL + '/dna/intent/api/v1/template-programmer/project'
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
        task_json = response.json()
        task_info = task_json['response']
        task_id = task_info['taskId']
        task_result = check_task_id_status(task_id, dnac_jwt_token)
        project_id = task_result['data']
    else:
        # project exists
        project_id = project_json[0]['id']
    return project_id


def delete_project(project_name, dnac_jwt_token):
    """
    This function will retrieve the CLI templates project id for the project with the name {project_name}
    :param project_name: CLI project name
    :param dnac_jwt_token: Cisco DNA Center token
    :return: project id
    """
    project_id = get_project_id(project_name, dnac_jwt_token)
    url = DNAC_URL + '/dna/intent/api/v1/template-programmer/project/' + project_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.delete(url, headers=header, verify=False)


def get_project_info(project_name, dnac_jwt_token):
    """
    This function will retrieve all templates associated with the project with the name {project_name}
    :param project_name: project name
    :param dnac_jwt_token: Cisco DNA Center token
    :return: list of all templates, including names and ids
    """
    url = DNAC_URL + '/dna/intent/api/v1/template-programmer/project?name=' + project_name
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    project_json = response.json()
    template_list = project_json[0]['templates']
    return template_list


def create_commit_template(template_name, project_name, cli_template, dnac_jwt_token):
    """
    This function will create and commit a CLI template, under the project with the name {project_name}, with the the text content
    {cli_template}
    :param template_name: CLI template name
    :param project_name: Project name
    :param cli_template: CLI template text content
    :param dnac_jwt_token: Cisco DNA Center token
    :return:
    """
    project_id = get_project_id(project_name, dnac_jwt_token)

    # prepare the template param to sent to DNA C
    payload = {
            "name": template_name,
            "description": "Remote router configuration",
            "tags": [],
            "author": "admin",
            "deviceTypes": [
                {
                    "productFamily": "Routers"
                },
                {
                    "productFamily": "Switches and Hubs"
                }
            ],
            "softwareType": "IOS-XE",
            "softwareVariant": "XE",
            "softwareVersion": "",
            "templateContent": cli_template,
            "rollbackTemplateContent": "",
            "templateParams": [],
            "rollbackTemplateParams": [],
            "parentTemplateId": project_id
        }

    # check and delete older versions of the template
    # template_id = get_template_id(template_name, project_name, dnac_jwt_token)
    # if template_id:
    #    delete_template(template_name, project_name, dnac_jwt_token)

    # create the new template
    url = DNAC_URL + '/dna/intent/api/v1/template-programmer/project/' + project_id + '/template'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)

    # get the template id
    template_id = get_template_id(template_name, project_name, dnac_jwt_token)

    # commit template
    commit_template(template_id, 'committed by Python script', dnac_jwt_token)


def commit_template(template_id, comments, dnac_jwt_token):
    """
    This function will commit the template with the template id {template_id}
    :param template_id: template id
    :param comments: text with comments
    :param dnac_jwt_token: Cisco DNA Center token
    :return:
    """
    url = DNAC_URL + '/dna/intent/api/v1/template-programmer/template/version'
    payload = {
            "templateId": template_id,
            "comments": comments
        }
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)


def update_commit_template(template_name, project_name, cli_template, dnac_jwt_token):
    """
    This function will update an existing template
    :param template_name: template name
    :param project_name: project name
    :param cli_template: CLI template text content
    :param dnac_jwt_token: Cisco DNA Center token
    :return:
    """
    # get the project id
    project_id = get_project_id(project_name, dnac_jwt_token)

    # get the template id
    template_id = get_template_id(template_name, project_name, dnac_jwt_token)
    url = DNAC_URL + '/dna/intent/api/v1/template-programmer/template'

    # prepare the template param to sent to DNA C
    payload = {
        "name": template_name,
        "description": "Remote router configuration",
        "tags": [],
        "id": template_id,
        "author": "admin",
        "deviceTypes": [
            {
                "productFamily": "Routers"
            },
            {
                "productFamily": "Switches and Hubs"
            }
        ],
        "softwareType": "IOS-XE",
        "softwareVariant": "XE",
        "softwareVersion": "",
        "templateContent": cli_template,
        "rollbackTemplateContent": "",
        "templateParams": [],
        "rollbackTemplateParams": [],
        "parentTemplateId": project_id
    }
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.put(url, data=json.dumps(payload), headers=header, verify=False)
    print(response.text)
    # commit template
    response = commit_template(template_id, 'committed by Python script', dnac_jwt_token)
    print(response.text)


def upload_template(template_name, project_name, cli_template, dnac_jwt_token):
    """
    This function will create, or will update an existing template, and deploy the new template
    :param template_name: template name
    :param project_name: project name
    :param cli_template: CLI template text content
    :param dnac_jwt_token: Cisco DNA Center token
    :return:
    """
    template_id = get_template_id(template_name, project_name, dnac_jwt_token)
    if template_id:
        update_commit_template(template_name, project_name, cli_template, dnac_jwt_token)
    else:
        create_commit_template(template_name, project_name, cli_template, dnac_jwt_token)


def delete_template(template_name, project_name, dnac_jwt_token):
    """
    This function will delete the template with the name {template_name}
    :param template_name: template name
    :param project_name: Project name
    :param dnac_jwt_token: Cisco DNA Center token
    :return:
    """
    template_id = get_template_id(template_name, project_name, dnac_jwt_token)
    url = DNAC_URL + '/dna/intent/api/v1/template-programmer/template/' + template_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.delete(url, headers=header, verify=False)


def get_all_template_info(dnac_jwt_token):
    """
    This function will return the info for all CLI templates existing on DNA C, including all their versions
    :param dnac_jwt_token: Cisco DNA Center token
    :return: all info for all templates
    """
    url = DNAC_URL + '/dna/intent/api/v1/template-programmer/template'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    all_template_list = response.json()
    return all_template_list


def get_template_name_info(template_name, project_name, dnac_jwt_token):
    """
    This function will return the info for the CLI template with the name {template_name}
    :param template_name: template name
    :param project_name: Project name
    :param dnac_jwt_token: Cisco DNA Center token
    :return: all info for all templates
    """
    template_id = get_template_id(template_name, project_name, dnac_jwt_token)
    url = DNAC_URL + '/dna/intent/api/v1/template-programmer/template/' + template_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    template_json = response.json()
    return template_json


def get_template_id(template_name, project_name, dnac_jwt_token):
    """
    This function will return the latest version template id for the DNA C template with the name {template_name},
    part of the project with the name {project_name}
    :param template_name: name of the template
    :param project_name: Project name
    :param dnac_jwt_token: Cisco DNA Center token
    :return: DNA C template id
    """
    template_list = get_project_info(project_name, dnac_jwt_token)
    template_id = None
    for template in template_list:
        if template['name'] == template_name:
            template_id = template['id']
    return template_id


def send_deploy_template(template_name, project_name, device_name, dnac_jwt_token):
    """
    This function will deploy the template with the name {template_name} to the network device with the name
    {device_name}
    :param template_name: template name
    :param project_name: project name
    :param device_name: device hostname
    :param dnac_jwt_token: Cisco DNA Center token
    :return: the deployment task id
    """
    template_id = get_template_id_version(template_name, project_name, dnac_jwt_token)
    payload = {
            "templateId": template_id,
            "targetInfo": [
                {
                    "id": device_name,
                    "type": "MANAGED_DEVICE_HOSTNAME",
                    "params": {}
                }
            ]
        }
    url = DNAC_URL + '/dna/intent/api/v1/template-programmer/template/deploy'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    deployment = requests.post(url, headers=header, data=json.dumps(payload), verify=False)
    deployment_json = deployment.json()
    depl_task_id = deployment_json["deploymentId"].split(' ')[-1]
    return depl_task_id


def check_template_deployment_status(depl_task_id, dnac_jwt_token):
    """
    This function will check the result for the deployment of the CLI template with the id {depl_task_id}
    :param depl_task_id: template deployment id
    :param dnac_jwt_token: Cisco DNA Center token
    :return: status - {SUCCESS} or {FAILURE}
    """
    url = DNAC_URL + '/dna/intent/api/v1/template-programmer/template/deploy/status/' + depl_task_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    response_json = response.json()
    deployment_status = response_json["status"]
    return deployment_status


def get_client_info(client_ip, dnac_jwt_token):
    """
    This function will retrieve all the information from the client with the IP address
    Deprecated, do not use
    :param client_ip: client IPv4 address
    :param dnac_jwt_token: Cisco DNA Center token
    :return: client info, or {None} if client does not found
    """
    url = DNAC_URL + '/api/v1/host?hostIp=' + client_ip
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    client_json = response.json()
    try:
        client_info = client_json['response'][0]
        return client_info
    except:
        return None


def locate_client_ip(client_ip, dnac_jwt_token):
    """
    Locate a wired client device in the infrastructure by using the client IP address
    Call to DNA C - api/v1/host?hostIp={client_ip}
    Deprecated, do not use
    :param client_ip: Client IP Address
    :param dnac_jwt_token: Cisco DNA Center token
    :return: hostname, interface_name, vlan_id, or None, if the client does not exist
    """

    client_info = get_client_info(client_ip, dnac_jwt_token)
    if client_info is not None:
        hostname = client_info['connectedNetworkDeviceName']
        interface_name = client_info['connectedInterfaceName']
        vlan_id = client_info['vlanId']
        return hostname, interface_name, vlan_id
    else:
        return None


def get_device_id_name(device_name, dnac_jwt_token):
    """
    This function will find the DNA C device id for the device with the name {device_name}
    :param device_name: device hostname
    :param dnac_jwt_token: Cisco DNA Center token
    :return:
    """
    device_id = None
    device_list = get_all_device_info(dnac_jwt_token)
    for device in device_list:
        if device['hostname'] == device_name:
            device_id = device['id']
    return device_id


def get_device_status(device_name, dnac_jwt_token):
    """
    This function will return the reachability status for the network device with the name {device_name}
    :param device_name: device name
    :param dnac_jwt_token: Cisco DNA Center token
    :return: status - {UNKNOWN} to locate a device in the database,
                      {SUCCESS} device reachable
                      {FAILURE} device not reachable
    """
    device_id = get_device_id_name(device_name, dnac_jwt_token)
    if device_id is None:
        return 'UNKNOWN'
    else:
        device_info = get_device_info(device_id, dnac_jwt_token)
        if device_info['reachabilityStatus'] == 'Reachable':
            return 'SUCCESS'
        else:
            return 'FAILURE'


def get_device_management_ip(device_name, dnac_jwt_token):
    """
    This function will find out the management IP address for the device with the name {device_name}
    :param device_name: device name
    :param dnac_jwt_token: Cisco DNA Center token
    :return: the management ip address
    """
    device_ip = None
    device_list = get_all_device_info(dnac_jwt_token)
    for device in device_list:
        if device['hostname'] == device_name:
            device_ip = device['managementIpAddress']
    return device_ip


def get_device_id_sn(device_sn, dnac_jwt_token):
    """
    The function will return the DNA C device id for the device with serial number {device_sn}
    :param device_sn: network device SN
    :param dnac_jwt_token: Cisco DNA Center token
    :return: DNA C device id
    """
    url = DNAC_URL + '/dna/intent/api/v1/network-device/serial-number/' + device_sn
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    device_response = requests.get(url, headers=header, verify=False)
    device_info = device_response.json()
    device_id = device_info['response']['id']
    return device_id


def sync_device(device_name, dnac_jwt_token):
    """
    This function will sync the device configuration from the device with the name {device_name}
    :param device_name: device hostname
    :param dnac_jwt_token: Cisco DNA Center token
    :return: the response status code, 202 if sync initiated, and the task id
    """
    device_id = get_device_id_name(device_name, dnac_jwt_token)
    param = [device_id]
    url = DNAC_URL + '/dna/intent/api/v1/network-device/sync?forceSync=true'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    sync_response = requests.put(url, data=json.dumps(param), headers=header, verify=False)
    task = sync_response.json()['response']['taskId']
    return sync_response.status_code, task


def check_task_id_status(task_id, dnac_jwt_token):
    """
    This function will check the status of the task with the id {task_id}
    :param task_id: task id
    :param dnac_jwt_token: Cisco DNA Center token
    :return: status - {SUCCESS} or {FAILURE}, and the task status message
    """
    # loop until the task is completed, check status every second
    task_result = ''

    while task_result == '':
        time.sleep(1)
        url = DNAC_URL + '/dna/intent/api/v1/task/' + task_id
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        task_response = requests.get(url, headers=header, verify=False)
        task_json = task_response.json()
        task_status = task_json['response']
        print(task_status)
        if 'endTime' in task_status.keys():
            return task_status


def check_task_id_output(task_id, dnac_jwt_token):
    """
    This function will check the status of the task with the id {task_id}.
    Loop one seconds increments until task is completed.
    :param task_id: task id
    :param dnac_jwt_token: Cisco DNA Center token
    :return: status - {SUCCESS} or {FAILURE}
    """
    url = DNAC_URL + '/dna/intent/api/v1/task/' + task_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    completed = 'no'
    while completed == 'no':
        try:
            task_response = requests.get(url, headers=header, verify=False)
            task_json = task_response.json()
            task_output = task_json['response']
            # check if file id available in output
            file_info = json.loads(task_output['progress'])
            completed = 'yes'
        finally:
            time.sleep(1)
    return task_output


def create_path_trace(src_ip, dest_ip, dnac_jwt_token):
    """
    This function will create a new Path Trace between the source IP address {src_ip} and the
    destination IP address {dest_ip}
    :param src_ip: Source IP address
    :param dest_ip: Destination IP address
    :param dnac_jwt_token: Cisco DNA Center token
    :return: DNA C path visualisation id
    """

    param = {
        'destIP': dest_ip,
        'periodicRefresh': False,
        'sourceIP': src_ip
    }

    url = DNAC_URL + '/dna/intent/api/v1/flow-analysis'
    header = {'accept': 'application/json', 'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    path_response = requests.post(url, data=json.dumps(param), headers=header, verify=False)
    path_json = path_response.json()
    path_id = path_json['response']['flowAnalysisId']
    return path_id


def get_path_trace_info(path_id, dnac_jwt_token):
    """
    This function will return the path trace details for the path visualisation {id}
    :param path_id: DNA C path visualisation id
    :param dnac_jwt_token: Cisco DNA Center token
    :return: Path visualisation status, and the details in a list [device,interface_out,interface_in,device...]
    """

    url = DNAC_URL + '/dna/intent/api/v1/flow-analysis/' + path_id
    header = {'accept': 'application/json', 'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    path_response = requests.get(url, headers=header, verify=False)
    path_json = path_response.json()
    path_info = path_json['response']
    path_status = path_info['request']['status']
    path_list = []
    if path_status == 'COMPLETED':
        network_info = path_info['networkElementsInfo']
        path_list.append(path_info['request']['sourceIP'])
        for elem in network_info:
            try:
                path_list.append(elem['ingressInterface']['physicalInterface']['name'])
            except:
                pass
            try:
                path_list.append(elem['name'])
            except:
                pass
            try:
                path_list.append(elem['egressInterface']['physicalInterface']['name'])
            except:
                pass
        path_list.append(path_info['request']['destIP'])
    return path_status, path_list


def check_ipv4_network_interface(ip_address, dnac_jwt_token):
    """
    This function will check if the provided IPv4 address is configured on any network interfaces
    :param ip_address: IPv4 address
    :param dnac_jwt_token: Cisco DNA Center token
    :return: None, or device_hostname and interface_name
    """
    url = DNAC_URL + '/dna/intent/api/v1/interface/ip-address/' + ip_address
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    response_json = response.json()
    try:
        response_info = response_json['response'][0]
        interface_name = response_info['portName']
        device_id = response_info['deviceId']
        device_info = get_device_info(device_id, dnac_jwt_token)
        device_hostname = device_info['hostname']
        return device_hostname, interface_name
    except:
        device_info = get_device_info_ip(ip_address, dnac_jwt_token)  # required for AP's
        device_hostname = device_info['hostname']
        return device_hostname, ''


def get_device_info_ip(ip_address, dnac_jwt_token):
    """
    This function will retrieve the device information for the device with the management IPv4 address {ip_address}
    :param ip_address: device management ip address
    :param dnac_jwt_token: Cisco DNA Center token
    :return: device information, or None
    """
    url = DNAC_URL + '/dna/intent/api/v1/network-device/ip-address/' + ip_address
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    response_json = response.json()
    device_info = response_json['response']
    if 'errorCode' == 'Not found':
        return None
    else:
        return device_info


def get_legit_cli_command_runner(dnac_jwt_token):
    """
    This function will get all the legit CLI commands supported by the {command runner} APIs
    :param dnac_jwt_token: Cisco DNA Center token
    :return: list of CLI commands
    """
    url = DNAC_URL + '/dna/intent/api/v1/network-device-poller/cli/legit-reads'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    response_json = response.json()
    cli_list = response_json['response']
    return cli_list


def get_content_file_id(file_id, dnac_jwt_token):
    """
    This function will download the file specified by the {file_id}
    :param file_id: file id
    :param dnac_jwt_token: Cisco DNA Center token
    :return: file
    """
    url = DNAC_URL + '/dna/intent/api/v1/file/' + file_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False, stream=True)
    response_json = response.json()
    return response_json


def get_output_command_runner(command, device_name, dnac_jwt_token):
    """
    This function will return the output of the CLI command specified in the {command}, sent to the device with the
    hostname {device}
    :param command: CLI command
    :param device_name: device hostname
    :param dnac_jwt_token: Cisco DNA Center token
    :return: file with the command output
    """

    # get the Cisco DNA Center device id
    device_id = get_device_id_name(device_name, dnac_jwt_token)

    # get the Cisco DNA Center task id that will execute the CLI command runner
    payload = {
        "commands": [command],
        "deviceUuids": [device_id],
        "timeout": 0
        }
    url = DNAC_URL + '/dna/intent/api/v1/network-device-poller/cli/read-request'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    response_json = response.json()
    try:
        task_id = response_json['response']['taskId']
    except:
        print('\n' + response_json['response']['detail'])
        return

    # get task id status
    # wait 2 second for the command runner task to be started
    time.sleep(2)
    task_result = check_task_id_output(task_id, dnac_jwt_token)
    file_info = json.loads(task_result['progress'])
    file_id = file_info['fileId']

    # get output from file
    time.sleep(2)  # wait for 2 seconds for the file to be ready
    file_output = get_content_file_id(file_id, dnac_jwt_token)
    command_responses = file_output[0]['commandResponses']
    if command_responses['SUCCESS'] != {}:
        command_output = command_responses['SUCCESS'][command]
    elif command_responses['FAILURE'] != {}:
        command_output = command_responses['FAILURE'][command]
    else:
        command_output = command_responses['BLACKLISTED'][command]
    return command_output


def get_all_configs(dnac_jwt_token):
    """
    This function will retrieve all the devices configurations
    :param dnac_jwt_token: Cisco DNA Center token
    :return: Return all config files in a list
    """
    url = DNAC_URL + '/dna/intent/api/v1/network-device/config'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    config_json = response.json()
    config_files = config_json['response']
    return config_files


def get_device_config(device_name, dnac_jwt_token):
    """
    This function will get the configuration file for the device with the name {device_name}
    :param device_name: device hostname
    :param dnac_jwt_token: Cisco DNA Center token
    :return: configuration file
    """
    device_id = get_device_id_name(device_name, dnac_jwt_token)
    url = DNAC_URL + '/dna/intent/api/v1/network-device/' + device_id + '/config'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    config_json = response.json()
    config_file = config_json['response']
    return config_file


def check_ipv4_address(ipv4_address, dnac_jwt_token):
    """
    This function will find if the IPv4 address is configured on any network interfaces or used by any hosts.
    :param ipv4_address: IPv4 address
    :param dnac_jwt_token: Cisco DNA Center token
    :return: True/False
    """
    # check against network devices interfaces
    try:
        device_info = check_ipv4_network_interface(ipv4_address, dnac_jwt_token)
        return True
    except:
        # check against any hosts
        try:
            client_info = get_client_info(ipv4_address, dnac_jwt_token)
            if client_info is not None:
                return True
        except:
            pass
    return False


def check_ipv4_address_configs(ipv4_address, dnac_jwt_token):
    """
    This function will verify if the IPv4 address is present in any of the configurations of any devices
    :param ipv4_address: IPv4 address
    :param dnac_jwt_token: Cisco DNA Center token
    :return: True/False
    """
    url = DNAC_URL + '/dna/intent/api/v1/network-device/config'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    config_json = response.json()
    config_files = config_json['response']
    for config in config_files:
        run_config = config['runningConfig']
        if ipv4_address in run_config:
            return True
    return False


def check_ipv4_duplicate(config_file):
    """
    This function will:
      - load a file with a configuration to be deployed to a network device
      - identify the IPv4 addresses that will be configured on interfaces
      - search in the DNA Center database if these IPV4 addresses are configured on any interfaces
      - find if any clients are using the IPv4 addresses
      - Determine if deploying the configuration file will create an IP duplicate
    :param config_file: configuration file name
    :return True/False
    """

    # open file with the template
    cli_file = open(config_file, 'r')

    # read the file
    cli_config = cli_file.read()

    ipv4_address_list = utils.identify_ipv4_address(cli_config)

    # get the DNA Center Auth token

    dnac_token = get_dnac_jwt_token(DNAC_AUTH)

    # check each address against network devices and clients database
    # initialize duplicate_ip

    duplicate_ip = False
    for ipv4_address in ipv4_address_list:

        # check against network devices interfaces

        try:
            device_info = check_ipv4_network_interface(ipv4_address, dnac_token)
            duplicate_ip = True
        except:
            pass

        # check against any hosts

        try:
            client_info = get_client_info(ipv4_address, dnac_token)
            if client_info is not None:
                duplicate_ip = True
        except:
            pass

    if duplicate_ip:
        return True
    else:
        return False


def get_device_detail(device_name, epoch_time, dnac_jwt_token):
    """
    This function will call the device health intent API and return device management interface IPv4 address,
    serial number, family, software version, device health score, ... for the device with the name {device_name}
    :param device_name: device hostname
    :param epoch_time: epoch time including msec
    :param dnac_jwt_token: Cisco DNA Center token
    :return: detailed network device information
    """
    device_id = get_device_id_name(device_name, dnac_jwt_token)
    url = DNAC_URL + '/dna/intent/api/v1/device-detail?timestamp=' + str(epoch_time) + '&searchBy=' + device_id
    url += '&identifier=uuid'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    device_detail_json = response.json()
    device_detail = device_detail_json['response']
    return device_detail


def pnp_get_device_count(device_state, dnac_jwt_token):
    """
    This function will return the count of the PnP devices in the state {state}
    :param device_state: device state, example 'Unclaimed'
    :param dnac_jwt_token: Cisco DNA Center token
    :return: device count
    """
    url = DNAC_URL + '/dna/intent/api/v1/onboarding/pnp-device/count'
    payload = {'state': device_state}
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, data=json.dumps(payload), verify=False)
    pnp_device_count = response.json()
    return pnp_device_count['response']


def pnp_get_device_list(dnac_jwt_token):
    """
    This function will retrieve the PnP device list info
    :param dnac_jwt_token: Cisco DNA Center token
    :return: PnP device info
    """
    url = DNAC_URL + '/api/v1/onboarding/pnp-device'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    pnp_device_json = response.json()
    return pnp_device_json


def pnp_claim_ap_site(device_id, floor_id, rf_profile, dnac_jwt_token):
    """
    This function will delete claim the AP with the {device_id} to the floor with the {floor_id}
    :param device_id: Cisco DNA C device id
    :param floor_id: Cisco DNA C floor id
    :param rf_profile: RF profile - options - "LOW", "TYPICAL", "HIGH"
    :param dnac_jwt_token: Cisco DNA C token
    :return: claim operation status
    """
    payload = {
        "type": "AccessPoint",
        "siteId": floor_id,
        "deviceId": device_id,
        "rfProfile": rf_profile
        }
    url = DNAC_URL + '/dna/intent/api/v1/onboarding/pnp-device/site-claim'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.post(url, headers=header, data=json.dumps(payload), verify=False)
    claim_status_json = response.json()
    claim_status = claim_status_json['response']
    return claim_status


def pnp_delete_provisioned_device(device_id, dnac_jwt_token):
    """
    This function will delete the provisioned device with the {device_id} from the PnP database
    :param device_id: Cisco DNA C device id
    :param dnac_jwt_token: Cisco DNA C token
    :return: delete opearation status
    """
    url = DNAC_URL + '/dna/intent/api/v1/onboarding/pnp-device/' + device_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.delete(url, headers=header, verify=False)
    delete_status = response.json()
    return delete_status


def pnp_get_device_info(device_id, dnac_jwt_token):
    """
    This function will get the details for the a PnP device with the {device_id} from the PnP database
    :param device_id: Cisco DNA C device id
    :param dnac_jwt_token: Cisco DNA C token
    :return: device info in json format
    """
    url = DNAC_URL + '/dna/intent/api/v1/onboarding/pnp-device/' + device_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    device_info_json = response.json()
    device_info = device_info_json['deviceInfo']
    return device_info


def get_physical_topology(ip_address, dnac_jwt_token):
    """
    This function will retrieve the physical topology for the device/client with the {ip_address}
    :param ip_address: device/interface IP address
    :param dnac_jwt_token: Cisco DNA C token
    :return: topology info - connected device hostname and interface
    """
    url = DNAC_URL + '/dna/intent/api/v1/topology/physical-topology'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    topology_json = response.json()['response']
    topology_nodes = topology_json['nodes']
    topology_links = topology_json['links']

    # try to identify the physical topology
    for link in topology_links:
        try:
            if link['startPortIpv4Address'] == ip_address:
                connected_port = link['endPortName']
                connected_device_id = link['target']
                for node in topology_nodes:
                    if node['id'] == connected_device_id:
                        connected_device_hostname = node['label']
                break
        except:
            connected_port = None
            connected_device_hostname = None
    return connected_device_hostname, connected_port

"""
dnac_auth = get_dnac_jwt_token(DNAC_AUTH)
project = create_project('test', dnac_auth)
input('nay key to continue ')
delete_project('test', dnac_auth)
"""

def delete_device(device_id, dnac_jwt_token):
    """
    This function will delete the device with the {device_id} from the DNA Center inventory
    :param device_id: DNA C device_id
    :param dnac_jwt_token: DNA C token
    :return: delete status
    """
    url = DNAC_URL + '/dna/intent/api/v1/network-device/' + device_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.delete(url, headers=header, verify=False)
    delete_response = response.json()
    delete_status = delete_response['response']
    return delete_status


def get_project_id(project_name, dnac_jwt_token):
    """
    This function will retrieve the CLI templates project id for the project with the name {project_name}
    :param project_name: CLI project template
    :param dnac_jwt_token: DNA token
    :return: project id
    """
    url = DNAC_URL + '/api/v1/template-programmer/project?name=' + project_name
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    proj_json = response.json()
    proj_id = proj_json[0]['id']
    return proj_id


def get_project_info(project_name, dnac_jwt_token):
    """
    This function will retrieve all templates associated with the project with the name {project_name}
    :param project_name: project name
    :param dnac_jwt_token: DNA C token
    :return: list of all templates, including names and ids
    """
    url = DNAC_URL + '/api/v1/template-programmer/project?name=' + project_name
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    project_json = response.json()
    template_list = project_json[0]['templates']
    return template_list


def create_commit_template(template_name, project_name, cli_template, dnac_jwt_token):
    """
    This function will create and commit a CLI template, under the project with the name {project_name}, with the the text content
    {cli_template}
    :param template_name: CLI template name
    :param project_name: Project name
    :param cli_template: CLI template text content
    :param dnac_jwt_token: DNA C token
    :return:
    """
    project_id = get_project_id(project_name, dnac_jwt_token)

    # prepare the template param to sent to DNA C
    payload = {
            "name": template_name,
            "description": "Remote router configuration",
            "tags": [],
            "author": "admin",
            "deviceTypes": [
                {
                    "productFamily": "Routers"
                },
                {
                    "productFamily": "Switches and Hubs"
                }
            ],
            "softwareType": "IOS-XE",
            "softwareVariant": "XE",
            "softwareVersion": "",
            "templateContent": cli_template,
            "rollbackTemplateContent": "",
            "templateParams": [],
            "rollbackTemplateParams": [],
            "parentTemplateId": project_id
        }

    # check and delete older versions of the template
    # template_id = get_template_id(template_name, project_name, dnac_jwt_token)
    # if template_id:
    #    delete_template(template_name, project_name, dnac_jwt_token)

    # create the new template
    url = DNAC_URL + '/api/v1/template-programmer/project/' + project_id + '/template'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)

    # get the template id
    template_id = get_template_id(template_name, project_name, dnac_jwt_token)

    # commit template
    commit_template(template_id, 'committed by Python script', dnac_jwt_token)


def commit_template(template_id, comments, dnac_jwt_token):
    """
    This function will commit the template with the template id {template_id}
    :param template_id: template id
    :param comments: text with comments
    :param dnac_jwt_token: DNA C token
    :return:
    """
    url = DNAC_URL + '/api/v1/template-programmer/template/version'
    payload = {
            "templateId": template_id,
            "comments": comments
        }
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)


def update_commit_template(template_name, project_name, cli_template, dnac_jwt_token):
    """
    This function will update an existing template
    :param template_name: template name
    :param project_name: project name
    :param cli_template: CLI template text content
    :param dnac_jwt_token: DNA C token
    :return:
    """
    # get the project id
    project_id = get_project_id(project_name, dnac_jwt_token)

    # get the template id
    template_id = get_template_id(template_name, project_name, dnac_jwt_token)
    url = DNAC_URL + '/api/v1/template-programmer/template'

    # prepare the template param to sent to DNA C
    payload = {
        "name": template_name,
        "description": "Remote router configuration",
        "tags": [],
        "id": template_id,
        "author": "admin",
        "deviceTypes": [
            {
                "productFamily": "Routers"
            },
            {
                "productFamily": "Switches and Hubs"
            }
        ],
        "softwareType": "IOS-XE",
        "softwareVariant": "XE",
        "softwareVersion": "",
        "templateContent": cli_template,
        "rollbackTemplateContent": "",
        "templateParams": [],
        "rollbackTemplateParams": [],
        "parentTemplateId": project_id
    }
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.put(url, data=json.dumps(payload), headers=header, verify=False)

    # commit template
    commit_template(template_id, 'committed by Python script', dnac_jwt_token)


def upload_template(template_name, project_name, cli_template, dnac_jwt_token):
    """
    This function will create and deploy a new template if not existing, or will update an existing template.
    :param template_name: template name
    :param project_name: project name
    :param cli_template: CLI template text content
    :param dnac_jwt_token: DNA C token
    :return:
    """
    template_id = get_template_id(template_name, project_name, dnac_jwt_token)
    if template_id:
        update_commit_template(template_name, project_name, cli_template, dnac_jwt_token)
    else:
        create_commit_template(template_name, project_name, cli_template, dnac_jwt_token)


def delete_template(template_name, project_name, dnac_jwt_token):
    """
    This function will delete the template with the name {template_name}
    :param template_name: template name
    :param project_name: Project name
    :param dnac_jwt_token: DNA C token
    :return:
    """
    template_id = get_template_id(template_name, project_name, dnac_jwt_token)
    url = DNAC_URL + '/api/v1/template-programmer/template/' + template_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.delete(url, headers=header, verify=False)


def get_all_template_info(dnac_jwt_token):
    """
    This function will return the info for all CLI templates existing on DNA C, including all their versions
    :param dnac_jwt_token: DNA C token
    :return: all info for all templates
    """
    url = DNAC_URL + '/api/v1/template-programmer/template'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    all_template_list = response.json()
    return all_template_list


def get_template_name_info(template_name, project_name, dnac_jwt_token):
    """
    This function will return the info for the CLI template with the name {template_name}
    :param template_name: template name
    :param project_name: Project name
    :param dnac_jwt_token: DNA C token
    :return: all info for all templates
    """
    template_id = get_template_id(template_name, project_name, dnac_jwt_token)
    url = DNAC_URL + '/api/v1/template-programmer/template/' + template_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    template_json = response.json()
    return template_json


def get_template_id(template_name, project_name, dnac_jwt_token):
    """
    This function will return the latest version template id for the DNA C template with the name {template_name},
    part of the project with the name {project_name}
    :param template_name: name of the template
    :param project_name: Project name
    :param dnac_jwt_token: DNA C token
    :return: DNA C template id
    """
    template_list = get_project_info(project_name, dnac_jwt_token)
    template_id = None
    for template in template_list:
        if template['name'] == template_name:
            template_id = template['id']
    return template_id


def get_template_id_version(template_name, project_name, dnac_jwt_token):
    """
    This function will return the latest version template id for the DNA C template with the name {template_name},
    part of the project with the name {project_name}
    :param template_name: name of the template
    :param project_name: Project name
    :param dnac_jwt_token: DNA C token
    :return: DNA C template id for the last version
    """
    template_id_ver = ''
    project_id = get_project_id(project_name, dnac_jwt_token)
    url = DNAC_URL + '/api/v1/template-programmer/template?projectId=' + project_id + '&includeHead=false'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    project_json = response.json()
    for template in project_json:
        if template['name'] == template_name:
            version = 0
            versions_info = template['versionsInfo']
            for ver in versions_info:
                if int(ver['version']) > version:
                    template_id_ver = ver['id']
                    version = int(ver['version'])
    return template_id_ver


def deploy_template(template_name, project_name, device_name, dnac_jwt_token):
    """
    This function will deploy the template with the name {template_name} to the network device with the name
    {device_name}
    :param template_name: template name
    :param project_name: project name
    :param device_name: device hostname
    :param dnac_jwt_token: DNA C token
    :return: the deployment task id
    """
    device_management_ip = get_device_management_ip(device_name, dnac_jwt_token)
    template_id = get_template_id_version(template_name, project_name, dnac_jwt_token)
    payload = {
            "templateId": template_id,
            "targetInfo": [
                {
                    "id": device_management_ip,
                    "type": "MANAGED_DEVICE_IP",
                    "params": {}
                }
            ]
        }
    url = DNAC_URL + '/api/v1/template-programmer/template/deploy'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.post(url, headers=header, data=json.dumps(payload), verify=False)
    depl_task_id = (response.json())["deploymentId"].split(' ')[-1]
    return depl_task_id


def check_template_deployment_status_backup(depl_task_id, dnac_jwt_token):
    """
    This function will check the result for the deployment of the CLI template with the id {depl_task_id}
    :param depl_task_id: template deployment id
    :param dnac_jwt_token: DNA C token
    :return: status - {SUCCESS} or {FAILURE}
    """
    url = DNAC_URL + '/api/v1/template-programmer/template/deploy/status/' + depl_task_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    response_json = response.json()
    deployment_status = response_json["status"]
    return deployment_status


def get_device_id_name(device_name, dnac_jwt_token):
    """
    This function will find the DNA C device id for the device with the name {device_name}
    :param device_name: device hostname
    :param dnac_jwt_token: DNA C token
    :return:
    """
    device_id = None
    #device_list = get_all_device_info(dnac_jwt_token)
    device_list = get_all_device_list(500, dnac_jwt_token)
    for device in device_list:
        if device['hostname'] == device_name:
            device_id = device['id']
    return device_id


def get_device_status(device_name, dnac_jwt_token):
    """
    This function will return the reachability status for the network device with the name {device_name}
    :param device_name: device name
    :param dnac_jwt_token: DNA C token
    :return: status - {UNKNOWN} to locate a device in the database,
                      {SUCCESS} device reachable
                      {FAILURE} device not reachable
    """
    device_id = get_device_id_name(device_name, dnac_jwt_token)
    if device_id is None:
        return 'UNKNOWN'
    else:
        device_info = get_device_info(device_id, dnac_jwt_token)
        if device_info['reachabilityStatus'] == 'Reachable':
            return 'SUCCESS'
        else:
            return 'FAILURE'


def get_device_management_ip(device_name, dnac_jwt_token):
    """
    This function will find out the management IP address for the device with the name {device_name}
    :param device_name: device name
    :param dnac_jwt_token: DNA C token
    :return: the management ip address
    """
    device_ip = None
    device_list = get_all_device_info(dnac_jwt_token)
    for device in device_list:
        if device['hostname'] == device_name:
            device_ip = device['managementIpAddress']
    return device_ip


def get_device_id_sn(device_sn, dnac_jwt_token):
    """
    The function will return the DNA C device id for the device with serial number {device_sn}
    :param device_sn: network device SN
    :param dnac_jwt_token: DNA C token
    :return: DNA C device id
    """
    url = DNAC_URL + '/api/v1/network-device/serial-number/' + device_sn
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    device_response = requests.get(url, headers=header, verify=False)
    device_info = device_response.json()
    device_id = device_info['response']['id']
    return device_id


def get_device_location(device_name, dnac_jwt_token):
    """
    This function will find the location for the device with the name {device_name}
    :param device_name: device name
    :param dnac_jwt_token: DNA C token
    :return: the location
    """
    device_id = get_device_id_name(device_name, dnac_jwt_token)
    url = DNAC_URL + '/api/v1/group/member/' + device_id + '?groupType=SITE'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    device_response = requests.get(url, headers=header, verify=False)
    device_info = (device_response.json())['response']
    device_location = device_info[0]['groupNameHierarchy']
    return device_location


def create_site(site_name, dnac_jwt_token):
    """
    The function will create a new site with the name {site_name}
    :param site_name: DNA C site name
    :param dnac_jwt_token: DNA C token
    :return: none
    """
    payload = {
        "additionalInfo": [
            {
                "nameSpace": "Location",
                "attributes": {
                    "type": "area"
                }
            }
        ],
        "groupNameHierarchy": "Global/" + site_name,
        "groupTypeList": [
            "SITE"
        ],
        "systemGroup": False,
        "parentId": "",
        "name": site_name,
        "id": ""
    }
    url = DNAC_URL + '/api/v1/group'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    requests.post(url, data=json.dumps(payload), headers=header, verify=False)

def create_building(site_name, building_name, address, dnac_jwt_token):
    """
    The function will create a new building with the name {building_name}, part of the site with the name {site_name}
    :param site_name: DNA C site name
    :param building_name: DNA C building name
    :param address: building address
    :param dnac_jwt_token: DNA C token
    :return: none
    """
    # get the site id for the site name
    site_id = get_site_id(site_name, dnac_jwt_token)

    # get the geolocation info for address
    geo_info = get_geo_info(address, GOOGLE_API_KEY)
    print('\nGeolocation info for the address ', address, ' is:')
    pprint(geo_info)

    payload = {
        "additionalInfo": [
            {
                "nameSpace": "Location",
                "attributes": {
                    "country": "United States",
                    "address": address,
                    "latitude": geo_info['lat'],
                    "type": "building",
                    "longitude": geo_info['lng']
                }
            }
        ],
        "groupNameHierarchy": "Global/" + site_name + '/' + building_name,
        "groupTypeList": [
            "SITE"
        ],
        "systemGroup": False,
        "parentId": site_id,
        "name": building_name,
        "id": ""
    }
    url = DNAC_URL + '/api/v1/group'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    requests.post(url, data=json.dumps(payload), headers=header, verify=False)


def get_building_id(building_name, dnac_jwt_token):
    """
    The function will get the DNA C building id for the building with the name {building_name}
    :param building_name: building name
    :param dnac_jwt_token: DNA C token
    :return: DNA C building id
    """
    building_id = None
    url = DNAC_URL + '/api/v1/group?groupType=SITE'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    building_response = requests.get(url, headers=header, verify=False)
    building_json = building_response.json()
    building_list = building_json['response']
    for building in building_list:
        if building_name == building['name']:
            building_id = building['id']
    return building_id


def create_floor(building_name, floor_name, floor_number, dnac_jwt_token):
    """
    The function will  create a floor in the building with the name {site_name}
    :param building_name: DNA C site name
    :param floor_name: floor name
    :param floor_number: floor number
    :param dnac_jwt_token: DNA C token
    :return: none
    """
    # get the site id
    building_id = get_building_id(building_name, dnac_jwt_token)

    payload = {
        "additionalInfo": [
            {
                "nameSpace": "Location",
                "attributes": {
                    "type": "floor"
                }
            },
            {
                "nameSpace": "mapGeometry",
                "attributes": {
                    "offsetX": "0.0",
                    "offsetY": "0.0",
                    "width": "200.0",
                    "length": "100.0",
                    "geometryType": "DUMMYTYPE",
                    "height": "20.0"
                }
            },
            {
                "nameSpace": "mapsSummary",
                "attributes": {
                    "floorIndex": floor_number
                }
            }
        ],
        "groupNameHierarchy": "",
        "groupTypeList": [
            "SITE"
        ],
        "name": floor_name,
        "parentId": building_id,
        "systemGroup": False,
        "id": ""
    }
    url = DNAC_URL + '/api/v1/group'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    requests.post(url, data=json.dumps(payload), headers=header, verify=False)


def get_floor_id(building_name, floor_name, dnac_jwt_token):
    """
    This function will return the floor id for the floor with the name {floor_name} located in the building with the
    name {building_name}
    :param building_name: building name
    :param floor_name: floor name
    :param dnac_jwt_token: DNA C token
    :return: floor_id
    """
    floor_id = None
    building_id = get_building_id(building_name, dnac_jwt_token)
    url = DNAC_URL + '/api/v1/group/' + str(building_id) + '/child?level=1'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    building_response = requests.get(url, headers=header, verify=False)
    building_json = building_response.json()
    floor_list = building_json['response']
    return floor_list
    '''
    for floor in floor_list:
        if floor['name'] == floor_name:
            floor_id = floor['id']
    return floor_id
    '''

def assign_device_sn_building(device_sn, building_name, dnac_jwt_token):
    """
    This function will assign a device with the specified SN to a building with the name {building_name}
    :param device_sn: network device SN
    :param building_name: DNA C building name
    :param dnac_jwt_token: DNA C token
    :return:
    """
    # get the building and device id's
    building_id = get_building_id(building_name, dnac_jwt_token)
    device_id = get_device_id_sn(device_sn, dnac_jwt_token)

    url = DNAC_URL + '/api/v1/group/' + building_id + '/member'
    payload = {"networkdevice": [device_id]}
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    print('\nDevice with the SN: ', device_sn, 'assigned to building: ', building_name)


def assign_device_name_building(device_name, building_name, dnac_jwt_token):
    """
    This function will assign a device with the specified name to a building with the name {building_name}
    :param device_name: network device name
    :param building_name: DNA C building name
    :param dnac_jwt_token: DNA C token
    :return:
    """
    # get the building and device id's
    building_id = get_building_id(building_name, dnac_jwt_token)
    device_id = get_device_id_name(device_name, dnac_jwt_token)

    url = DNAC_URL + '/api/v1/group/' + building_id + '/member'
    payload = {"networkdevice": [device_id]}
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    print('\nDevice with the name: ', device_name, 'assigned to building: ', building_name)


def get_geo_info(address, google_key):
    """
    The function will access Google Geolocation API to find the longitude/latitude for a address
    :param address: address, including ZIP and Country
    :param google_key: Google API Key
    :return: longitude/latitude
    """
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + address + '&key=' + google_key
    header = {'content-type': 'application/json'}
    response = requests.get(url, headers=header, verify=False)
    response_json = response.json()
    location_info = response_json['results'][0]['geometry']['location']
    return location_info


def sync_device(device_name, dnac_jwt_token):
    """
    This function will sync the device configuration from the device with the name {device_name}
    :param device_name: device hostname
    :param dnac_jwt_token: DNA C token
    :return: the response status code, 202 if sync initiated, and the task id
    """
    device_id = get_device_id_name(device_name, dnac_jwt_token)
    param = [device_id]
    url = DNAC_URL + '/api/v1/network-device/sync?forceSync=true'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    sync_response = requests.put(url, data=json.dumps(param), headers=header, verify=False)
    task = sync_response.json()['response']['taskId']
    return sync_response.status_code, task


def check_task_id_status(task_id, dnac_jwt_token):
    """
    This function will check the status of the task with the id {task_id}
    :param task_id: task id
    :param dnac_jwt_token: DNA C token
    :return: status - {SUCCESS} or {FAILURE}
    """
    url = DNAC_URL + '/api/v1/task/' + task_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    task_response = requests.get(url, headers=header, verify=False)
    task_json = task_response.json()
    task_status = task_json['response']['isError']
    if not task_status:
        task_result = 'SUCCESS'
    else:
        task_result = 'FAILURE'
    return task_result


def check_task_id_output(task_id, dnac_jwt_token):
    """
    This function will check the status of the task with the id {task_id}. Loop one seconds increments until task is completed
    :param task_id: task id
    :param dnac_jwt_token: DNA C token
    :return: status - {SUCCESS} or {FAILURE}
    """
    url = DNAC_URL + '/api/v1/task/' + task_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    completed = 'no'
    while completed == 'no':
        try:
            task_response = requests.get(url, headers=header, verify=False)
            task_json = task_response.json()
            task_output = task_json['response']
            completed = 'yes'
        except:
            time.sleep(3)
    return task_output

'''
def create_path_trace(src_ip, dest_ip, dnac_jwt_token):
    """
    This function will create a new Path Trace between the source IP address {src_ip} and the
    destination IP address {dest_ip}
    :param src_ip: Source IP address
    :param dest_ip: Destination IP address
    :param dnac_jwt_token: DNA C token
    :return: DNA C path visualisation id
    """

    param = {
        'destIP': dest_ip,
        'periodicRefresh': False,
        'sourceIP': src_ip
    }

    url = DNAC_URL + '/api/v1/flow-analysis'
    header = {'accept': 'application/json', 'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    path_response = requests.post(url, data=json.dumps(param), headers=header, verify=False)
    path_json = path_response.json()
    path_id = path_json['response']['flowAnalysisId']
    return path_id

def create_path_trace(src_ip, src_port, dest_ip, dest_port, protocol, dnac_jwt_token):
    """
    This function will create a new Path Trace between the source IP address {src_ip} and the
    destination IP address {dest_ip}.
    The
    :param src_ip: Source IP address
    :param src_port: Source port, range (1-65535) or 'None'
    :param dest_ip: Destination IP address
    :param dest_port: Destination port, range (1-65535) or 'None'
    :param protocol: IP Protocol, range (1-254) or 'None'
    :param dnac_jwt_token: Cisco DNA Center token
    :return: Cisco DNA Center path visualisation id
    """

    param = {
        'destIP': dest_ip,
        'sourceIP': src_ip,
        'periodicRefresh': False,
        'inclusions': [
            'INTERFACE-STATS',
            'DEVICE-STATS',
            'ACL-TRACE',
            'QOS-STATS'
        ]
    }
    if src_port is not '':
        param.update({'sourcePort': src_port})
    if dest_port is not '':
        param.update({'destPort': dest_port})
    if protocol is not '':
        param.update({'protocol': protocol})

    # print the path trace details
    print('\nInitiated Path Trace with these parameters:')
    pprint(param)
    url = DNAC_URL + '/dna/intent/api/v1/flow-analysis'
    header = {'accept': 'application/json', 'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    path_response = requests.post(url, data=json.dumps(param), headers=header, verify=False)
    path_json = path_response.json()
    path_id = path_json['response']['flowAnalysisId']
    return path_id


def get_path_trace_info(path_id, dnac_jwt_token):
    """
    This function will return the path trace details for the path visualisation {id}
    :param path_id: DNA C path visualisation id
    :param dnac_jwt_token: DNA C token
    :return: Path visualisation status, and the details in a list [device,interface_out,interface_in,device...]
    """

    url = DNAC_URL + '/api/v1/flow-analysis/' + path_id
    header = {'accept': 'application/json', 'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    path_response = requests.get(url, headers=header, verify=False)
    path_json = path_response.json()
    path_info = path_json['response']
    path_status = path_info['request']['status']
    path_list = []
    if path_status == 'COMPLETED':
        network_info = path_info['networkElementsInfo']
        path_list.append(path_info['request']['sourceIP'])
        for elem in network_info:
            try:
                path_list.append(elem['ingressInterface']['physicalInterface']['name'])
            except:
                pass
            try:
                path_list.append(elem['name'])
            except:
                pass
            try:
                path_list.append(elem['egressInterface']['physicalInterface']['name'])
            except:
                pass
        path_list.append(path_info['request']['destIP'])
    return path_status, path_list


def get_path_trace_info(path_id, dnac_jwt_token):
    """
    This function will return the path trace details for the path visualisation {id}
    :param path_id: Cisco DNA Center path visualisation id
    :param dnac_jwt_token: Cisco DNA Center token
    :return: Path visualisation status, and the details in a list [device,interface_out,interface_in,device...]
    """
    # check every 10 seconds to see if path trace completed
    path_status = 'INPROGRESS'
    while path_status == 'INPROGRESS':

        # wait 2 seconds for the path trace to be completed
        time.sleep(2)

        url = DNAC_URL + '/dna/intent/api/v1/flow-analysis/' + path_id
        header = {'accept': 'application/json', 'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        path_response = requests.get(url, headers=header, verify=False)
        path_json = path_response.json()
        path_info = path_json['response']
        path_status = path_info['request']['status']

    path_list = []
    if path_status == 'COMPLETED':
        # print the complete Path Trace output
        print('\n\nThe complete path trace info is: \n')
        pprint(path_info)
        network_info = path_info['networkElementsInfo']
        path_list.append(path_info['request']['sourceIP'])
        for elem in network_info:
            try:
                path_list.append(elem['ingressInterface']['physicalInterface']['name'])
            except:
                pass
            try:
                path_list.append(elem['name'])
            except:
                pass
            try:
                path_list.append(elem['egressInterface']['physicalInterface']['name'])
            except:
                pass
        path_list.append(path_info['request']['destIP'])
        return path_status, path_list
    else:
        if path_status == 'FAILED':
            path_error = [path_info['request']['failureReason']]
            return path_status, path_error
        else:
            return 'Something went wrong', ''


'''

def check_ipv4_network_interface(ip_address, dnac_jwt_token):
    """
    This function will check if the provided IPv4 address is configured on any network interfaces
    :param ip_address: IPv4 address
    :param dnac_jwt_token: Cisco DNA Center token
    :return: None, or device_hostname and interface_name
    """
    url = DNAC_URL + '/dna/intent/api/v1/interface/ip-address/' + ip_address
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    response_json = response.json()
    response_status = response_json['response']

    # if response_status is a dict, it will include an error code. This means the IPv4 address is not assigned
    # to any managed network devices. We will check the PnP inventory next.
    # if the response_status is a list, it will include the info for the device with the interface
    # configured with the specified IPv4 address

    if type(response_status) is dict:
        pnp_device_list = pnp_get_device_list(dnac_jwt_token)
        for pnp_device in pnp_device_list:
            if pnp_device['deviceInfo']['httpHeaders'][0]['value'] == ip_address:
                device_hostname = pnp_device['deviceInfo']['hostname']
                return 'Found', device_hostname, ''
        return response_status['errorCode'], '', ''
    else:
        # noinspection PyBroadException
        try:
            response_info = response_json['response'][0]
            interface_name = response_info['portName']
            device_id = response_info['deviceId']
            device_info = get_device_info(device_id, dnac_jwt_token)
            device_hostname = device_info['hostname']
            return 'Found', device_hostname, interface_name
        except:
            device_info = get_device_info_ip(ip_address, dnac_jwt_token)  # required for AP's
            device_hostname = device_info['hostname']
            return 'Found', device_hostname, ''


def get_device_info_ip(ip_address, dnac_jwt_token):
    """
    This function will retrieve the device information for the device with the management IPv4 address {ip_address}
    :param ip_address: device management ip address
    :param dnac_jwt_token: DNA C token
    :return: device information, or None
    """
    url = DNAC_URL + '/api/v1/network-device/ip-address/' + ip_address
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    response_json = response.json()
    device_info = response_json['response']
    if 'errorCode' == 'Not found':
        return None
    else:
        return device_info


def get_legit_cli_command_runner(dnac_jwt_token):
    """
    This function will get all the legit CLI commands supported by the {command runner} APIs
    :param dnac_jwt_token: DNA C token
    :return: list of CLI commands
    """
    url = DNAC_URL + '/api/v1/network-device-poller/cli/legit-reads'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    response_json = response.json()
    cli_list = response_json['response']
    return cli_list


def get_content_file_id(file_id, dnac_jwt_token):
    """
    This function will download a file specified by the {file_id}
    :param file_id: file id
    :param dnac_jwt_token: DNA C token
    :return: file
    """
    url = DNAC_URL + '/api/v1/file/' + file_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False, stream=True)
    response_json = response.json()
    return response_json


def get_output_command_runner(command, device_name, dnac_jwt_token):
    """
    This function will return the output of the CLI command specified in the {command}, sent to the device with the
    hostname {device}
    :param command: CLI command
    :param device_name: device hostname
    :param dnac_jwt_token: DNA C token
    :return: file with the command output
    """

    # get the DNA C device id
    device_id = get_device_id_name(device_name, dnac_jwt_token)

    # get the DNA C task id that will process the CLI command runner
    payload = {
        "commands": [command],
        "deviceUuids": [device_id],
        "timeout": 0
        }
    url = DNAC_URL + '/api/v1/network-device-poller/cli/read-request'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.post(url, data=json.dumps(payload), headers=header, verify=False)
    response_json = response.json()
    print(response_json)
    task_id = response_json['response']['taskId']

    # get task id status
    time.sleep(10)  # wait for 3 seconds to receive the file name
    task_result = check_task_id_output(task_id, dnac_jwt_token)
    file_info = json.loads(task_result['progress'])
    file_id = file_info['fileId']

    # get output from file
    time.sleep(10)  # wait for 3 seconds for the file to be ready
    file_output = get_content_file_id(file_id, dnac_jwt_token)
    command_responses = file_output[0]['commandResponses']
    if command_responses['SUCCESS'] is not {}:
        command_output = command_responses['SUCCESS'][command]
    elif command_responses['FAILURE'] is not {}:
        command_output = command_responses['FAILURE'][command]
    else:
        command_output = command_responses['BLACKLISTED'][command]
    return command_output


def get_all_configs(dnac_jwt_token):
    """
    This function will retrieve all the devices configurations
    :param dnac_jwt_token: DNA C token
    :return: Return all config files in a list
    """
    url = DNAC_URL + '/api/v1/network-device/config'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    config_json = response.json()
    config_files = config_json['response']
    return config_files


def check_ipv4_address(ipv4_address, dnac_jwt_token):
    """
    This function will find if the IPv4 address is configured on any network interfaces or used by any hosts.
    :param ipv4_address: IPv4 address
    :param dnac_jwt_token: DNA C token
    :return: True/False
    """
    # check against network devices interfaces
    try:
        device_info = check_ipv4_network_interface(ipv4_address, dnac_jwt_token)
        return True
    except:
        # check against any hosts
        try:
            client_info = get_client_info(ipv4_address, dnac_jwt_token)
            if client_info is not None:
                return True
        except:
            pass
    return False


def check_ipv4_address_configs(ipv4_address, dnac_jwt_token):
    """
    This function will verify if the IPv4 address is present in any of the configurations of any devices
    :param ipv4_address: IPv4 address
    :param dnac_jwt_token: DNA C token
    :return: True/False
    """
    url = DNAC_URL + '/api/v1/network-device/config'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    config_json = response.json()
    config_files = config_json['response']
    for config in config_files:
        run_config = config['runningConfig']
        if ipv4_address in run_config:
            return True
    return False


def check_ipv4_duplicate(config_file):
    """
    This function will:
      - load a file with a configuration to be deployed to a network device
      - identify the IPv4 addresses that will be configured on interfaces
      - search in the DNA Center database if these IPV4 addresses are configured on any interfaces
      - find if any clients are using the IPv4 addresses
      - Determine if deploying the configuration file will create an IP duplicate
    :param config_file: configuration file name
    :return True/False
    """

    # open file with the template
    cli_file = open(config_file, 'r')

    # read the file
    cli_config = cli_file.read()

    ipv4_address_list = utils.identify_ipv4_address(cli_config)

    # get the DNA Center Auth token

    dnac_token = get_dnac_jwt_token(DNAC_AUTH)

    # check each address against network devices and clients database
    # initialize duplicate_ip

    duplicate_ip = False
    for ipv4_address in ipv4_address_list:

        # check against network devices interfaces

        try:
            device_info = check_ipv4_network_interface(ipv4_address, dnac_token)
            duplicate_ip = True
        except:
            pass

        # check against any hosts

        try:
            client_info = get_client_info(ipv4_address, dnac_token)
            if client_info is not None:
                duplicate_ip = True
        except:
            pass

    if duplicate_ip:
        return True
    else:
        return False


def pnp_get_device_count(device_state, dnac_jwt_token):
    """
    This function will return the count of the PnP devices in the state {state}
    :param device_state: device state, example 'Unclaimed'
    :param dnac_jwt_token: DNA C token
    :return: device count
    """
    url = DNAC_URL + '/dna/intent/api/v1/onboarding/pnp-device/count'
    payload = {'state': device_state}
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, data=json.dumps(payload), verify=False)
    pnp_device_count = response.json()
    return pnp_device_count['response']


def pnp_get_device_list(dnac_jwt_token):
    """
    This function will retrieve the PnP device list info
    :param dnac_jwt_token: DNA C token
    :return: PnP device info
    """
    url = DNAC_URL + '/dna/intent/api/v1/onboarding/pnp-device'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    pnp_device_json = response.json()
    return pnp_device_json

def pnp_get_device_list1(device_state, dnac_jwt_token):
    """
    This function will retrieve the PnP device list info
    :param dnac_jwt_token: DNA C token
    :return: PnP device info
    """
    url = DNAC_URL + '/dna/intent/api/v1/onboarding/pnp-device'
    payload = {'state': device_state}
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    pnp_device_json = response.json()
    return pnp_device_json

def pnp_claim_ap_site(device_id, floor_id, rf_profile, dnac_jwt_token):
    """
    This function will delete claim the AP with the {device_id} to the floor with the {floor_id}
    :param device_id: Cisco DNA C device id
    :param floor_id: Cisco DNA C floor id
    :param rf_profile: RF profile - options - "LOW", "TYPICAL", "HIGH"
    :param dnac_jwt_token: Cisco DNA C token
    :return: claim operation status
    """
    payload = {
        "type": "AccessPoint",
        "siteId": floor_id,
        "deviceId": device_id,
        "rfProfile": rf_profile
        }
    url = DNAC_URL + '/dna/intent/api/v1/onboarding/pnp-device/site-claim'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.post(url, headers=header, data=json.dumps(payload), verify=False)
    claim_status_json = response.json()
    claim_status = claim_status_json['response']
    return claim_status


def pnp_delete_provisioned_device(device_id, dnac_jwt_token):
    """
    This function will delete the provisioned device with the {device_id} from the PnP database
    :param device_id: Cisco DNA C device id
    :param dnac_jwt_token: Cisco DNA C token
    :return: delete opearation status
    """
    url = DNAC_URL + '/dna/intent/api/v1/onboarding/pnp-device/' + device_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.delete(url, headers=header, verify=False)
    delete_status = response.json()
    return delete_status


def pnp_get_device_info(device_id, dnac_jwt_token):
    """
    This function will get the details for the a PnP device with the {device_id} from the PnP database
    :param device_id: Cisco DNA C device id
    :param dnac_jwt_token: Cisco DNA C token
    :return: device info in json format
    """
    url = DNAC_URL + '/api/v1/onboarding/pnp-device/' + device_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    device_info_json = response.json()
    device_info = device_info_json['deviceInfo']
    return device_info


def get_physical_topology(ip_address, dnac_jwt_token):
    """
    This function will retrieve the physical topology for the device/client with the {ip_address}
    :param ip_address: device/interface IP address
    :param dnac_jwt_token: Cisco DNA C token
    :return: topology info - connected device hostname and interface
    """
    url = DNAC_URL + '/api/v1/topology/physical-topology'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    topology_json = response.json()['response']
    topology_nodes = topology_json['nodes']
    topology_links = topology_json['links']

    # try to identify the physical topology
    for link in topology_links:
        try:
            if link['startPortIpv4Address'] == ip_address:
                connected_port = link['endPortName']
                connected_device_id = link['target']
                for node in topology_nodes:
                    if node['id'] == connected_device_id:
                        connected_device_hostname = node['label']
                break
        except:
            connected_port = None
            connected_device_hostname = None
    return connected_device_hostname, connected_port

### Code have been added from here 

def get_all_device_list(limit, dnac_jwt_token):
    """
    The function will return all network devices info, using the specified limit of devices/API Call
    :param limit: the number of devices to return per API call
    :param dnac_jwt_token: Cisco DNA C token
    :return: DNA C device inventory info
    """
    offset = 1
    all_devices_list = []
    all_devices_info = ['']  # assign a value, to make sure the API call will run at least once
    while all_devices_info:
        all_devices_info = ''
        url = DNAC_URL + '/api/v1/network-device?offset=' + str(offset) + '&limit=' + str(limit)
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        all_devices_response = requests.get(url, headers=header, verify=False)
        all_devices_json = all_devices_response.json()
        all_devices_info = all_devices_json['response']
        all_devices_list += all_devices_info
        offset += limit
    return all_devices_list
 
'''
def get_all_task_info(limit, dnac_jwt_token):
    """
    The function will return all network devices info
    :param dnac_jwt_token: DNA C token
    :return: DNA C device inventory info
    """
    url = DNAC_URL + '/api/v1/task?username=h421923&startTime=1609891200000&endTime=1609977600000'
    #url = DNAC_URL + '/api/v1/task?username=h421923&serviceType=NCTP'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    all_task_response = requests.get(url, headers=header, verify=False)
    all_task_info = all_task_response.json()
    return all_task_info
    #return all_task_info['response']

''' 
def get_all_task_info(limit, dnac_jwt_token):
    """
    The function will return all network devices info
    :param dnac_jwt_token: DNA C token
    :return: DNA C device inventory info
    """
    offset = 1
    all_devices_list = []
    all_devices_info = ['']  # assign a value, to make sure the API call will run at least once
    while all_devices_info:
        all_devices_info = ''
        url = DNAC_URL + '/dna/intent/api/v1/task?username=h421923&offset=' + str(offset) + '&limit=' + str(limit)
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        all_devices_response = requests.get(url, headers=header, verify=False)
        all_devices_json = all_devices_response.json()
        all_devices_info = all_devices_json['response']
        all_devices_list += all_devices_info
        offset += limit
    return all_devices_list

def get_all_log(username, dnac_jwt_token):
    """
    The function will return all network devices info
    :param dnac_jwt_token: DNA C token
    :return: DNA C device inventory info
    """
    body = ""
    url = DNAC_URL + '/api/v1/audit?auditParentId=&limit=20000&offset=0&orderBy=createdDateTime&orderByType=desc&auditRequestor=' + username
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    all_task_response = requests.get(url, headers=header,json=body, verify=False)
    all_task_info = all_task_response.json()
    all_task = all_task_info['response']
    return all_task
    #return all_task_info['response']
    
def get_assurance_poor(limit, dnac_jwt_token):
    """
    The function will return all network devices info
    :param dnac_jwt_token: DNA C token
    :return: DNA C device inventory info
    """
    offset = 1
    all_devices_list = []
    all_devices_info = ['']  # assign a value, to make sure the API call will run at least once
    while all_devices_info:
        all_devices_info = ''
        url = DNAC_URL + '/dna/intent/api/v1/device-health?health=POOR'
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        all_devices_response = requests.get(url, headers=header, verify=False)
        all_devices_json = all_devices_response.json()
        #all_devices_info = all_devices_json['response']
        #all_devices_list += all_devices_info
        offset += limit
    return all_devices_json
    
def get_device_assurance(limit, dnac_jwt_token):
    """
    The function will return all network devices info
    :param dnac_jwt_token: DNA C token
    :return: DNA C device inventory info
    """
    offset = 1
    all_devices_list = []
    all_devices_info = ['']  # assign a value, to make sure the API call will run at least once
    while all_devices_info:
        all_devices_info = ''
        url = DNAC_URL + '/dna/intent/api/v1/device-health'
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        all_devices_response = requests.get(url, headers=header, verify=False)
        all_devices_json = all_devices_response.json()
        #all_devices_info = all_devices_json['response']
        #all_devices_list += all_devices_info
        offset += limit
    return all_devices_json
   
  
def get_assurance_fair(limit, dnac_jwt_token):
    """
    The function will return all network devices info
    :param dnac_jwt_token: DNA C token
    :return: DNA C device inventory info
    """
    offset = 1
    all_devices_list = []
    all_devices_info = ['']  # assign a value, to make sure the API call will run at least once
    while all_devices_info:
        all_devices_info = ''
        url = DNAC_URL + '/dna/intent/api/v1/device-health?health=FAIR'
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        all_devices_response = requests.get(url, headers=header, verify=False)
        all_devices_json = all_devices_response.json()
        #all_devices_info = all_devices_json['response']
        #all_devices_list += all_devices_info
        offset += limit
    return all_devices_json

def get_clinet_health(limit, dnac_jwt_token):
    """
    The function will return all network devices info
    :param dnac_jwt_token: DNA C token
    :return: DNA C device inventory info
    """
    offset = 1
    all_devices_list = []
    all_devices_info = ['']  # assign a value, to make sure the API call will run at least once
    while all_devices_info:
        all_devices_info = ''
        url = DNAC_URL + '/dna/intent/api/v1/device-health?health=POOR'
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        all_devices_response = requests.get(url, headers=header, verify=False)
        all_devices_json = all_devices_response.json()
        #all_devices_info = all_devices_json['response']
        #all_devices_list += all_devices_info
        offset += limit
    return all_devices_json

 ### Client level troubleshooting from here :

def get_client_info(client_ip, dnac_jwt_token):
    """
    This function will retrieve all the information from the client with the IP address
    :param client_ip: client IPv4 address
    :param dnac_jwt_token: DNA C token
    :return: client info, or {None} if client does not found
    """
    url = DNAC_URL + '/api/v1/host?hostIp=' + client_ip
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    #client_json = response.json()
    #client_info = client_json['detail'][0]
    return response
    


def locate_client_ip(client_ip, dnac_jwt_token):
    """
    Locate a wired client device in the infrastructure by using the client IP address
    Call to DNA C - api/v1/host?hostIp={client_ip}
    :param client_ip: Client IP Address
    :param dnac_jwt_token: DNA C token
    :return: hostname, interface_name, vlan_id, or None, if the client does not exist
    """

    client_info = get_client_info(client_ip, dnac_jwt_token)
    if client_info is not None:
        hostname = client_info['connectedNetworkDeviceName']
        interface_name = client_info['connectedInterfaceName']
        vlan_id = client_info['vlanId']
        return hostname, interface_name, vlan_id
    else:
        return None
 
def get_client_info_by_mac(mac_address, dnac_jwt_token):
    """
    This function will retrieve all the information from the client with the IP address
    :param client_ip: client IPv4 address
    :param dnac_jwt_token: DNA C token
    :return: client info, or {None} if client does not found
    """
    url = DNAC_URL + '/api/v1/client-detail?macAddress=' + mac_address
    #client-detail?timestamp=<timestamp>&macAddress
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    client_json = response.json()
    return client_json
        

def get_all_issues_info(limit, dnac_jwt_token):
    """
    The function will return all network devices info
    :param dnac_jwt_token: DNA C token
    :return: DNA C device inventory info
    """
    offset = 1
    all_devices_list = []
    all_devices_info = ['']  # assign a value, to make sure the API call will run at least once
    while all_devices_info:
        all_devices_info = ''
        url = DNAC_URL + '/dna/intent/api/v1/issues'
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        all_devices_response = requests.get(url, headers=header, verify=False)
        all_devices_json = all_devices_response.json()
        #all_devices_info = all_devices_json['response']
        #all_devices_list += all_devices_info
        offset += limit
    return all_devices_json
       

 
def get_device_health1(device_name, dnac_jwt_token):
    """
    This function will call the device health intent API and return device management interface IPv4 address,
    serial number, family, software version, device health score, ... for the device with the name {device_name}
    :param device_name: device hostname
    :param epoch_time: epoch time including msec
    :param dnac_jwt_token: DNA C token
    :return: detailed network device information
    """
    device_id = get_device_id_name(device_name, dnac_jwt_token)
    #url = DNAC_URL + '/dna/intent/api/v1/device-detail?timestamp=' + str(epoch_time) + '&searchBy=' + device_id
    url = DNAC_URL + '/dna/intent/api/v1/device-detail?&searchBy=' + device_name + '&identifier=uuid' + str(device_id)
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    device_detail_json = response.json()
    #device_detail = device_detail_json['response']
    return device_detail_json 

def get_site_health(limit, dnac_jwt_token):
    """
    The function will return all network devices info
    :param dnac_jwt_token: DNA C token
    :return: DNA C device inventory info
    """
    offset = 1
    all_devices_list = []
    all_devices_info = ['']  # assign a value, to make sure the API call will run at least once
    while all_devices_info:
        all_devices_info = ''
        url = DNAC_URL + '/dna/intent/api/v1/site-health'
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        all_devices_response = requests.get(url, headers=header, verify=False)
        all_devices_json = all_devices_response.json()
        all_devices_info = all_devices_json['response']
        #all_devices_list += all_devices_info
        offset += limit
    return all_devices_info

def get_network_health(limit, dnac_jwt_token):
    """
    The function will return all network devices info
    :param dnac_jwt_token: DNA C token
    :return: DNA C device inventory info
    """
    offset = 1
    all_devices_list = []
    all_devices_info = ['']  # assign a value, to make sure the API call will run at least once
    while all_devices_info:
        all_devices_info = ''
        url = DNAC_URL + '/dna/intent/api/v1/network-health'
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        all_devices_response = requests.get(url, headers=header, verify=False)
        all_devices_json = all_devices_response.json()
        #all_devices_info = all_devices_json['response']
        #all_devices_list += all_devices_info
        offset += limit
    return all_devices_json  

def get_device_health(limit, dnac_jwt_token):
    """
    The function will return all network devices info
    :param dnac_jwt_token: DNA C token
    :return: DNA C device inventory info
    """
    offset = 1
    all_devices_list = []
    all_devices_info = ['']  # assign a value, to make sure the API call will run at least once
    while all_devices_info:
        all_devices_info = ''
        url = DNAC_URL + '/dna/intent/api/v1/device-health'
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        all_devices_response = requests.get(url, headers=header, verify=False)
        all_devices_json = all_devices_response.json()
        #all_devices_info = all_devices_json['response']
        #all_devices_list += all_devices_info
        offset += limit
        
def get_client_health(limit, dnac_jwt_token):
    """
    The function will return all network devices info
    :param dnac_jwt_token: DNA C token
    :return: DNA C device inventory info
    """
    offset = 1
    all_devices_list = []
    all_devices_info = ['']  # assign a value, to make sure the API call will run at least once
    while all_devices_info:
        all_devices_info = ''
        url = DNAC_URL + '/dna/intent/api/v1/client-health'
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        all_devices_response = requests.get(url, headers=header, verify=False)
        all_devices_json = all_devices_response.json()
        #all_devices_info = all_devices_json['response']
        #all_devices_list += all_devices_info
        offset += limit
    return all_devices_json   



#device_id = get_device_id_name(device_name, dnac_jwt_token)  

def get_application_health(device_id, dnac_jwt_token):
    """
    The function will return all network devices info
    :param dnac_jwt_token: DNA C token
    :return: DNA C device inventory info
    """
    url = DNAC_URL + '/dna/intent/api/v1/application_health/?deviceId=' + device_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    all_devices_response = requests.get(url, headers=header, verify=False)
    all_devices_json = all_devices_response.json()
    #all_devices_info = all_devices_json['response']
    #all_devices_list += all_devices_info
    #offset += limit
    return all_devices_json   


def get_site_count(dnac_jwt_token):
    """
    This function will return the count of the PnP devices in the state {state}
    :param device_state: device state, example 'Unclaimed'
    :param dnac_jwt_token: DNA C token
    :return: device count
    """
    url = DNAC_URL + '/dna/intent/api/v1/site/count'
    #payload = {'state': device_state}
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    pnp_device_count = response.json()
    return pnp_device_count["response"]


def get_site(limit, dnac_jwt_token):
    """
    
    """
    all_devices_info = []
    offset = 1
    limit = 500
    #device_id = get_device_id_name(device_name, dnac_jwt_token)
    total_devices = get_site_count(dnac_jwt_token)
    while offset < total_devices:
        
        url = DNAC_URL + '/dna/intent/api/v1/site?offset=' + str(offset) + '&limit=' + str(limit)
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        all_devices_response = requests.get(url, headers=header, verify=False)
        all_devices_json = all_devices_response.json()
        all_devices_info += all_devices_json
        offset += 500
    return all_devices_json

def get_device_config_archive(limit, dnac_jwt_token):
    """
    """
    all_devices_info = []
    offset = 1
    limit = 500
    #device_id = get_device_id_name(device_name, dnac_jwt_token)
    #total_devices = get_site_count(dnac_jwt_token)
    all_device_list = get_all_device_list(500, dnac_jwt_token)
    device_count = len(all_device_list)
    #device_count = 10
    while offset < device_count:
        url = DNAC_URL + '/api/v1/archive-config?offset=' + str(offset) + '&limit=' + str(limit) 
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        all_devices_response = requests.get(url, headers=header, verify=False)
        all_devices_json = all_devices_response.json()['archiveResultlist']
        all_devices_info += all_devices_json
        offset += 500
    return all_devices_info

def get_device_health(limit, dnac_jwt_token):
    """
    """
    all_device_list = get_all_device_list(500, dnac_jwt_token)
    device_count = len(all_device_list)
    offset = 1
    limit = 500
    all_devices_info = []  # assign a value, to make sure the API call will run at least once
    total_devices = device_count
    while offset < total_devices:
        #all_devices_info = ''
        url = DNAC_URL + '/dna/intent/api/v1/device-health?offset=' + str(offset) + '&limit=' + str(limit)
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        all_devices_response = requests.get(url, headers=header, verify=False)
        all_devices_json = all_devices_response.json()['response']        
        all_devices_info += all_devices_json
        offset += 500
    return all_devices_info

'''	
offset = 1
limit = 500
url_dev = url + '/dna/intent/api/v1/network-device/count'
header = {​​'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}​​
count_response = requests.get(url_dev, headers=header, verify=False)
total_devices = count_response.json()['response']
while offset < total_devices:
    url_dev = url + '/dna/intent/api/v1/network-device?offset=' + str(offset) + '&limit=' + str(limit)
    header = {​​'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}​​
    all_devices_response = requests.get(url_dev, headers=header, verify=False)
    all_devices_json = all_devices_response.json()['response']
'''



def get_site_id(site_name, dnac_jwt_token):
    """
    The function will get the DNA C site id for the site with the name {site_name}
    :param site_name: DNA C site name
    :param dnac_jwt_token: DNA C token
    :return: DNA C site id
    """
    site_id = None
    url = DNAC_URL + '/api/v1/group?groupType=SITE'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    site_response = requests.get(url, headers=header, verify=False)
    site_json = site_response.json()
    site_list = site_json['response']
    for site in site_list:
        if site_name == site['name']:
            site_id = site['id']
    return site_id
  
def get_device_name(device_ip, dnac_jwt_token):
    """
    This function will find out the management IP address for the device with the name {device_name}
    :param device_name: device name
    :param dnac_jwt_token: DNA C token
    :return: the management ip address
    """
    device_name = None
    device_list = get_all_device_info(dnac_jwt_token)
    for device in device_list:
        if device['managementIpAddress'] == device_ip:
           device_name = device['hostname']
    return device_name
  
def get_client_info_by_name(username, dnac_jwt_token):
    """
    This function will return the wireless client info for the wireless client using the username {username}
    5 API calls/minute
    :param username: client username
    :param dnac_auth: Cisco DNA Center token
    :return: wireless client info
    """
    url = DNAC_URL + '/dna/intent/api/v1/user-enrichment-details'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token, 'entity_type': 'network_user_id', 'entity_value': username}
    client_response = requests.get(url, headers=header, verify=False)
    wireless_client_json = client_response.json()
    wireless_client_info = []
    if wireless_client_json[0]['userDetails'] != {}:  # check if user details is empty. if yes, unknown users
        return wireless_client_json
    else:
        return wireless_client_info
        
def get_client_info_by_mac(mac_address, dnac_jwt_token):
    """
    This function will return the wireless client info for the wireless client using the MAC address {mac_address}
    5 API calls/minute
    :param mac_address: client MAC address
    :param dnac_auth: Cisco DNA Center token
    :return: wireless client info
    """
    url = DNAC_URL + '/dna/intent/api/v1/user-enrichment-details'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token, 'entity_type': 'mac_address',
              'entity_value': mac_address}
    client_response = requests.get(url, headers=header, verify=False)
    wireless_client_json = client_response.json()
    wireless_client_info = []
    if wireless_client_json[0]['userDetails'] != {}:  # check if user details is empty. if yes, unknown users
        return wireless_client_json
    else:
        return wireless_client_info
        
def get_client_detail(mac_address, timestamp, dnac_jwt_token):
    """
    This function will return the client_detial info for the wireless client using the MAC address {mac_address},
    at a specific timestamp in epoch msec
    100 API calls/minute
    :param mac_address: client MAC address
    :param timestamp: timestamp in epoch msec
    :param dnac_auth: Cisco DNA Center token
    :return: wireless client info
    """
    url = DNAC_URL + '/dna/intent/api/v1/client-detail?timestamp=' + str(timestamp) + '&macAddress=' + mac_address
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    client_response = requests.get(url, headers=header, verify=False)
    client_detail_json = client_response.json()
    return client_detail_json
    
def check_ipv4_network_interface1(ip_address, dnac_jwt_token):
    """
    This function will check if the provided IPv4 address is configured on any network interfaces
    :param ip_address: IPv4 address
    :param dnac_jwt_token: Cisco DNA Center token
    :return: None, or device_hostname and interface_name
    """
    url = DNAC_URL + '/dna/intent/api/v1/interface/ip-address/' + ip_address
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    response_json = response.json()
    response_status = response_json['response']

    # if response_status is a dict, it will include an error code. This means the IPv4 address is not assigned
    # to any managed network devices. We will check the PnP inventory next.
    # if the response_status is a list, it will include the info for the device with the interface
    # configured with the specified IPv4 address

    if type(response_status) is dict:
        pnp_device_list = pnp_get_device_list(dnac_jwt_token)
        for pnp_device in pnp_device_list:
            if pnp_device['deviceInfo']['httpHeaders'][0]['value'] == ip_address:
                device_hostname = pnp_device['deviceInfo']['hostname']
                return device_hostname
        return response_status['errorCode'], '', ''
    else:
        # noinspection PyBroadException
        try:
            response_info = response_json['response'][0]
            interface_name = response_info['portName']
            device_id = response_info['deviceId']
            device_info = get_device_info(device_id, dnac_jwt_token)
            device_hostname = device_info['hostname']
            return device_hostname
        except:
            device_info = get_device_info_ip(ip_address, dnac_jwt_token)  # required for AP's
            device_hostname = device_info['hostname']
            return device_hostname
            
def get_all_compliance(limit, dnac_jwt_token):
    """
    The function will return all network devices info
    :param dnac_jwt_token: DNA C token
    :return: DNA C device inventory info
    """
    offset = 1
    all_devices_list = []
    all_devices_info = ['']  # assign a value, to make sure the API call will run at least once
    while all_devices_info:
        all_devices_info = ''
        url = DNAC_URL + '/dna/intent/api/v1/compliance'
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        all_devices_response = requests.get(url, headers=header, verify=False)
        all_devices_json = all_devices_response.json()
        #all_devices_info = all_devices_json['response']
        #all_devices_list += all_devices_info
        offset += limit
    return all_devices_json
 
def get_device_config(device_name, dnac_jwt_token):
    """
    This function will get the configuration file for the device with the name {device_name}
    :param device_name: device hostname
    :param dnac_jwt_token: DNA C token
    :return: configuration file
    """
    device_id = get_device_id_name(device_name, dnac_jwt_token)
    url = DNAC_URL + '/api/v1/network-device/' + device_id + '/config'
    #url = DNAC_URL +'/api/v1/network-device/{}/config'.format(device_id)
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    config_json = response.json()
    #config_file = config_json['response']
    return config_json 
 
def send_deploy_template_no_params(template_name, project_name, device_name, dnac_jwt_token):
    """
    This function will deploy the template with the name {template_name} to the network device with the name
    {device_name}
    :param template_name: template name
    :param project_name: project name
    :param device_name: device hostname
    :param dnac_jwt_token: Cisco DNA Center token
    :return: the deployment task id
    """
    template_id = get_template_id(template_name, project_name, dnac_jwt_token)
    payload = {
            "templateId": template_id,
            "forcePushTemplate": True,
            "targetInfo": [
                {
                    "id": device_name,
                    "type": "MANAGED_DEVICE_HOSTNAME"
                }
            ]
        }
    url = DNAC_URL + '/dna/intent/api/v1/template-programmer/template/deploy'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    deployment = requests.post(url, headers=header, data=json.dumps(payload), verify=False)
    deployment_json = deployment.json()
    depl_task_id = deployment_json["deploymentId"].split(' ')[-1]
    return depl_task_id

def check_template_deployment_status(depl_task_id, dnac_jwt_token):
    """
    This function will check the result for the deployment of the CLI template with the id {depl_task_id}
    Loop until the deployment task is completed
    :param depl_task_id: template deployment id
    :param dnac_jwt_token: Cisco DNA Center token
    :return: status - {SUCCESS} or {FAILURE}
    """
    # loop until the task is completed, check status every 5 seconds
    deployment_status = 'unknown'
    count = 0
    while deployment_status == 'unknown':
        time.sleep(2)
        count += 1
        try:
            url = DNAC_URL + '/dna/intent/api/v1/template-programmer/template/deploy/status/' + depl_task_id
            header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
            deployment_response = requests.get(url, headers=header, verify=False)
            deployment_response_json = deployment_response.json()
            if deployment_response_json['endTime'] != '':
                deployment_status = deployment_response_json['status']
                return deployment_status
        except:
            pass
        if count >= 5:
            return deployment_status

def get_device_config_new(device_name, dnac_jwt_token):
    """
    This function will get the configuration file for the device with the name {device_name}
    :param device_name: device hostname
    :param dnac_jwt_token: DNA C token
    :return: configuration file
    """
    device_id = get_device_id_name(device_name, dnac_jwt_token)
    url = DNAC_URL + '/api/v1/network-device/' + device_id + '/config'
    #url = DNAC_URL +'/api/v1/network-device/{}/config'.format(device_id)
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    config_json = response.json()
    data = config_json['response']
    #data = json.dumps(config_json)
    #data1 = data[1]
    #data = config_json[0]
    #result = json.dumps(config_json)
    #data = result.response
    #config = config_json['response']
    #config = result['response']
    #config_file = config_json['response']
    return data
    

def get_device_config_backup(device_name, dnac_jwt_token):
    """
    """
    network_device_id = get_device_id_name(device_name, dnac_jwt_token)
    device_config = {}
    if network_device_id:
       #url = DNAC_URL + '/api/v1/network-device/{}/config'.format(network_device_id)
       url = DNAC_URL +'/api/v1/network-device/{}/config'.format(network_device_id)
       header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
       response = requests.get(url, headers=header, verify=False)

       if response.content:
           device_config = response.json()

    if 'response' in device_config.keys():
        return device_config['response'] # Take off outer response dictionary and return string
    else:
        return None       
 
def get_device_startupconfig_backup(device_name, dnac_jwt_token):
    """ 
    """
    network_device_id = get_device_id_name(device_name, dnac_jwt_token)
    device_config = {}
    if network_device_id:
       #url = DNAC_URL + '/api/v1/network-device/{}/config'.format(network_device_id)
       url = DNAC_URL +'/api/v1/network-device/{}/startupconfig'.format(network_device_id)
       header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
       response = requests.get(url, headers=header, verify=False)

       if response.content:
           device_config = response.json()

    if 'response' in device_config.keys():
        return device_config['response'] # Take off outer response dictionary and return string
    else:
        return None   
 
    
def get_interface_vlan_info(device_id, dnac_jwt_token):
    """
    This function will get the configuration file for the device with the name {device_name}
    :param device_name: device hostname
    :param dnac_jwt_token: DNA C token
    :return: configuration file
    """
    #device_id = get_device_id_name(device_name, dnac_jwt_token)
    url = DNAC_URL + '/api/v1/network-device/' + device_id + '/vlan'
    #url = DNAC_URL +'/api/v1/network-device/{}/config'.format(device_id)
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False) 
    config_json = response.json()
    data = config_json['response']
    return data
 
def get_site_membership(site_id ,dnac_jwt_token):
    """
    """
    all_devices_json = ''
    #device_id = get_device_id_name(device_name, dnac_jwt_token)
    url = DNAC_URL + '/api/v1/membership/&siteId=' + site_id
    #url = DNAC_URL + '/api/v1/membership/&siteId?offset=' + str(offset) + '&limit=' + str(limit) + site_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    all_devices_response = requests.get(url, headers=header, verify=False)
    all_devices_json = all_devices_response.json()['version']
    for item in all_devices_json: 
        message = ''
        message = item['message']
        print (str(message))
    
    #all_devices_info += all_devices_json
        
    return all_devices_json

def get_device_health(limit, dnac_jwt_token):
    """
    """
    all_device_list = get_all_device_list(500, dnac_jwt_token)
    device_count = len(all_device_list)
    offset = 1
    limit = 500
    all_devices_info = []  # assign a value, to make sure the API call will run at least once
    total_devices = device_count
    while offset < total_devices:
        #all_devices_info = ''
        url = DNAC_URL + '/dna/intent/api/v1/device-health?offset=' + str(offset) + '&limit=' + str(limit)
        header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
        all_devices_response = requests.get(url, headers=header, verify=False)
        all_devices_json = all_devices_response.json()['response']        
        all_devices_info += all_devices_json
        offset += 500
    return all_devices_info
 
 
def get_all_vlan(dnac_jwt_token):
    """
    This function will get the configuration file for the device with the name {device_name}
    :param device_name: device hostname
    :param dnac_jwt_token: DNA C token
    :return: configuration file
    """
    #device_id = get_device_id_name(device_name, dnac_jwt_token)
    url = DNAC_URL + '/api/v1/topology/vlan/vlan-names'
    #url = DNAC_URL +'/api/v1/network-device/{}/config'.format(device_id)
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False) 
    config_json = response.json()
    data = config_json['response']
    return data

 
def get_device_name_with_id(device_ip, dnac_jwt_token):
    """
    This function will find out the management IP address for the device with the name {device_name}
    :param device_name: device name
    :param dnac_jwt_token: DNA C token
    :return: the management ip address
    """
    device_id = None
    device_list = get_all_device_info(dnac_jwt_token)
    for device in device_list:
        if device['id'] == device_id:
           device_name = device['hostname']
    return device_name
      
    
def delete_site1(site_id, dnac_jwt_token):
    """
    This function will delete the device with the {site_id} from the DNA Center inventory
    :param device_id: DNA C site_id
    :param dnac_jwt_token: DNA C token
    :return: delete status
    """
    url = DNAC_URL + '/dna/intent/api/v1/site/' + site_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.delete(url, headers=header, verify=False)
    delete_response = response.json()
    #delete_status = delete_response['response']
    return delete_status

def delete_site(site_id, dnac_jwt_token):
    """
    This function will delete the device with the {site_id} from the DNA Center inventory
    :param device_id: DNA C site_id
    :param dnac_jwt_token: DNA C token
    :return: delete status
    """
    url = DNAC_URL + '/dna/intent/api/v1/site/' + site_id
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.delete(url, headers=header, verify=False)
    delete_response = response.json()
    print (delete_response)
    delete_status = delete_response['message']
    return delete_status

def get_users(dnac_jwt_token):
    """
    This function will get the configuration file for the device with the name {device_name}
    :param device_name: device hostname
    :param dnac_jwt_token: DNA C token
    :return: configuration file
    """
    #device_id = get_device_id_name(device_name, dnac_jwt_token)
    url = DNAC_URL + '/api/v1/user/h421923'
    #url = DNAC_URL +'/api/v1/network-device/{}/config'.format(device_id)
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False) 
    config_json = response.json()
    data = config_json['response']
    return data


def get_license_device(deviceid, dnac_jwt_token):
    """
    """

    device_info = []
    url = DNAC_URL + '/api/v1/license-info/network-device/' + deviceid
    header = {'accept': 'application/json', 'X-Auth-Token': dnac_jwt_token}
    payload = {'deviceid': deviceid}
    device_response = requests.get(url, params=payload, headers=header, verify=False)
    if device_response.status_code == 200:
        device_json = device_response.json()
        device_info = device_json['response']
        # pprint(device_info)    # use this for printing info about each device

        #for licenses in device_info:
         #   try:  # required to avoid errors due to some devices, for example Access Points,
                # that do not have an "inuse" license.
          #      if licenses.get('status') == 'INUSE':
           #         new_license = licenses.get('name')
            #        if new_license not in license_info:
             #           license_info.append(new_license)
            #except:
             #   pass
    return device_info
    
def collect_switchport_info(device_id, dnac_jwt_token):
    """
    This function will create an inventory of all switchports and relevant information for each switchport
    Call to /interface/network-device/{deviceId}
    :param device_id: DNAC switch id
    :return: list with all the relevant info for each switchport
    """

    all_switchport_info_list=[]
    url = DNAC_URL + '/api/v1/interface/network-device/' + device_id
    header = {'accept': 'application/json', 'X-Auth-Token': dnac_jwt_token}
    switch_response = requests.get(url, headers=header, verify=False)
    switch_response = switch_response.json()
    switch_info = switch_response['response']
    return switch_info
    # pprint(switch_info)
    
def get_device_config_search(device_id, keyword, dnac_jwt_token):
    
    #url = DNAC_URL + '/api/v1/network-device/{}/config'.format(network_device_id)
    url = DNAC_URL +'/api/v1/network-device/{}/config'.format(device_id)
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    if response.content:
        device_config = response.json()
    if 'response' in device_config.keys():
        device_config = device_config['response'] # Take off outer response dictionary and return string  
        print(device_config)        
        try:
            keyword = r'%s([^!]+)' % keyword
            config = re.search(keyword, device_config).group(1)
            print(config)
            return config
        except:
            print("Doesn't contain the string match")
            return False
    return False
 
def check_config(device_id, keyword, dnac_jwt_token):
    #url = DNAC_URL + '/api/v1/network-device/{}/config'.format(network_device_id)
    url = DNAC_URL +'/api/v1/network-device/{}/config'.format(device_id)
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    if response.content:
        device_config = response.json()        
    if 'response' in device_config.keys():
        device_config = device_config['response'] # Take off outer response dictionary and return string  
        print(device_config)
        if keyword in device_config:
            print("Configuration contains: ", keyword)
            return True
        else:
            print("Configuration DOES NOT contains: ", keyword)
        #return False
       
 
def get_discovery1(dnac_jwt_token):
    """
    The function will return all network devices info
    :param dnac_jwt_token: DNA C token
    :return: DNA C device inventory info
    """
    #startIndex = 1
    #recordsToReturn = 328
    url = DNAC_URL + '/api/v1/discovery/1/220'
    #url = DNAC_URL + '/api/v1/discovery/?startIndex={}&recordsToReturn={}'.format(startIndex,recordsToReturn)
    #url = DNAC_URL + '/api/v1/archive-config?offset=' + str(offset) + '&limit=' + str(limit)
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    all_device_response = requests.get(url, headers=header, verify=False)
    all_device_info = all_device_response.json()
    return all_device_info['response']    
 
def check_client_ip_address(client_ip):
    """
    The function will find out if DNAC has a client device configured with the specified IP address.
    API call to /host
    It will print if a client device exists or not.
    :param client_ip: client IP address
    :return: None
    """
    dnac_auth = get_dnac_jwt_token(DNAC_AUTH)
    
    url = DNAC_URL + '/api/v1/host'
    header = {'accept': 'application/json', 'X-Auth-Token': dnac_auth}
    payload = {'hostIp': client_ip}
    host_response = requests.get(url, params=payload, headers=header, verify=False)
    host_json = host_response.json()
    if not host_json['response']:
        print('The IP address ', client_ip, ' is not used by any client devices')
    else:
        print('The IP address ', client_ip, ' is used by a client device')


 
'''
def get_template_id_version(template_name, project_name, dnac_jwt_token):
    """
    This function will return the latest version template id for the DNA C template with the name {template_name},
    part of the project with the name {project_name}
    :param template_name: name of the template
    :param project_name: Project name
    :param dnac_jwt_token: Cisco DNA Center token
    :return: DNA C template id for the last version
    """
    project_id = get_project_id(project_name, dnac_jwt_token)
    url = DNAC_URL + '/dna/intent/api/v1/template-programmer/template?projectId=' + project_id + '&includeHead=false'
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    response = requests.get(url, headers=header, verify=False)
    project_json = response.json()
    for template in project_json:
        if template['name'] == template_name:
            version = 0
            versions_info = template['versionsInfo']
            for ver in versions_info:
                if int(ver['version']) > version:
                    template_id_ver = ver['id']
                    version = int(ver['version'])
    return template_id_ver
'''

 