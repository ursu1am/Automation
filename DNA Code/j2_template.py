import datetime
import time

import urllib3
from requests.auth import HTTPBasicAuth  # for Basic Auth
from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings

import dnac_apis1
from env_lab import DNAC_PASS, DNAC_USER
from env_lab import PROJECT_J2, MANAGEMENT_INT_J2, DEVICE_NAME, PARAMS

urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)


def main():
    """
    This script will load the file with the name {file_info}
    The file includes the information required to deploy the template. The network device hostname, the Cisco DNA Center
    project name, the configuration template file name.
    The application will:
     - verify if the project exists and create a new project if does not
     - update or upload the configuration template
     - commit the template
     - verify the device hostname is valid
     - deploy the template
     - verify completion and status of the template deployment
    """

    # the local date and time when the code will start execution

    date_time = str(datetime.datetime.now().replace(microsecond=0))

    print('\n\nApplication "dnacenter_jinja2_templates.py" Run Started: ' + date_time)

    # get a Cisco DNA Center auth token
    dnac_auth = dnac_apis1.get_dnac_jwt_token(DNAC_AUTH)

    # check if existing project, if not create a new project
    project_id = dnac_apis1.create_project(PROJECT_J2, dnac_auth)
    if project_id == 'none':
        # unable to find or create the project
        print('\nUnable to create the project: ', PROJECT_J2)
        return

    # continue with the project id
    print('The project "' + PROJECT_J2 + '" id is: ' + project_id)

    input('\nEnter any key to continue ')

    # Management IP address configuration
    # create new template and commit if not existing
    # update the existing template and commit if existing

    template_name = MANAGEMENT_INT_J2.split('.')[0]  # select the template name from the template file

    cli_file = open(MANAGEMENT_INT_J2, 'r')  # open file with the template
    cli_config_commands = cli_file.read()  # read the file

    template_param = [
        {
            "parameterName": "interface_number",
            "dataType": "STRING",
            "required": True,
            "order": 1
        },
        {
            "parameterName": "ip_address",
            "dataType": "STRING",
            "required": True,
            "order": 2
        }
    ]

    # verify if existing template in the project
    template_id = dnac_apis1.get_template_id(template_name, PROJECT_J2, dnac_auth)

    if template_id == '':
        print('\nThe template with the name "' + template_name + '" not found, create and commit the template')
        template_id = dnac_apis1.create_commit_template(template_name, PROJECT_J2, cli_config_commands, template_param,
                                              dnac_auth)

    else:
        print('\nThe template with the name "' + template_name + '" found, update and commit template')
        dnac_apis1.update_commit_template(template_name, PROJECT_J2, cli_config_commands,
                                                       template_param, dnac_auth)

    print('The template "' + template_name + '" id is: ', template_id)
    input('\nEnter any key to continue \n')

    # deploy the template
    deployment_id = dnac_apis1.send_deploy_template(template_name, PROJECT_J2, DEVICE_NAME, PARAMS, dnac_auth)

    print('\nTemplate "' + template_name + '" started, task id: "' + deployment_id)
    time.sleep(10)

    deployment_status = dnac_apis1.check_template_deployment_status(deployment_id, dnac_auth)
    print('Deployment task result :', deployment_status)

    # optional, delete the project and template
    input('\nEnter any key to delete the template and project \n')
    dnac_apis1.delete_template(template_name, PROJECT_J2, dnac_auth)
    dnac_apis1.delete_project(PROJECT_J2, dnac_auth)

    date_time = str(datetime.datetime.now().replace(microsecond=0))
    print('\n\nEnd of Application "dnacenter_jinja2_templates.py" Run: ' + date_time)
    return


if __name__ == "__main__":
    main()