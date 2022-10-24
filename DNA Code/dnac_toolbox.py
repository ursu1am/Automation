
import os
import time
import json
import getpass
import click
import requests
from requests.auth import HTTPBasicAuth
import urllib3


DISABLEINSECUREWARNINGS = True

if DISABLEINSECUREWARNINGS:
	urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
	VERIFYCERT=False
else:
	VERIFYCERT=True

# Global variables

# Set DNAC Server IP to your SPECIFIC server ip address
DNAC_SERVER_IP = 'sandboxdnac.cisco.com'
DNAC_AUTHROOT = '/dna/system/api/v1'
DNAC_APIROOT = '/dna/intent/api/v1'

def create_token():
	"""Get API Token from username and password of valid DNA Center user"""
	print('')
	print('WARNING: Insecure certificate warnings have been disabled.')
	print('If you are using a valid certificate set disableInsecureWarnings to False')
	print('')

	username = input('Enter your DNA Center username: ')
	password = getpass.getpass(prompt = 'Enter your DNA Center password: ')

	print('\nRequesting Token...')
	authurl = 'https://' + DNAC_SERVER_IP + DNAC_AUTHROOT + '/auth/token'

	# Remove verify=False if you have a valid certificate installed on your DNA Center and stored on your localhost
	auth_resp = requests.post(authurl, auth=HTTPBasicAuth(username, password), verify=VERIFYCERT)

	try:
		auth_resp.raise_for_status()
	except requests.exceptions.HTTPError as e:
		return "Error: " + str(e)

	auth_token = auth_resp.json()['Token']
	return auth_token

@click.group()
@click.option('--allid', is_flag=True, help='Request all configuration templates from DNA Center appliance (DEFAULT)')
@click.option('--cfgid', help=' Request configuration template for specific ID from DNA Center appliance')

@click.pass_context
def main(ctx, allid, cfgid):
	"""Setup options to pass to commands"""
	click.echo('Connecting to DNA Center Appliance...')
	click.echo()

	ctx.obj = {
        'allid': allid,
		'cfgid': cfgid,
    	}

@main.command()
@click.pass_context
def get_templates(ctx):
	"""Gets configuration templates from DNA Center.  Will GET all templates or GET a single template if --cfgid is provided"""
	cfgid = ctx.obj['cfgid']

	auth_token = create_token()

	hdr = {'x-auth-token': auth_token, 'content-type' : 'application/json'}

	if cfgid is not None:
		templateurl = 'https://' + DNAC_SERVER_IP + DNAC_APIROOT + '/template-programmer/template/'+ cfgid
	else:
		templateurl = 'https://' + DNAC_SERVER_IP + DNAC_APIROOT + '/template-programmer/template/'

	#Remove verify=False if you have a valid certificate installed on your DNA Center and stored on your localhost
	tmpltresp = requests.get(templateurl, headers=hdr, verify=VERIFYCERT)
	template_list = tmpltresp.json()

	print(json.dumps(template_list, indent=4, sort_keys=True))

@main.command()
@click.pass_context
def dwnld_templates(ctx):
	"""Gets configuration templates from DNA Center and downloads them.  Will download either all templates or a single template if --cfgid is provided"""
	cfgid = ctx.obj['cfgid']

	#Get auth_token
	auth_token = create_token()

	#Create time string for filename
	timestr = time.strftime("%Y%m%d-%H%M%S")

	if not os.path.exists('./config-templates'):
		print('Configuration Template folder does not exist.  Creating....')
		print()
		os.makedirs('./config-templates')

	working_dir = './config-templates/'

	hdr = {'x-auth-token': auth_token, 'content-type' : 'application/json'}

	if cfgid is not None:
		templateurl = 'https://' + DNAC_SERVER_IP + DNAC_APIROOT + '/template-programmer/template/'+ cfgid
	else:
		templateurl = 'https://' + DNAC_SERVER_IP + DNAC_APIROOT + '/template-programmer/template/'

	# Get the template(s) based on selected option's URL
	get_response = requests.request("GET", templateurl, headers=hdr, verify = False)

	# Load reponse as JSON and store in resp varible
	resp = json.loads(get_response.text)

	if cfgid is not None:
		print('Downloading template: ' + resp['name'] + ' to ' + working_dir + resp['name'])
		with open(working_dir + resp['name'] + '-' + timestr, 'w') as json_file:
			json.dump(resp, json_file, indent=4, sort_keys=True)
	else:
		for item in resp:
			print('Downloading template: ' + item['name'] + ' to ' + working_dir + item['name'])
			download_templates = requests.request("GET", templateurl + "/" + item['templateId'], headers=hdr, verify = False)
			pretty_template = json.loads(download_templates.text)
			with open(working_dir + item['name'] + '-' + timestr, 'w') as json_file:
				json.dump(pretty_template, json_file, indent=4, sort_keys=True)

if __name__ == "__main__":
	main()