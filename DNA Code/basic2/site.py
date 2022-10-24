from __future__ import print_function
import json
import logging
import time
import calendar
import csv
from datetime import datetime
from argparse import ArgumentParser
from util import get_url, post_sync, delete

# often addresses have special chars in them
# encoding=utf8
import sys
if sys.version_info < (3,):
    reload(sys)
    sys.setdefaultencoding('utf8')

class Site:
    def __init__(self):
        pass

LIMIT = 500
class SiteCache:
    def __init__(self):
        self._cache = {}
        response = get_url("group/count?groupType=SITE")
        count = response['response']
        print ("COUNT:{}".format(count))

        for start in range(1, count, LIMIT):
            response = get_url("group?groupType=SITE&offset={}&limit={}".format(start,LIMIT))

            sites = response['response']
            for s in sites:
                logging.debug("Caching {}".format(s['groupNameHierarchy']))
                self._cache[s['groupNameHierarchy']] =  s

        self._new_cache_site("Global","area")

    def _new_cache_site(self,name,type):
        self._cache[name] = {'groupNameHierarchy' : name, 'additionalInfo' : [{'attributes' : {'type' :type}}]}

    def lookup(self, fqSiteName):
        if fqSiteName in self._cache:
            return self._cache[fqSiteName]
        else:
            raise ValueError("Cannot find site:{}".format(fqSiteName))

    def split_path(self, full_path):
        parts = full_path.split("/")
        path = '/'.join(parts[:-1])
        site = parts[-1]
        return path, site

    def find_parent(self,full_path):
        path, site = self.split_path(full_path)
        return self.lookup(path)

    def find_children(self,name):

        site = self.lookup(name)

        site_id_path = site['groupHierarchy']
        result = []
        for site in self._cache.values():
            if site['groupNameHierarchy'] != 'Global' and site_id_path in site['groupHierarchy'] :
                result.append({site['groupHierarchy']: site['groupNameHierarchy']})
        print(json.dumps(result, indent=2))
        return sorted(result,reverse=True, key=lambda x: list(x.keys())[0])

    def add_cache(self, name, sitetype):
        self._new_cache_site(name, sitetype)

    def add_dnac(self, name, sitetype, parentname, address):
        path, site = self.split_path(name)
        payload = {
            "type": sitetype,
            "site": {
                sitetype: {
                 "name": site
                }
            }
        }
        if sitetype == "area":
            payload['site'][sitetype]['parentName'] = parentname
        if sitetype == 'building':
            payload['site']['building']['address']= address
        if sitetype != 'area':

            parentpath, parentsite = self.split_path(parentname)

            # need to add an area to the payload for floors and buildings. For a floor the area should not contain the building
            if sitetype == "floor":
                parentpath, parentsite = self.split_path(parentpath)

            # need to add an area
            payload['site']['area'] = {'name' : parentsite, 'parentName': parentpath}

            # fix the parent name to take into account the area
            if sitetype == 'floor':
             payload['site'][sitetype]["parentName"] = parentname.split("/")[-1]

        url = "dna/system/api/v1/site"
        logging.debug("AddSite Payload:{}".format(json.dumps(payload)))
        response = post_sync(url=url, data=payload)

        return response

    def del_dnac(self, site_id):
        url = "group/{}".format(site_id)
        response = delete(url)
        logging.debug(json.dumps(response))
        if 'errorCode' in response:
            return response['message']
        message = response['progress']
        if "failureReason" in response:
            message += '-:{}'.format(response['failureReason'])
        return message

    def parse_sites(self):

        print('{}|{}|{}|{}'.format('name', 'type', 'address', 'id'))
        for site in self._cache.values():

            if 'id' in  site:
                print('{}|{}|{}|{}'.format(site['groupNameHierarchy'],
                                       get_site_type(site),
                                       get_site_address(site),
                                       site['id']))
            else:
                logging.debug("skipping dummy global:")
                logging.debug(site)

def get_site_type(site):
    for a in site['additionalInfo']:
        if 'type' in a['attributes']:
            return a['attributes']['type']

def get_site_address(site):
    for a in site['additionalInfo']:
        if 'address' in a['attributes']:
            return a['attributes']['address']
    return None

def add_locations(location_file, site_cache, commit):
    with open(location_file, "rt") as f:
        reader = csv.DictReader(f, delimiter='|')
        for site in reader:
            logging.debug("Add Location read line:{}".format(json.dumps(site)))
            try:
                parent = site_cache.find_parent(site['name'])
                parent_name = parent['groupNameHierarchy']
                parent_type = get_site_type(parent)
                site_cache.add_cache(site['name'], site['type'])
            except ValueError as e:
                print('Error: no parent for site {}'.format(site['name']))
                continue
            print ('Adding {}[{}] to {}[{}]:'.format(site['name'],site['type'],parent_name, parent_type), end='')
            if commit:

                response = site_cache.add_dnac(site['name'], site['type'],parent_name, address=site['address'])
                logging.debug("Commit/Add/Response" + str(response))
                status = response['status']

                if status == "True":
                   status = "Success"
                else:
                  status = "Failed"
                message = ''
                if "result" in response:
                  message = response['result']
                  if "result" in message:
                      message = message['result']
                  if "progress" in message:
                        message = message['progress']

                print('Status:{}:{}'.format(status, message))
            else:
                print()

def del_locations(location_file, site_cache, commit):
    with open(location_file, "rt") as f:
        reader = csv.DictReader(f, delimiter='|')
        for site in reader:
            print(site['name'])
            try:
                children = site_cache.find_children(site['name'])
                for child in children:
                    site_name = list(child.values())[0]
                    site_id = list(child.keys())[0].split("/")[-1]
                    print("Deleting {}:({})".format(site_name, site_id))
                    if commit:
                        response = site_cache.del_dnac(site_id)
                        print(response)
            except ValueError as e:
                print('Error: no children for site {}:{}'.format(site['name'], e.message))
                continue
            print ('Finished deleting {}'.format(site['name']))

if __name__ == "__main__":
    parser = ArgumentParser(description='Select options.')

    parser.add_argument('--raw', action='store_true',
                        help="raw json")
    parser.add_argument('--commit', action='store_true',
                        help="commit the operation (addition/deletion")
    parser.add_argument('--add',
                        help="add locations from file.  Need to use --commit to make it happen")
    parser.add_argument('--delete',
                        help="del locations from file.  Need to use --commit to make it happen")
    parser.add_argument('-v', action='store_true',
                        help="verbose")
    args = parser.parse_args()
    if args.v:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    site_cache = SiteCache()

    if args.add:
        print("adding from {}".format(args.add))
        add_locations(args.add, site_cache, args.commit)
    elif args.delete:
        print("deleting from {}".format(args.add))
        del_locations(args.delete, site_cache, args.commit)
    else:
        # default
        site_cache.parse_sites()
