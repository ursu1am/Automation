import requests
import json
import sys
import time
import logging

from env_lab import DNAC, DNAC_PORT, DNAC_USER, DNAC_PASS
from requests.auth import HTTPBasicAuth
from http.client import NOT_FOUND
from requests.exceptions import HTTPError

requests.packages.urllib3.disable_warnings()


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
TASK_DEFAULT_TIMEOUT = 60  # seconds
TASK_TREE_DEFAULT_TIMEOUT = 10  # seconds
GET_TASK_MAX_RETRIES = 6
EXPONENTIAL_BACKOFF_MULTIPLIER = 2


# -------------------------------------------------------------------
# Config Audit file Create functions - configuration commands
# -------------------------------------------------------------------



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

def get_device_uuid(ip_address):
    device_detail = get_url("api/v1/network-device?managementIpAddress=" + ip_address)
    if len(device_detail["response"])==0:
        print("Device with IP Address " + ip_address + " does not exist in DNAC")
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


def get_auth_token(controller_ip=DNAC, username=DNAC_USER, password=DNAC_PASS):
    """ Authenticates with controller and returns a token to be used in subsequent API invocations
    """

    login_url = "https://{0}:{1}/api/system/v1/auth/token".format(controller_ip, DNAC_PORT)
    result = requests.post(url=login_url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASS), verify=False)
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
    
def get_acl(device_uuid):
    show_command = "show ip access-list"
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


print ("Device IP Address " + sys.argv[1])
device_ip_address = sys.argv[1]
device_uuid = get_device_uuid(device_ip_address)
get_last_running_configuration_change(device_uuid)
get_acl(device_uuid)
get_last_startup_configuration_change(device_uuid)
get_config_mismatch(device_uuid)



