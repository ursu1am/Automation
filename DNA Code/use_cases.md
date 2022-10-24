#Use Case 01 -  Assurance API Script
This script shows how to use the Cisco DNA Center assurance API's.

DNA Center 2.1.X is required as it has the platform API, which include Assurance.

## Installing
If you are running python2 you will need the requests library.  If you are running and old version of the SSL library you will 
need to update that.
```buildoutcfg
pip install -r requirements.txt

```
## Running the script
The script uses the dnac_config.py file to specify the DNA Center, username and password.
These can also be set using environment variables too.  Run the following commands in the shell (changing the appropriate values)

```buildoutcfg
export DNAC="1.1.1.1"
export DNAC_USER="admin"
export DNAC_PASSWORD="password"
export DNAC_PORT=443

```

Once the credentials are set, the script can be run without arguments.  This will assume the current time as a timestamp and access the 
following API
- site-health - shows the health score for the sites
- device-health - shows the health score for network devices
- client-health - shows the health score for clients (user devices)

The --raw option is used to get raw json output and the --timestamp argument returns health score at a specific time (historical).  This timestamp is in milliseconds.
Some examples include
```buildoutcfg
./assurance.py
./assurance.py --raw
./assurnace.py --timestamp <epoc>
```

The following options return client-detail and device-detail information.  Again they can be called with --raw and --timestamp
```
#  these can also be run with --raw and --timestamp
./assurance.py --mac 00:26:08:E0:F4:97
./assurance.py --hostName 3504_WLC

```

## Example
```buildoutcfg
$ ./assurance.py
https://sandboxdnac.cisco.com:443/dna/intent/api/v1/site-health?timestamp=
Site Health
SiteName            SiteType  Issues  RouterHealth  AccessHealth  ClientHealth  ClientCount
 All Sites          area      0       100           100           100           2
Luxembourg          area      0       100           100           100           2
 All Buildings      building  0       100           100           100           2
LUX                 building  0       100           100           100           2


https://sandboxdnac.cisco.com:443/dna/intent/api/v1/client-health?timestamp=1616569719000
Client health @ 2021-03-24 12:32:00 <-> 2021-03-24 12:37:00 (1616569320000-1616569620000)
ALL 2
WIRED 2
 POOR (0)
 FAIR (0)
 GOOD (2)
 IDLE (0)
 NODATA (0)
 NEW (0)
WIRELESS 0
 POOR (0)
 FAIR (0)
 GOOD (0)
 IDLE (0)
 NODATA (0)
 NEW (0)


https://sandboxdnac.cisco.com:443/dna/intent/api/v1/network-health?timestamp=
Network Health: 100% at 2021-03-24 12:30:00

 Devices Monitored 4, unMonitored 0
Category   Score     Good%     KPI
 Access    100       100
 Distribution100       100
 Router    100       100

```

The client detail shows a view of the topology for the client.  Client is connected to "SDA-Guest" ssid, then to a 3802 AP then a 3504 WLC.

```buildoutcfg
$ ./assurance.py --mac B8:27:EB:70:9F:83
https://adam-dnac:443/dna/intent/api/v1/client-detail?timestamp=&macAddress=B8:27:EB:70:9F:83
Client Detail for:00:F6:63:34:6A:C0 at 2018-10-14 12:11:29 (1539479489498)
HostType: WIRELESS connected to 3804_sda

10.11.200.23(None)[Linux-Workstation] - Health:1 ->
SSID: SDA-Guest(2.4 GHZ) ->
3804_sda:10.11.250.14:AIR-AP3802E-Z-K9(8.5.131.0) - Health:10 ->
3504:10.10.10.147:AIR-CT3504-K9(8.5.131.0) - Health:10

```
## some other tests 
```
python.exe assurance.py --deviceName asr1001-x.abc.inc --raw
https://sandboxdnac.cisco.com:443/dna/intent/api/v1/device-detail?timestamp=1616565649000&searchBy=asr1001-x.abc.inc&identifier=nwDeviceName
{
  "response": {
    "managementIpAddr": "10.10.22.253",
    "haStatus": "Non-redundant",
    "serialNumber": "FXS1932Q1SE",
    "communicationState": "REACHABLE",
    "nwDeviceName": "asr1001-x.abc.inc",
    "platformId": "ASR1001-X",
    "nwDeviceId": "6aad2ec7-d1d0-4605-bf32-f62266c5f53e",
    "nwDeviceRole": "BORDER ROUTER",
    "nwDeviceFamily": "Routers",
    "macAddress": "00:C8:8B:80:BB:00",
    "collectionStatus": "SUCCESS",
    "deviceSeries": "Cisco ASR 1000 Series Aggregation Services Routers",
    "osType": "IOS-XE",
    "ringStatus": false,
    "lastBootTime": 1613509603829,
    "stackType": "NA",
    "softwareVersion": "16.3.2",
    "nwDeviceType": "Cisco ASR 1001-X Router",
    "overallHealth": 10,
    "memoryScore": 10,
    "cpuScore": 10,
    "memory": "2.388763427734375",
    "cpu": "0.0",
    "location": "Global/Luxembourg/LUX",
    "timestamp": "1616565649000"
  }
}
```

## Enrichment
this is only enabled if the serviceNow integration bundle is selected.
The ./enrichment.py file can be used to exercise these API.

There are 4 types of enrichment
- user: get details of the user
- client: similar to user, but also includes issues associated with the userid/mac
- issue: Takes an issue_id or mac_address and finds matching issues
- device: takes an ip_address or mac_address

Some examples:

```buildoutcfg
./enrichment.py --mac_address 00:26:08:E0:F4:97 --etype user
./enrichment.py --network_user_id brad --etype client
./enrichment.py --mac_address 00:26:08:E0:F4:97 --etype issue
./enrichment.py --ip_address 10.10.6.2 --etype device

```
## Use case 02 - Create Site Hierarchy on the Cisco DNA Center via APIs

This is a Python sample code to showcase how to create the Site Hierarchy on the Cisco DNA Center via APIs. The Site Hierarchy is provided in JSON format and the sample code is then able to build this hierarchy on the Cisco DNA Center.

Tools & Frameworks:

Python environment
Usage

$ python3 create-site.py site-info.json
The above example will:

Retrieve the site details from the input file

Create this hierarchy on Cisco DNA Center

Sample output

```

python.exe create-site.py site_example2.json
File Name site_example2.json
US-West Global
{"type": "area", "site": {"area": {"name": "US-West", "parentName": "Global"}}}
{"result": {"result": {"startTime": 1616571872696, "endTime": 1616571872826, "progress": "Site Creation completed successfully"}}, "status": "True", "siteId": "76b454ca-8575-4551-be35-a6fa1c3968ea"}
Area1 US-West
{"type": "area", "site": {"area": {"name": "Area1", "parentName": "US-West"}}}
{"result": {"result": {"startTime": 1616571877391, "endTime": 1616571877488, "progress": "Site Creation completed successfully"}}, "status": "True", "siteId": "85d71b0c-7bb9-4feb-a95e-3ff67f1a06c6"}
Area2 US-West
{"type": "area", "site": {"area": {"name": "Area2", "parentName": "US-West"}}}
{"result": {"result": {"startTime": 1616571880687, "endTime": 1616571880735, "progress": "Site Creation completed successfully"}}, "status": "True", "siteId": "e164765c-a0d5-4221-aca6-552b3f2336d7"}
Area3 US-West
{"type": "area", "site": {"area": {"name": "Area3", "parentName": "US-West"}}}
{"result": {"result": {"startTime": 1616571884786, "endTime": 1616571884837, "progress": "Site Creation completed successfully"}}, "status": "True", "siteId": "af37b0c6-b452-47b8-b708-4dd083bcd0b9"}


---------- Area Creation complete !! ----------


Area1 US-West Area1-BLD1 170 West Tasman Drive, San Jose 95134
{"type": "building", "site": {"area": {"name": "Area1", "parentName": "US-West"}, "building": {"name": "Area1-BLD1", "address": "170 West Tasman Drive, San Jose 95134"}}}
{"result": {"result": {"startTime": 1616571888999, "endTime": 1616571889112, "progress": "Site Creation completed successfully"}}, "status": "True", "siteId": "c62d8666-96fc-427d-96a5-ca68b11ea43c"}
Area1 US-West Area1-BLD2 171 West Tasman Drive, San Jose 95134
{"type": "building", "site": {"area": {"name": "Area1", "parentName": "US-West"}, "building": {"name": "Area1-BLD2", "address": "171 West Tasman Drive, San Jose 95134"}}}
{"result": {"result": {"startTime": 1616571892799, "endTime": 1616571892846, "progress": "Site Creation completed successfully"}}, "status": "True", "siteId": "4436e070-f09e-48be-9194-1b9fc067500e"}
Area2 US-West Area2-BLD1 180 West Tasman Drive, San Jose 95134
{"type": "building", "site": {"area": {"name": "Area2", "parentName": "US-West"}, "building": {"name": "Area2-BLD1", "address": "180 West Tasman Drive, San Jose 95134"}}}
{"result": {"result": {"startTime": 1616571896096, "endTime": 1616571896152, "progress": "Site Creation completed successfully"}}, "status": "True", "siteId": "b117d431-121f-4e82-b5f7-2f8172944a34"}
Area3 US-West Area3-BLD1 190 West Tasman Drive, San Jose 95134
{"type": "building", "site": {"area": {"name": "Area3", "parentName": "US-West"}, "building": {"name": "Area3-BLD1", "address": "190 West Tasman Drive, San Jose 95134"}}}
{"result": {"result": {"startTime": 1616571899320, "endTime": 1616571899399, "progress": "Site Creation completed successfully"}}, "status": "True", "siteId": "a994e5ba-7def-436a-8ae8-f302cd74f451"}
Area3 US-West Area3-BLD2 191 West Tasman Drive, San Jose 95134
{"type": "building", "site": {"area": {"name": "Area3", "parentName": "US-West"}, "building": {"name": "Area3-BLD2", "address": "191 West Tasman Drive, San Jose 95134"}}}
{"result": {"result": {"startTime": 1616571902792, "endTime": 1616571902917, "progress": "Site Creation completed successfully"}}, "status": "True", "siteId": "98178a89-0175-4291-b7b6-aa0f5c1629c5"}


---------- Building Creation complete !! ----------

---------- Site Creation complete !! ----------
```

## Use case 03 Get Site list & Search how many devices per site & Device Discovery 

>> Get the list of all the sites :
```
>python.exe get_sites.py
https://sandboxdnac.cisco.com:443/api/v1/group/count?groupType=SITE
COUNT:2
https://sandboxdnac.cisco.com:443/api/v1/group?groupType=SITE&offset=1&limit=500
name|type|address|id
Global/Luxembourg/LUX|building|79, Rue Basse, Steinsel, Luxembourg|004c606c-c0ff-4871-a103-92e60aab1570
Global/Luxembourg|area|None|e6896d43-b12c-4113-804a-2e65017c8a42
```

>> Cisco DNA Center Devices and Sites
This script will ask the user for input a name for a device or a site. It will collect the sites and devices inventory and search for:

exact match for the device name If found it will return the site name and address for the device
partial match for the site name If found it will return the site name, address and the device inventory for the site
Cisco Products & Services:

Usage

Here are some samples for the the script run for few different user provided values:

Please enter the name of a network device or partial name of a site (using the format "site name/floor #" with "floor #" optional): NYC
The location with the name "Global/NYC", address: "111 8th Ave, Manhattan, New York, New York 10011, United States", has these devices: NYC-ACCESS, NYC-RO

This script may be useful as part of integrations with other workflows for device inventory or network troubleshooting.

```
python.exe device_sites.py

Please enter the name of a network device or partial name of a site (using the format "site name/floor #" with "floor #" optional): Lux

The location with the name "Global/Luxembourg/LUX", address: "79, Rue Basse, Steinsel, Luxembourg",
has these devices: cat_9k_1, cs3850.abc.inc, asr1001-x.abc.inc, cat_9k_2
```
>>> Device Discovery report 

python.exe get_Discovery.py
```
Application "get_discovery.py" Run Started: 2021-03-24 14:39:56
[]

File "device_report.csv" saved

End of application "test-host.py" run
```

## Use case 04 enhancement in use case 3 , get the site list with site ID & then delete those sites , which do not have 
## network devices associated with ( IMP use case for site cleanup & optimization ) 

```
python.exe wlanmgmt.py site-list
Retrieving the sites.
Global/US-East/Area1/Area1-BLD1           81ecef3a-c464-4d24-8a1a-4617dd994580
Global/US-East/Area3           c2e439fb-eda1-42b0-a35b-dc5fd892dd54
Global/US-East/Area3/Area3-BLD2           6eba60c2-d53b-4fab-85ce-218d28b68e06
Global/US-East/Area1           8b7ded8c-910f-4cad-8cbf-70ce1981b131
Global/US-East/Area1/Area1-BLD2           e73767ae-c075-4044-9838-e1e7b2ae709a
Global/US-West/Area1/Area1-BLD1           c62d8666-96fc-427d-96a5-ca68b11ea43c
Global/US-East/Area3/Area3-BLD1           78dd3957-af95-4dcc-a84f-3cff85f34d13
Global/US-West/Area2/Area2-BLD1           b117d431-121f-4e82-b5f7-2f8172944a34
Global/US-West/Area1           85d71b0c-7bb9-4feb-a95e-3ff67f1a06c6
Global/US-West/Area2           e164765c-a0d5-4221-aca6-552b3f2336d7
Global/US-East           2211fee9-ec51-493b-b363-d28f6cdf460d
Global/US-West           76b454ca-8575-4551-be35-a6fa1c3968ea
Global/US-East/Area2           1aeef9e4-ce86-4720-9cef-f832b3dcbe1f
╒════════════╤══════════════════════════════════════╕
│ name       │ id                                   │
╞════════════╪══════════════════════════════════════╡
│ Area1-BLD1 │ 81ecef3a-c464-4d24-8a1a-4617dd994580 │
├────────────┼──────────────────────────────────────┤
│ Area3      │ c2e439fb-eda1-42b0-a35b-dc5fd892dd54 │
├────────────┼──────────────────────────────────────┤
│ Area3-BLD2 │ 6eba60c2-d53b-4fab-85ce-218d28b68e06 │
├────────────┼──────────────────────────────────────┤
│ Area1      │ 8b7ded8c-910f-4cad-8cbf-70ce1981b131 │
├────────────┼──────────────────────────────────────┤
│ Area1-BLD2 │ e73767ae-c075-4044-9838-e1e7b2ae709a │
├────────────┼──────────────────────────────────────┤
│ Area1-BLD1 │ c62d8666-96fc-427d-96a5-ca68b11ea43c │
├────────────┼──────────────────────────────────────┤
│ Area3-BLD1 │ 78dd3957-af95-4dcc-a84f-3cff85f34d13 │
├────────────┼──────────────────────────────────────┤
│ Area2-BLD1 │ b117d431-121f-4e82-b5f7-2f8172944a34 │
├────────────┼──────────────────────────────────────┤
│ Area1      │ 85d71b0c-7bb9-4feb-a95e-3ff67f1a06c6 │
├────────────┼──────────────────────────────────────┤
│ Area2      │ e164765c-a0d5-4221-aca6-552b3f2336d7 │
├────────────┼──────────────────────────────────────┤
│ US-East    │ 2211fee9-ec51-493b-b363-d28f6cdf460d │
├────────────┼──────────────────────────────────────┤
│ US-West    │ 76b454ca-8575-4551-be35-a6fa1c3968ea │
├────────────┼──────────────────────────────────────┤
│ Area2      │ 1aeef9e4-ce86-4720-9cef-f832b3dcbe1f │
╘════════════╧══════════════════════════════════════╛

python.exe delete_sites.py
site id for audit purpose 6eba60c2-d53b-4fab-85ce-218d28b68e06
{'executionId': '4846a8bc-b9de-42a8-b459-0f4f146cfb78', 'executionStatusUrl': '/dna/platform/management/business-api/v1/execution-status/4846a8bc-b9de-42a8-b459-0f4f146cfb78', 'message': 'The request has been accepted for execution'}
site id for audit purpose 8b7ded8c-910f-4cad-8cbf-70ce1981b131
{'executionId': '8b1b0889-0fda-452a-883c-f5d21e2db22c', 'executionStatusUrl': '/dna/platform/management/business-api/v1/execution-status/8b1b0889-0fda-452a-883c-f5d21e2db22c', 'message': 'The request has been accepted for execution'}
site id for audit purpose e73767ae-c075-4044-9838-e1e7b2ae709a
{'executionId': '0cb0fa1a-b0d3-41bf-81cc-436ad75e4a07', 'executionStatusUrl': '/dna/platform/management/business-api/v1/execution-status/0cb0fa1a-b0d3-41bf-81cc-436ad75e4a07', 'message': 'The request has been accepted for execution'}
site id for audit purpose c62d8666-96fc-427d-96a5-ca68b11ea43c
{'executionId': 'c38cfc50-e212-4f54-a2dd-e5473064a960', 'executionStatusUrl': '/dna/platform/management/business-api/v1/execution-status/c38cfc50-e212-4f54-a2dd-e5473064a960', 'message': 'The request has been accepted for execution'}
site id for audit purpose 78dd3957-af95-4dcc-a84f-3cff85f34d13
```

## Use case 05 Baseline configuration vs Runnig configuration automation with ciscoconfparse

\\ Take the backup of all the devices & then run the ciscoconfparse programe to check the configuration deviation 
ciscoconfparse is a Python library, which parses through Cisco IOS-style configurations. It can:
Audit existing router / switch / firewall / wlc configurations
Retrieve portions of the configuration
Modify existing configurations
Build new configurations
The library examines an IOS-style config and breaks it into a set of linked parent / child relationships; each configuration line is stored in a different IOSCfgLine object.

```
---------start----------
C:\\DNAC-TemplateProgrammer\ciscoconfparse\config\BR05RS0001.com.txt
-------------------
Global Config Audit
-------------------
0001  Server Pad              ------------------------------------------------------------ -------->PASS
0002 Service UDP Small Servers------------------------------------------------------------ -------->FAIL
0003 Service TCP Small Servers------------------------------------------------------------ -------->FAIL
0004 SIP Finger               ------------------------------------------------------------ -------->FAIL
0005 SIP bootp Server         ------------------------------------------------------------ -------->FAIL
0006 Platform punt-keepalive disable-kernel-core  ---------------------------------------- -------->FAIL
0007 Source-Route             ------------------------------------------------------------ -------->PASS
0008 Http Server              ------------------------------------------------------------ -------->PASS
0009 Https Server             ------------------------------------------------------------ -------->FAIL
0010 no service dhcp          ------------------------------------------------------------ -------->FAIL
0011 Service tcp-keepalives-in------------------------------------------------------------ -------->PASS
0012 Service tcp-keepalives-out------------------------------------------------------------ ------->PASS
0013 service timestamps debug datetime msec show-timezone--------------------------------- -------->FAIL
0014 service timestamps log datetime msec show-timezone  --------------------------------- -------->FAIL
0015 service password-encryption------------------------------------------------------------ ------->FAIL
0016 LLDP Run                  ------------------------------------------------------------ -------->FAIL
0017 CDP Run                   ------------------------------------------------------------ -------->FAIL
0018 ip domain-name net.ABC LTD.com              ---------------------------------------- -------->FAIL
0019 ip domain-name net.ABC LTD.com              ---------------------------------------- -------->FAIL
0020 ip ssh version 2          ------------------------------------------------------------ -------->PASS
0021 ip ssh time-out 60        ------------------------------------------------------------ -------->PASS
0022 ip ssh auth-retries 3     ------------------------------------------------------------ -------->FAIL
0023 ip ssh source-int vlan1000------------------------------------------------------------ -------->FAIL
0024 ip ssh source-int vlan1000------------------------------------------------------------ -------->PASS
0025 errdisable recovery cause bpduguard           ---------------------------------------- -------->PASS
0026 errdisable recovery cause channel-misconfig   ---------------------------------------- -------->PASS
0027 errdisable recovery cause link-flap           ---------------------------------------- -------->PASS
0028 errdisable recovery cause psecure-violation   ---------------------------------------- -------->PASS
0029 errdisable recovery cause port-mode-failure   ---------------------------------------- -------->PASS
0030 errdisable recovery cause dhcp-rate-limit     ---------------------------------------- -------->PASS
0031 errdisable recovery cause mac-limit           ---------------------------------------- -------->PASS
0032 errdisable recovery cause inline-power        ---------------------------------------- -------->PASS
0033 VTP                       ------------------------------------------------------------ -------->FAIL
0034 spanning-tree mode rapid-pvst       -------------------------------------------------- -------->FAIL
0035 spanning-tree portfast bpduguard default      ---------------------------------------- -------->FAIL
0036 spanning-tree extend system-id      -------------------------------------------------- -------->PASS
0037 udld enable               ------------------------------------------------------------ -------->FAIL
0038 Username & Secret 9 Key   ------------------------------------------------------------ -------->PASS
0039 Banner MOTD               ------------------------------------------------------------ -------->PASS
0040 Service Compress Config   ------------------------------------------------------------ -------->FAIL
0041 logging buffered 16384 debugging    -------------------------------------------------- -------->FAIL
0042 logging console notifications       -------------------------------------------------- -------->PASS
0043 logging host 110.10.10.10           -------------------------------------------------- -------->FAIL
0044 logging host 110.10.10.10           -------------------------------------------------- -------->FAIL
0045 logging host 110.10.10.10 transport udp port 5029    --------------------------------- -------->FAIL
0046 logging origin-id ip      ------------------------------------------------------------ -------->FAIL
0047 logging source-interface Vlan1000   -------------------------------------------------- -------->FAIL
0048 clock timezone GMT 0      ------------------------------------------------------------ -------->FAIL
0049 ip access-list standard DENY-ANY    -------------------------------------------------- -------->FAIL
0050 ip access-list standard NTP-SERVERS -------------------------------------------------- -------->FAIL
0051 remark ABC LTD NTP SRV  ------------------------------------------------------------ -------->FAIL
0052 permit 110.10.10.10     ------------------------------------------------------------ -------->FAIL
``` !! & more lines !!

## Use case 06 Out of Sync(NON-Compliant) & Config-diff report Scripts  

Problem:
startupRunningStatus : OUT_OF_SYNC Report 

Within IOS there are actually two separate files for the configuration. One being the startup-config and the second being the running-config. When a device shows up in the list of devices in the startup/running out of sync report, there is a difference between these two files. This Script with help of DNAC API uses both of these files to build this report .  Once the running-config has been saved to startup-config, the device will no longer show up in this report.

Solution : Use other Script to perform below task : 

Code features :
The Python script uses the Cisco DNAC APIs to get the difference between the running configuration and startup configuration of a device a
Cisco DNAC Controller knows about. The APIs provides the details of the timestamp when the last startup and running configuration change
was done and by whom. It also provides the difference between the running config and startup config for the given device.

Example output sample 

```
python.exe oosync.py
Hostname : leaf1.test.com    startupRunningStatus : Non-Compliant
Hostname : leaf2.test.com    startupRunningStatus : Non-Compliant
Hostname : spine1.test.com    startupRunningStatus : Non-Compliant
```

## Use case 07 Template runner & Deploy Config Scripts 

# Template Programmer
These scripts demonstrate the template programmer API on Cisco DNA Center.
The scripts assume the templates have been setup on Cisco DNA center in advance.

## Running the script
The script needs a DNAC to communicate to via a config file (dnac_config.py) or environmnent variables - 
(DNAC, DNAC_USER, DNAC_PASSWORD).

## get a list of templates
Run the script without argumnents to get a list of templates.

```buildoutcfg
python.exe template.py
Available Templates:
https://sandboxdnac2.cisco.com:443/dna/intent/api/v1/template-programmer/template
  APIIT Testing/SW1
  Arr/dhcp
  Arr/vlan
  Cloud DayN Templates/DMVPN Spoke for Branch Router - System Default
  Cloud DayN Templates/DMVPN for Cloud Router - System Default
  Cloud DayN Templates/IPsec for Branch Router - System Default
  Cloud DayN Templates/IPsec for Cloud Router - System Default
  DAYN_New/basic_config
  Day-N Templates/Add Description
  Day-N Templates/Clear ARP, MAC, Interface Counter
  Day-N Templates/Enable/Disable Interface Switch
  Day-N Templates/Interface Switch Template
  MA/MA-AAA
  MA/MA-Basic Admin
  Onboarding Configuration/DMVPN Hub for Cloud Router- System Default
  Onboarding Configuration/DNA Center Guide - Day2
  Onboarding Configuration/DNA Center Guide - Day3
  Onboarding Configuration/DNA Center Guide - Day4
  Onboarding Configuration/IPsec 1 Branch for Cloud Router - System Default
  Onboarding Configuration/IPsec 2 Branch for Cloud Router - System Default
  Onboarding Configuration/Test template
  Onboarding Configuration/WLC test
  Onboarding Configuration/basic
  Project Test-RTP/Test-RTP-template
  STR/str01
  STR/wireless_roguer
  SanJose Deployment/ChangeDescription
  cis/loopback 18
  prova/prova1
  www.cpm/ACL

```

## look at body of a template
To find out the parameters and other attributes of a template, run the script with the --template option
The script automatically gets the latest version of the template.
It shows you the paramaters required ("vlan" and "interface")
```buildoutcfg
python.exe template.py --template DAYN_New/basic_config
Looking for: DAYN_New/basic_config
https://sandboxdnac2.cisco.com:443/dna/intent/api/v1/template-programmer/template
TemplateId: cc2fd8bc-7aff-4ecf-a8fb-907245a4f031 Version: 2

https://sandboxdnac2.cisco.com:443/dna/intent/api/v1/template-programmer/template/cc2fd8bc-7aff-4ecf-a8fb-907245a4f031
Showing Template Body:
{'name': 'basic_config', 'description': '', 'tags': [], 'author': 'dnacdev', 'deviceTypes': [{'productFamily': 'Switches and Hubs'}], 'softwareType': 'IOS-XE', 'softwareVariant': 'XE', 'templateContent': '## ------ Nonessential services----\r\n!\r\nno service pad\r\nno service udp-small-servers\r\nno service tcp-small-servers\r\nno ip finger\t\t\t\t\t   \r\nno ip bootp server\r\nno platform punt-keepalive disable-kernel-core\r\nno ip source-route\r\nno ip http server\r\nno ip http secure-server\r\n!\r\n!--access switch specific--\r\nno service dhcp\r\n!\r\n## ------ Active services----\r\n!\r\nservice tcp-keepalives-in\r\nservice tcp-keepalives-out\r\nservice timestamps debug datetime msec show-timezone\r\nservice timestamps log datetime msec show-timezone\r\nservice password-encryption\r\n!\r\ncdp run\r\nlldp run\r\n!\r\n## ------ Basic configuration----\r\n\r\n!\r\n#hostname ${hostname}\r\n!\r\nno aaa new-model\r\n!\r\nenable secret cisco123\r\n!\r\nusername cisco privilege 15 secret cisco\r\n!\r\nip domain-name dcloud.cisco.com\r\n!\r\nno ip domain-lookup\r\n!\r\nip ssh version 2\r\nip ssh time-out 60\r\nip ssh authentication-retries 3\r\nip ssh source-interface vlan1000\r\n!\r\ncrypto key generate rsa general-keys modulus 2048 \r\n!\r\nerrdisable recovery cause udld\r\nerrdisable recovery cause bpduguard\r\nerrdisable recovery cause channel-misconfig\r\nerrdisable recovery cause link-flap\r\nerrdisable recovery cause psecure-violation\r\nerrdisable recovery cause port-mode-failure\r\nerrdisable recovery cause dhcp-rate-limit\r\nerrdisable recovery cause mac-limit\r\nerrdisable recovery cause inline-power\r\n!\r\n##---------Spanning Tree Protocol and Associated Protocols -------\r\n!\r\nspanning-tree mode rapid-pvst\r\nspanning-tree loopguard default\r\nspanning-tree portfast bpduguard default\r\nspanning-tree extend system-id\r\n!\r\nudld enable\r\n!\r\nip access-list extended basic_one\r\npermit ip any any\r\n\r\n', 'rollbackTemplateContent': '', 'templateParams': [{'parameterName': 'hostname', 'dataType': 'STRING', 'defaultValue': None, 'description': None, 'required': True, 'notParam': False, 'paramArray': False, 'displayName': None, 'instructionText': None, 'group': None, 'order': 1, 'selection': None, 'range': [], 'key': None, 'provider': None, 'binding': '', 'id': '26df5c10-e86d-49c8-9100-1a55a43a6561'}], 'rollbackTemplateParams': [], 'composite': False, 'containingTemplates': [], 'id': 'cc2fd8bc-7aff-4ecf-a8fb-907245a4f031', 'createTime': 1616674953061, 'lastUpdateTime': 1616675089467, 'parentTemplateId': '1c1fb380-8e68-411d-b035-8b971fd0e5b9'}
## ------ Nonessential services----
!
no service pad
no service udp-small-servers
no service tcp-small-servers
no ip finger
no ip bootp server
no platform punt-keepalive disable-kernel-core
no ip source-route
no ip http server
no ip http secure-server
!
!--access switch specific--
no service dhcp
!
## ------ Active services----
!
service tcp-keepalives-in
service tcp-keepalives-out
service timestamps debug datetime msec show-timezone
service timestamps log datetime msec show-timezone
service password-encryption
!
cdp run
lldp run
!
## ------ Basic configuration----

!
#hostname ${hostname}
!
no aaa new-model
!
enable secret cisco123
!
username cisco privilege 15 secret cisco
!
ip domain-name dcloud.cisco.com
!
no ip domain-lookup
!
ip ssh version 2
ip ssh time-out 60
ip ssh authentication-retries 3
ip ssh source-interface vlan1000
!
crypto key generate rsa general-keys modulus 2048
!
errdisable recovery cause udld
errdisable recovery cause bpduguard
errdisable recovery cause channel-misconfig
errdisable recovery cause link-flap
errdisable recovery cause psecure-violation
errdisable recovery cause port-mode-failure
errdisable recovery cause dhcp-rate-limit
errdisable recovery cause mac-limit
errdisable recovery cause inline-power
!
##---------Spanning Tree Protocol and Associated Protocols -------
!
spanning-tree mode rapid-pvst
spanning-tree loopguard default
spanning-tree portfast bpduguard default
spanning-tree extend system-id
!
udld enable
!
ip access-list extended basic_one
permit ip any any



Required Parameters for template body: {"hostname":""}

Bindings []
```
## apply a template

```python.exe deploy_configs.py


Application "deploy_configs.py" Run Started: 2021-03-25 18:35:17

The template "Disable Access Port" id is:  None
The unreachable devices to which the template will not be deployed are: []
The devices to which the template will be deployed are: ['cat_9k_1', 'cat_9k_2', 'cs3850.abc.inc']

The number of devices to deploy the template to is:  3

What is the device index you want to start with ? (integer between 0 and total number of switches)  0
```










