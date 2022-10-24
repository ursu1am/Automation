import requests
import json
import sys
import time
import logging
import datetime
import os
import schedule
from getpass import getpass
from env_lab import DNAC, DNAC_PORT, DNAC_USER, DNAC_PASSWORD
from requests.auth import HTTPBasicAuth
from http.client import NOT_FOUND
from requests.exceptions import HTTPError

requests.packages.urllib3.disable_warnings()
#print ('Please Enter your password to proceed ')
#DNAC_PASSWORD = getpass()

# -------------------------------------------------------------------
# Custom exception definitions
# -------------------------------------------------------------------
class TaskTimeoutError(Exception):
    pass


class TaskError(Exception):
    pass


# API ENDPOINTS
ENDPOINT_TICKET = "ticket"
ENDPOINT_TASK_SUMMARY = "task/%s"
RETRY_INTERVAL = 2
FILE_NAME = "change_audit.txt"
TASK_COMPLETION_POLL_INTERVAL = 3  # seconds
TASK_DEFAULT_TIMEOUT = 120  # seconds
TASK_TREE_DEFAULT_TIMEOUT = 10  # seconds
GET_TASK_MAX_RETRIES = 6
EXPONENTIAL_BACKOFF_MULTIPLIER = 2


# -------------------------------------------------------------------
# Config Audit file Create functions - configuration commands
# -------------------------------------------------------------------

def create_audit_file(audit_commands, device_uuid):
    payload = {
        "commands": [
            "tclsh",
            "puts [open flash:audit_config.txt w+] {",
            audit_commands,
            "}",
            "tclquit"
        ],
        "description": "Config_Audit_compliance",
        "timeout": 0,
        "deviceUuids": [
            device_uuid
        ],
        "name": "Config_Audit_compliance"
    }
    result = post_url("api/v1/network-device-poller/cli/read-request",payload)
    return result

def execute_show_command(show_command, device_uuid):
    payload = {
        "commands": [
            show_command
        ],
        "description": "Config_Audit_compliance",
        "timeout": 0,
        "deviceUuids": [
            device_uuid
        ],
        "name": "Config_Audit_compliance"
    }
    result = post_url("api/v1/network-device-poller/cli/read-request",payload)
    return result

def check_compliance(command, device_uuid):
    payload = {
        "commands": [
            command,
        ],
        "description": "Config_Audit_compliance_check",
        "timeout": 0,
        "deviceUuids": [
            device_uuid
        ],
        "name": "Config_Audit_compliance_check"
    }
    result = post_url("api/v1/network-device-poller/cli/read-request", payload)
    return result

def __wait_for_task_complete(task_id=None, timeout=None):

    if timeout is None:
        timeout = TASK_DEFAULT_TIMEOUT

    assert task_id is not None
    task_completed = False

    start_time = time.time()
    task_response = None

    while not task_completed:
        if time.time() > (start_time + timeout):
            assert False, ("Task {0} didn't complete within {1} seconds"
                           .format(task_response, timeout))
        task_response = __get_task_response(task_id)
        if __is_task_success(task_response) or __is_task_failed(task_response):
            task_completed = True
            return task_response
        else:
            time.sleep(TASK_COMPLETION_POLL_INTERVAL)
    return task_response

def get_task_by_task_id(task_id):
    return get_url("api/v1/task/" + task_id)

def __get_task_response(task_id):
    retry_interval = 1
    retries = GET_TASK_MAX_RETRIES
    for retry in range(retries):
        try:
            task_result = get_task_by_task_id(
                task_id=task_id)
            assert task_result is not None

            task_response = task_result["response"]
            assert task_response is not None

            return task_response
        except HTTPError as err:
            # changed
            error_code = err.response.status_code
            error_result = err.response._content.decode()
            if error_code == NOT_FOUND:
                if retry < retries - 1:
                    time.sleep(retry_interval)
                    retry_interval *= EXPONENTIAL_BACKOFF_MULTIPLIER
                else:
                    assert False, ("Max retries ({0}) exceeded\nHTTP error code: "
                                   "{1}\nerror result: {2}".format(retries,
                                                                   error_code,
                                                                   json.loads(error_result)))
            else:
                assert False, ("\nHTTP error code: {0}\nerror result: {1}"
                               .format(error_code, json.loads(error_result)))

def __is_task_failed(task_response):
    assert task_response is not None
    return task_response["isError"] is True

def __is_task_success(task_response):
    """
    :type error_codes: list
    """
    assert task_response is not None
    is_not_error = task_response["isError"] is None or task_response["isError"] is False
    is_end_time_present = task_response.get("endTime") is not None
    return is_not_error and is_end_time_present

def get_device_uuid(device_name):
    device_detail = get_url("api/v1/network-device?hostname=" + device_name)
    if len(device_detail["response"])==0:
        print("Device with Hostname " + device_name + " does not exist in DNAC")
        sys.exit(1)
    return device_detail["response"][0]["instanceUuid"]


# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------

def get_url(url):
    url = create_url(path=url)
    token = get_auth_token()
    headers = {'X-auth-token': token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print("Error processing request", cerror)
        sys.exit(1)

    return response.json()


def create_url(path, controller_ip=DNAC):
    """ Helper function to create a DNAC API endpoint URL
    """

    return "https://%s:%s/%s" % (controller_ip, DNAC_PORT, path)


def get_auth_token(controller_ip=DNAC, username=DNAC_USER, password=DNAC_PASSWORD):
    """ Authenticates with controller and returns a token to be used in subsequent API invocations
    """

    login_url = "https://{0}:{1}/api/system/v1/auth/token".format(controller_ip, DNAC_PORT)
    result = requests.post(url=login_url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASSWORD), verify=False)
    result.raise_for_status()

    token = result.json()["Token"]
    return {
        "controller_ip": controller_ip,
        "token": token
    }


def post_url(url, payload):
    token = get_auth_token()
    url = create_url(path=url)
    headers = {
        'x-auth-token': token['token'],
        'content-type': 'application/json',
        '__runsync': "true",
        '__timeout': "30",
        '__persistbapioutput': "true"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
    except requests.exceptions.RequestException  as cerror:
        print("Error processing request", cerror)
        sys.exit(1)

    return response.json()

def get_file_content(file_id):
    file_service_response = get_url("api/v1/file/" + file_id)
    command_response = file_service_response[0]["commandResponses"]
    return command_response;

def get_last_running_configuration_change(device_uuid):
    show_command = "show running-config | i Last configuration change"
    response = execute_show_command(show_command, device_uuid)
    task_id = response["response"]["taskId"]
    task_response = __wait_for_task_complete(task_id)
    # task_response = __get_task_response(task_id)
    file_id_result = dict(eval(task_response["progress"]))
    file_id = file_id_result["fileId"]
    file_service_response = get_file_content(file_id)
    success_response = file_service_response["SUCCESS"]
    print("\n Running Configuration Change time and user details")
    print("------------------------------------------------------")
    print_config_change_line(success_response, show_command)

def get_last_startup_configuration_change(device_uuid):
    show_command = "show startup-config | i Last configuration change"
    response = execute_show_command(show_command, device_uuid)
    task_id = response["response"]["taskId"]
    task_response = __wait_for_task_complete(task_id)
    # task_response = __get_task_response(task_id)
    file_id_result = dict(eval(task_response["progress"]))
    file_id = file_id_result["fileId"]
    file_service_response = get_file_content(file_id)
    success_response = file_service_response["SUCCESS"]
    print("\n Startup Configuration Change time and user details")
    print("------------------------------------------------------")
    print_config_change_line(success_response,show_command)
    
def get_dot1x_log(device_uuid, show_command):
    #show_command = "show ip access-list SSH-UNRESTRICTED"
    response = execute_show_command(show_command, device_uuid)
    task_id = response["response"]["taskId"]
    task_response = __wait_for_task_complete(task_id)
    # task_response = __get_task_response(task_id)
    file_id_result = dict(eval(task_response["progress"]))
    file_id = file_id_result["fileId"]
    file_service_response = get_file_content(file_id)
    success_response = file_service_response["SUCCESS"]
    if success_response is not None:
        result = dict(success_response)
        for key, value in result.items():
            lines = value.splitlines()
            return lines

           #print(lines)
            for line in lines:
                if not (line.startswith("!Contextual Config Diffs") or line.startswith(
                        "show") or "quit" in line or "#" in line):
                    words = line.split(" ")
                    if not (len(words) == 10 or len(words) == 9):
                        print(line)
      

def get_vlan_change(device_uuid):
    show_command = "show running | se vlan"
    response = execute_show_command(show_command, device_uuid)
    task_id = response["response"]["taskId"]
    task_response = __wait_for_task_complete(task_id)
    # task_response = __get_task_response(task_id)
    file_id_result = dict(eval(task_response["progress"]))
    file_id = file_id_result["fileId"]
    file_service_response = get_file_content(file_id)
    success_response = file_service_response["SUCCESS"]
    #print("\n VLAN details")
    #print("------------------------------------------------------")
    #print_config_change_line(success_response, show_command)
    return success_response
    
def get_vlan_output(device_uuid):
    show_command = "show running | se vlan"
    response = execute_show_command(show_command, device_uuid)
    task_id = response["response"]["taskId"]
    task_response = __wait_for_task_complete(task_id)
    # task_response = __get_task_response(task_id)
    file_id_result = dict(eval(task_response["progress"]))
    file_id = file_id_result["fileId"]
    file_service_response = get_file_content(file_id)
    success_response = file_service_response["SUCCESS"]
    print("\n VLAN details")
    print("------------------------------------------------------")
    print_config_change_line(success_response, show_command)
    #return success_response
    
def print_config_change_line(show_command_response, command):
    response = show_command_response[command]
    lines = response.splitlines()
    for line in lines:
        if line.startswith("!"):
            print(str(line).replace("!", ""))

        


def get_config_mismatch(device_uuid):
    show_command = "show archive config differences nvram:startup-config"
    response = execute_show_command(show_command, device_uuid)
    task_id = response["response"]["taskId"]
    task_response = __wait_for_task_complete(task_id)
    # task_response = __get_task_response(task_id)
    file_id_result = dict(eval(task_response["progress"]))
    file_id = file_id_result["fileId"]
    file_service_response = get_file_content(file_id)
    success_response = file_service_response["SUCCESS"]
    if success_response is not None:
        result = dict(success_response)
        for key, value in result.items():
            print(
                "\n  Difference between Running and startup config for the device " + device_ip_address + "\n")
            print("---------------------------------------------------------------------------------------------------")
            lines = value.splitlines(True)
            for line in lines:
                if not (line.startswith("!Contextual Config Diffs") or line.startswith(
                        "show") or "quit" in line or "#" in line):
                    words = line.split(" ")
                    if not (len(words) == 10 or len(words) == 9):
                        print(line)

# -----------------------------------------
# Main function
# -----------------------------------------
date_time = str(datetime.datetime.now().replace(microsecond=0))
print('\n\nApplication "error logs" Run Started: ' + date_time)
print('\n')

for i in range(1,500):
    with open('devices1.txt') as f:
    
        ip_list = f.read().splitlines()    
    for switch in ip_list:
     
        f = open("Errors_CPU.txt", 'a')
        date_time = str(datetime.datetime.now().replace(microsecond=0))
        f.write('\n\nApplication "error logs" Run Started: ' + date_time + '\n\n')
         
        print("Checking device " + switch + " Configuration")
        device_uuid = get_device_uuid(switch)
        device_config1 = []
        device_config2 = []
        device_config21 = []
        show_command1 = 'show interfaces TenGigabitEthernet1/1/1 | in input errors| output drops'    
        device_config1 = get_dot1x_log(device_uuid, show_command1)
        for item1 in device_config1:
            f.write(item1+ '\n')
            
        show_command2 = 'show interfaces TenGigabitEthernet1/1/1 | in input errors| output drops'   
        device_config2 = get_dot1x_log(device_uuid, show_command2) 
        for item2 in device_config2:
            f.write(item2+ '\n')    

        show_command21 = 'show processes cpu | ex 0.00'   
        device_config21 = get_dot1x_log(device_uuid, show_command21) 
        for item21 in device_config21:
            f.write(item21+ '\n')             
        f.close()

    i+=1
    time.sleep(30)    
    
print (' END of the Script Thanks  .....................................')
 
