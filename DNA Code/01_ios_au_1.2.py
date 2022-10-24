#!/usr/bin/python -tt

from ciscoconfparse import CiscoConfParse
import sys
import os
import functools
import warnings
import requests
warnings.filterwarnings("ignore")
requests.packages.urllib3.disable_warnings()
os.system('cls')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


BASELINE_DIR = os.path.join(os.getcwd(), "config")
files = sorted(os.listdir(BASELINE_DIR))

num_files = len(files)
   
for i, fin in enumerate(files, 1):
    #  print("diffios: {:>3}/{} Processing: {}".format(i, num_files, fin),
    #        end="\r")
    comparison_file = os.path.join(BASELINE_DIR, fin)
    dname = comparison_file

    #dname = str(sys.argv[1])
    parse = CiscoConfParse(dname)
    
    print('---------start----------')
    print(dname)
    print('-------------------')
    print('Global Config Audit')
    print('-------------------')
    #Requirement - Enabled
    ##------ Nonessential services----
    
    # Service Pad 
    space = '-' * 60
    space1 = '-'* 40
    space2 = '-'* 50
    space3 = '-'* 33
    space4 = '-'* 20
    if parse.find_lines('^no\sservice\spad'):
       print('0001 ' + ' Server Pad              ' + space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0001 '  +' Server Pad              ' + space + '\033[1;31;40m -------->FAIL \033[0;0m')
     
    # Service UDP Small Servers 
    
    if parse.find_lines('^no\sservice\sudp-small-servers'):
       print('0002 ' + 'Service UDP Small Servers '+space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0002 ' + 'Service UDP Small Servers'+space + '\033[1;31;40m -------->FAIL \033[0;0m')
    
    # Service TCP Small Servers
    
    if parse.find_lines('^no\sservice\stcp-small-servers'): 
       print('0003 ' + 'Service TCP Small Servers '+space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0003 ' + 'Service TCP Small Servers'+space + '\033[1;31;40m -------->FAIL \033[0;0m')
    # SIP Finger     
    if parse.find_lines('^no\sip finger'):
        print('0004 ' + 'SIP Finger              '+space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0004 ' + 'SIP Finger               '+space + '\033[1;31;40m -------->FAIL \033[0;0m')
    # SIP Bootp Server 
    if parse.find_lines('^no\sip bootp\sserver'):
      print('0005 ' + 'SIP bootp Server         '+space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0005 ' + 'SIP bootp Server         '+space + '\033[1;31;40m -------->FAIL \033[0;0m')
    
    # Platform punt-keepalive disable-kernel-core
    if parse.find_lines('^no\splatform\spunt-keepalive disable-kernel-core'):
      print('0006 ' + 'Platform punt-keepalive disable-kernel-core  '+space1 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0006 ' + 'Platform punt-keepalive disable-kernel-core  '+space1 + '\033[1;31;40m -------->FAIL \033[0;0m')

    #  Source-Route 
    if parse.find_lines('^no\sip\ssource-route'): 
       print('0007 ' + 'Source-Route             '+space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0007 ' + 'Source-Route             '+space + '\033[1;31;40m -------->FAIL \033[0;0m')
    
    #  Http Server 
    if parse.find_lines('^no\sip\shttp\sserver'):
       print('0008 ' + 'Http Server              '+space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0008 ' + 'Http Server              '+space + '\033[1;31;40m -------->FAIL \033[0;0m')
    

    # Https Server 
    if parse.find_lines('^no\sip\shttp\ssecure-server'):   
       print('0009 ' + 'Https Server             '+space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0009 ' + 'Https Server             '+space + '\033[1;31;40m -------->FAIL \033[0;0m')
        
    #--access switch specific dhcp --
    #no service dhcp
    if parse.find_lines('^no\sservice\sdhcp'):
       print('0010 ' + 'no service dhcp          '+space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0010 ' + 'no service dhcp          '+space + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    ##------ Service tcp-keepalives-in & out --- 
        
    if parse.find_lines(r'service tcp-keepalives-in'): 
       print('0011 ' + 'Service tcp-keepalives-in'+space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0011 ' + 'Service tcp-keepalives-in'+space + '\033[1;31;40m -------->FAIL \033[0;0m')
    
    if parse.find_lines(r'service tcp-keepalives-out'): 
      print('0012 ' + 'Service tcp-keepalives-out'+space + '\033[1;32;40m ------->PASS \033[0;0m')
    else:
      print('0012 ' + 'Service tcp-keepalives-out'+space + '\033[1;31;40m ------->FAIL \033[0;0m')
    
    # service timestamps debug datetime msec show-timezone
    if parse.find_lines(r'service timestamps debug datetime msec show-timezone'):
       print('0013 ' + 'service timestamps debug datetime msec show-timezone'+space3 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0013 ' + 'service timestamps debug datetime msec show-timezone'+space3 + '\033[1;31;40m -------->FAIL \033[0;0m')

    if parse.find_lines(r'service timestamps log datetime msec show-timezone'):
       print('0014 ' + 'service timestamps log datetime msec show-timezone  '+space3 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0014 ' + 'service timestamps log datetime msec show-timezone  '+space3 + '\033[1;31;40m -------->FAIL \033[0;0m')


    if parse.find_lines('^nservice password-encryption'):
      print('0015 ' + 'service password-encryption'+space + '\033[1;32;40m ------->PASS \033[0;0m')
    else:
      print('0015 ' + 'service password-encryption'+space + '\033[1;31;40m ------->FAIL \033[0;0m')

    if parse.find_lines('^nslldp\srun'):
      print('0016 ' + 'LLDP Run                 '+space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0016 ' + 'LLDP Run                  '+space + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines('^ncdp\srun'):
       print('0017 ' + 'CDP Run                  '+space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0017 ' + 'CDP Run                   '+space + '\033[1;31;40m -------->FAIL \033[0;0m')
    
    # Password | SSH Configuration 
    if parse.find_lines(r'ip domain-name net.ABC LTD.com'):
       print('0018 ' + 'ip domain-name net.ABC LTD.com             '+space1 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0018 ' + 'ip domain-name net.ABC LTD.com              '+space1 + '\033[1;31;40m -------->FAIL \033[0;0m')
    
    if parse.find_lines(r'ip ssh dh min size 2048'):
       print('0019 ' + 'ip domain-name net.ABC LTD.com             '+space1 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0019 ' + 'ip domain-name net.ABC LTD.com              '+space1 + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines(r'ip ssh version 2'):
       print('0020 ' + 'ip ssh version 2          '+space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0020 ' + 'ip ssh version 2            '+space + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines(r'ip ssh time-out 60'): 
       print('0021 ' + 'ip ssh time-out 60        '+space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0021 ' + 'ip ssh time-out 60         '+space + '\033[1;31;40m -------->FAIL \033[0;0m')
     
    if parse.find_lines(r'ip ssh authentication-retries 3'):
      print('0022 ' + 'ip ssh auth-retries 3     '        +space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0022 ' + 'ip ssh auth-retries 3     '        +space + '\033[1;31;40m -------->FAIL \033[0;0m') 
      
    if parse.find_lines(r'ip ssh source-interface vlan1000'):
      print('0023 ' + 'ip ssh source-int vlan1000'        +space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0023 ' + 'ip ssh source-int vlan1000'        +space + '\033[1;31;40m -------->FAIL \033[0;0m') 
    
    if parse.find_lines(r'errdisable recovery cause udld'):
       print('0024 ' + 'ip ssh source-int vlan1000'        +space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0024 ' + 'ip ssh source-int vlan1000'        +space + '\033[1;31;40m -------->FAIL \033[0;0m') 
  
  
    if parse.find_lines(r'errdisable recovery cause bpduguard'):
      print('0025 ' + 'errdisable recovery cause bpduguard           '        +space1 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0025 ' + 'errdisable recovery cause bpduguard           '        +space1 + '\033[1;31;40m -------->FAIL \033[0;0m') 
  
    if  parse.find_lines(r'errdisable recovery cause channel-misconfig'):
      print('0026 ' + 'errdisable recovery cause channel-misconfig   '        +space1 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0026 ' + 'errdisable recovery cause channel-misconfig   '        +space1 + '\033[1;31;40m -------->FAIL \033[0;0m') 
       
    if parse.find_lines(r'errdisable recovery cause link-flap'):
      print('0027 ' + 'errdisable recovery cause link-flap           '        +space1 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0027 ' + 'errdisable recovery cause link-flap           '        +space1 + '\033[1;31;40m -------->FAIL \033[0;0m')        
        
    if parse.find_lines(r'errdisable recovery cause psecure-violation'):
      print('0028 ' + 'errdisable recovery cause psecure-violation   '        +space1 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0028 ' + 'errdisable recovery cause psecure-violation   '        +space1 + '\033[1;31;40m -------->FAIL \033[0;0m') 
        
    if parse.find_lines(r'errdisable recovery cause port-mode-failure'):
      print('0029 ' + 'errdisable recovery cause port-mode-failure   '        +space1 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0029 ' + 'errdisable recovery cause port-mode-failure   '        +space1 + '\033[1;31;40m -------->FAIL \033[0;0m') 
       
    if parse.find_lines(r'errdisable recovery cause dhcp-rate-limit'):
      print('0030 ' + 'errdisable recovery cause dhcp-rate-limit     '        +space1 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0030 ' + 'errdisable recovery cause dhcp-rate-limit     '        +space1 + '\033[1;31;40m -------->FAIL \033[0;0m') 
      
    if parse.find_lines(r'errdisable recovery cause mac-limit'):
      print('0031 ' + 'errdisable recovery cause mac-limit           '        +space1 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0031 ' + 'errdisable recovery cause mac-limit           '        +space1 + '\033[1;31;40m -------->FAIL \033[0;0m') 
           
    if parse.find_lines(r'errdisable recovery cause inline-power'):
      print('0032 ' + 'errdisable recovery cause inline-power        '        +space1 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0032 ' + 'errdisable recovery cause inline-power        '        +space1 + '\033[1;31;40m -------->FAIL \033[0;0m') 
        
    #vtp mode
    if parse.find_lines('^vtp\smode\stransparent') or parse.find_lines('^vtp\smode\soff'):
      print('0033 ' + 'VTP                       '        +space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0033 ' + 'VTP                       '         +space + '\033[1;31;40m -------->FAIL \033[0;0m') 
 
##---------Spanning Tree Protocol and Associated Protocols -------

    if parse.find_lines(r'spanning-tree mode rapid-pvst'):
      print('0034 ' + 'spanning-tree mode rapid-pvst       '        +space2 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0034 ' + 'spanning-tree mode rapid-pvst       '        +space2 + '\033[1;31;40m -------->FAIL \033[0;0m') 

## if parse.find_lines('^spanning-tree loopguard default')

    if parse.find_lines(r'spanning-tree portfast bpduguard default'):
      print('0035 ' + 'spanning-tree portfast bpduguard default      '        +space1 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0035 ' + 'spanning-tree portfast bpduguard default      '        +space1 + '\033[1;31;40m -------->FAIL \033[0;0m') 
                                                                       
    if parse.find_lines(r'spanning-tree extend system-id'):            
      print('0036 ' + 'spanning-tree extend system-id      '        +space2 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0036 ' + 'spanning-tree extend system-id      '        +space2 + '\033[1;31;40m -------->FAIL \033[0;0m')                                                               
    if parse.find_lines(r'udld enable'):                               
      print('0037 ' + 'udld enable               '        +space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0037 ' + 'udld enable               '        +space + '\033[1;31;40m -------->FAIL \033[0;0m')

    #enable secret
    if parse.find_lines('^enable\ssecret') or parse.find_lines('^username\sHonMgmtLocal\ssecret\s9'):
      print('0038 ' + 'Username & Secret 9 Key   '        +space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0038 ' + 'Username & Secret 9 Key   '        +space + '\033[1;31;40m -------->FAIL \033[0;0m')
                                                                                                                                   
    #banner motd                                                   
    if parse.find_lines('^banner\smotd'):                          
      print('0039 ' + 'Banner MOTD               '        +space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0039 ' + 'Banner MOTD               '        +space + '\033[1;31;40m -------->FAIL \033[0;0m')
                                                                   
     #service config                                               
    if parse.find_lines(r'service\scompress\sconfig'):             
      print('0040 ' + 'Service Compress Config   '        +space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0040 ' + 'Service Compress Config   '        +space + '\033[1;31;40m -------->FAIL \033[0;0m')
                                                                        
    ## Line console / vty / aux                                    
                                                                   
    if parse.find_lines('^logging buffered 16384 debugging'):
      print('0041 ' + 'logging buffered 16384 debugging    '        +space2 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0041 ' + 'logging buffered 16384 debugging    '        +space2 + '\033[1;31;40m -------->FAIL \033[0;0m')
      
    if parse.find_lines('^logging console notifications'):            
      print('0042 ' + 'logging console notifications       '        +space2 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0042 ' + 'logging console notifications       '        +space2 + '\033[1;31;40m -------->FAIL \033[0;0m')
                                                                      
    if parse.find_lines('^logging host 110.10.10.10'):                
      print('0043 ' + 'logging host 110.10.10.10           '        +space2 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0043 ' + 'logging host 110.10.10.10           '        +space2 + '\033[1;31;40m -------->FAIL \033[0;0m')
    if parse.find_lines('^logging host 110.10.10.10'):                
      print('0044 ' + 'logging host 110.10.10.10           '        +space2 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0044 ' + 'logging host 110.10.10.10           '        +space2 + '\033[1;31;40m -------->FAIL \033[0;0m')

    if parse.find_lines('^logging host 110.10.10.10 transport udp port 5029'):
      print('0045 ' + 'logging host 110.10.10.10 transport udp port 5029    '        +space3 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0045 ' + 'logging host 110.10.10.10 transport udp port 5029    '        +space3 + '\033[1;31;40m -------->FAIL \033[0;0m')
    
    if parse.find_lines('^logging origin-id ip'):                          
      print('0046 ' + 'logging origin-id ip      '        +space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0046 ' + 'logging origin-id ip      '        +space + '\033[1;31;40m -------->FAIL \033[0;0m')

    if parse.find_lines('^logging source-interface Vlan1000'):             
      print('0047 ' + 'logging source-interface Vlan1000  '        +space2 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0047 ' + 'logging source-interface Vlan1000   '        +space2 + '\033[1;31;40m -------->FAIL \033[0;0m')
                                                                           
    # NTP                                                                  
    if parse.find_lines('^clock timezone GMT 0'):                          
      print('0048 ' + 'clock timezone GMT 0      '        +space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0048 ' + 'clock timezone GMT 0      '        +space + '\033[1;31;40m -------->FAIL \033[0;0m')
                                                                           
    if parse.find_lines('^ip access-list standard DENY-ANY'):                                      
      print('0049 ' + 'ip access-list standard DENY-ANY    '        +space2 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0049 ' + 'ip access-list standard DENY-ANY    '        +space2 + '\033[1;31;40m -------->FAIL \033[0;0m')
    
    if parse.find_lines('^ip access-list standard NTP-SERVERS'):           
      print('0050 ' + 'ip access-list standard NTP-SERVERS '        +space2 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0050 ' + 'ip access-list standard NTP-SERVERS '        +space2 + '\033[1;31;40m -------->FAIL \033[0;0m')
      
    if parse.find_lines('^remark ABC LTD NTP SERVERS'):                  
       print('0051 ' + 'remark ABC LTD NTP SRV  '        +space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0051 ' + 'remark ABC LTD NTP SRV  '        +space + '\033[1;31;40m -------->FAIL \033[0;0m')
            
    if parse.find_lines('^permit 110.10.10.10'):                        
        print('0052 ' + 'permit 110.10.10.10     '        +space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0052 ' + 'permit 110.10.10.10     '        +space + '\033[1;31;40m -------->FAIL \033[0;0m')
                        
    if parse.find_lines('^permit 110.10.10.10'):                        
        print('0053 ' + 'permit 110.10.10.10     '        +space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0053 ' + 'permit 110.10.10.10      '        +space + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines('^permit 110.10.10.10'):                        
        print('0054 ' + 'permit 110.10.10.10     '        +space + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0054 ' + 'permit 110.10.10.10      '        +space + '\033[1;31;40m -------->FAIL \033[0;0m')
    if parse.find_lines('^ntp access-group peer NTP-SERVERS'):           
       print('0055 ' + 'ntp access-group peer NTP-SERVERS   '        +space2 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0055 ' + 'ntp access-group peer NTP-SERVERS   '        +space2 + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines('^ntp access-group serve DENY-ANY'):             
       print('0056 ' + 'ntp access-group serve DENY-ANY     '        +space2 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0056 ' + 'ntp access-group serve DENY-ANY     '        +space2 + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines('^ntp access-group serve-only DENY-ANY'):        
       print('0057 ' + 'ntp access-group serve-only DENY-ANY'        +space2 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0057 ' + 'ntp access-group serve-only DENY-ANY'        +space2 + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines('^ntp access-group query-only DENY-ANY'):        
       print('0058 ' + 'ntp access-group query-only DENY-ANY'        +space2 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0058 ' + 'ntp access-group query-only DENY-ANY'        +space2 + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines('^ntp server 110.10.10.10 prefer'):             
       print('0059 ' + 'ntp server 110.10.10.10 prefer     '        +space2 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0059 ' + 'ntp server 110.10.10.10 prefer     '        +space2 + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines('^ntp server 110.10.10.10'):                    
       print('0060 ' + 'ntp server 110.10.10.10            '        +space2 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0060 ' + 'ntp server 110.10.10.10            '        +space2 + '\033[1;31;40m -------->FAIL \033[0;0m')
                                                                               
    #aaa authentication attempts login 5
    if parse.find_lines('^aaa\sauthentication\sattempts\slogin\s5'):
       print('0061 ' + 'aaa authentication attempts login 5 '        +space2 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0061 ' + 'aaa authentication attempts login 5 '        +space2 + '\033[1;31;40m -------->FAIL \033[0;0m')
    
    if parse.find_lines(r'aaa authentication password-prompt "TACACS failure / enter local Password:"'):
       print('0062 ' + 'aaa authentication password-prompt "TACACS failure / enter local Password:           '  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0062 ' + 'aaa authentication password-prompt "TACACS failure / enter local Password:            '  + '\033[1;31;40m -------->FAIL \033[0;0m')
    
    if parse.find_lines(r'aaa authentication username-prompt "TACACS failure / enter local Username:"'):
       print('0063 ' + 'aaa authentication username-prompt "TACACS failure / enter local Username:           '  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0063 ' + 'aaa authentication username-prompt "TACACS failure / enter local Username:            '  + '\033[1;31;40m -------->FAIL \033[0;0m')
        
    if parse.find_lines(r'aaa authentication login default group ABC LTD local'):
     print('0064 ' + 'aaa authentication login default group ABC LTD_loc ' +space3  +'\033[1;32;40m -------->PASS \033[0;0m')
    else:
     print('0064 ' + 'aaa authentication login default group ABC LTD_loc  '+space3 + '\033[1;31;40m -------->FAIL \033[0;0m')
      
    if parse.find_lines(r'aaa authentication enable default group ABC LTD enable'):
      print('0065 ' + 'aaa authentication enable default group ABC LTD enable:          ' +'-------------------' + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0065 ' + 'aaa authentication enable default group ABC LTD enable:          ' +'-------------------'+ '\033[1;31;40m -------->FAIL \033[0;0m')
        
    if parse.find_lines(r'aaa authorization console'):
       print('0066 ' + 'aaa authorization console           '        +space2 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0066 ' + 'aaa authorization console           '        +space2 + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines(r'aaa authorization config-commands'):
       print('0067 ' + 'aaa authorization config-commands             '        +space1 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0067 ' + 'aaa authorization config-commands             '        +space1 + '\033[1;31;40m -------->FAIL \033[0;0m')
        
    if parse.find_lines(r'aaa authorization exec default group ABC LTD if-authenticated'):
       print('0068 ' + 'aaa authorization exec default group ABC LTD if-authenticated   '        +space4 + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0068 ' + 'aaa authorization exec default group ABC LTD if-authenticated   '        +space4 + '\033[1;31;40m -------->FAIL \033[0;0m')
       
        
    if parse.find_lines(r'aaa authorization commands 15 default group ABC LTD if-authenticated'):
        print('0069 ' + 'aaa authorization commands 15 default group ABC LTD if-authenticated                '  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0069 ' + 'aaa authorization commands 15 default group ABC LTD if-authenticated                 '   + '\033[1;31;40m -------->FAIL \033[0;0m')
        
    if parse.find_lines(r'aaa accounting exec default start-stop group ABC LTD'):
       print('0070 ' + 'aaa accounting exec default start-stop group ABC LTD                                '  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0070 ' + 'aaa accounting exec default start-stop group ABC LTD                                '   + '\033[1;31;40m -------->FAIL \033[0;0m')
        
    if parse.find_lines(r'aaa accounting exec commands start-stop group ABC LTD'):
        print('0071 ' + 'aaa accounting exec commands start-stop group ABC LTD                               '  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0071 ' + 'aaa accounting exec commands start-stop group ABC LTD                                '   + '\033[1;31;40m -------->FAIL \033[0;0m')
        
    if parse.find_lines(r'aaa accounting commands 5 default stop-only group ABC LTD'):
       print('0072 ' + 'aaa accounting commands 5 default stop-only group ABC LTD                           '  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0072 ' + 'aaa accounting commands 5 default stop-only group ABC LTD                           '   + '\033[1;31;40m -------->FAIL \033[0;0m')
        
    if parse.find_lines(r'aaa accounting commands 15 default start-stop group ABC LTD'):
        print('0073 ' + 'aaa accounting commands 15 default start-stop group ABC LTD                         '  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0073 ' + 'aaa accounting commands 15 default start-stop group ABC LTD                          '   + '\033[1;31;40m -------->FAIL \033[0;0m')
        
    if parse.find_lines(r'aaa accounting connection default start-stop group ABC LTD'):
        print('0074 ' + 'aaa accounting connection default start-stop group ABC LTD                          '  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0074 ' + 'aaa accounting connection default start-stop group ABC LTD                           '  + '\033[1;31;40m -------->FAIL \033[0;0m')
        
    if parse.find_lines(r'aaa accounting system default start-stop group ABC LTD'):
       print('0075 ' + 'aaa accounting system default start-stop group ABC LTD                              '  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0075 ' + 'aaa accounting system default start-stop group ABC LTD                               '  + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines(r'aaa session-id common'):
       print('0076 ' + 'aaa session-id common     ' +space  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0076 ' + 'aaa session-id common     '  +space + '\033[1;31;40m -------->FAIL \033[0;0m')
     
    if parse.find_lines(r'no snmp-server group default v3 priv'):
       print('0077 ' + 'no snmp-server group default v3 priv' +space2  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0077 ' + 'no snmp-server group default v3 priv'  +space2 + '\033[1;31;40m -------->FAIL \033[0;0m')

    if parse.find_lines(r'snmp-server view ReadView-Internet internet included'):
       print('0078 ' + 'snmp-server view ReadView-Internet internet included              ' +space4  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0078 ' + 'snmp-server view ReadView-Internet internet included              '  +space4 + '\033[1;31;40m -------->FAIL \033[0;0m') 
        
    if parse.find_lines(r'snmp-server group HON-SNMP-RO v3 priv read ReadView-Internet access SNMP-HON-ACL'):
        print('0079 ' + 'snmp-server view ReadView-Internet internet included                                  '+   '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0079 ' + 'snmp-server view ReadView-Internet internet included                                   '+ '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines(r'snmp-server user ABC LTD-ro HON-SNMP-RO v3 auth md5'):
       print('0080 ' + 'snmp-server user ABC LTD-ro HON-SNMP-RO v3 auth md5             ' +space4  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0080 ' + 'snmp-server user ABC LTD-ro HON-SNMP-RO v3 auth md5             '  +space4 + '\033[1;31;40m -------->FAIL \033[0;0m')
            
    if parse.find_lines(r'snmp-server enable traps snmp authentication linkdown linkup coldstart warmstart'):
       print('0081 ' + 'snmp-server enable traps snmp authentication linkdown linkup coldstart warmstart      ' + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0081 ' + 'snmp-server enable traps snmp authentication linkdown linkup coldstart warmstart      ' + '\033[1;31;40m -------->FAIL \033[0;0m')
            
    if parse.find_lines(r'snmp-server enable traps mac-notification change move'):
       print('0082 ' + 'snmp-server enable traps mac-notification change move             ' +space4  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0082 ' + 'snmp-server enable traps mac-notification change move             '+space4   + '\033[1;31;40m -------->FAIL \033[0;0m')
            
    if parse.find_lines(r'snmp-server trap-source Vlan1000'):
       print('0083 ' + 'snmp-server trap-source Vlan1000    ' +space2  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0083 ' + 'snmp-server trap-source Vlan1000    '+space2   + '\033[1;31;40m -------->FAIL \033[0;0m')
            
    if parse.find_lines(r'snmp-server queue-length 20'):
       print('0084 ' + 'snmp-server queue-length 20         ' +space2  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0084 ' + 'snmp-server queue-length 20         '+space2   + '\033[1;31;40m -------->FAIL \033[0;0m')
        
    if parse.find_lines(r'snmp-server location'):
       print('0085 ' + 'snmp-server location                ' +space2  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0085 ' + 'snmp-server location                '+space2   + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines(r'snmp ifmib ifindex persist'):
       print('0086 ' + 'snmp ifmib ifindex persist          ' +space2  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0086 ' + 'snmp ifmib ifindex persist          '+space2   + '\033[1;31;40m -------->FAIL \033[0;0m')
         
    #print('#### forward-protocol | http | secure-active-session-modules| active-session-modules | client | ssh algorithm')
    
    if parse.find_lines(r'ip forward-protocol nd'):
       print('0087 ' + 'ip forward-protocol nd    ' +space  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0087 ' + 'ip forward-protocol nd    '+space   + '\033[1;31;40m -------->FAIL \033[0;0m')
    if parse.find_lines(r'ip http server'):
       print('0088 ' + 'ip http server            ' +space  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0088 ' + 'ip http server            '+space   + '\033[1;31;40m -------->FAIL \033[0;0m')
    if parse.find_lines(r'ip http secure-server'):
       print('0089 ' + 'ip http secure-server     ' +space  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0089 ' + 'ip http secure-server     '+space   + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines(r'ip http secure-active-session-modules none'):
       print('0090 ' + 'ip http secure-active-session-modules none           ' +space3  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0090 ' + 'ip http secure-active-session-modules none           '+space3   + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines(r'ip http active-session-modules none'):
        print('0091 ' + 'ip http active-session-modules none                  ' +space3  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0091 ' + 'ip http active-session-modules none                   '+space3   + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines(r'ip http client source-interface Vlan1'):
       print('0092 ' + 'ip http client source-interface Vlan1                ' +space3  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0092 ' + 'ip http client source-interface Vlan1                '+space3   + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines(r'ip tftp source-interface Vlan1'):
       print('0093 ' + 'ip tftp source-interface Vlan1                       ' +space3  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0093 ' + 'ip tftp source-interface Vlan1                       '+space3   + '\033[1;31;40m -------->FAIL \033[0;0m')
    if parse.find_lines(r'ip ssh time-out 60'):
       print('0094 ' + 'ip ssh time-out 60                  ' +space2  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0094 ' + 'ip ssh time-out 60                  '+space2   + '\033[1;31;40m -------->FAIL \033[0;0m')
    if parse.find_lines(r'ip ssh source-interface Vlan1'):
        print('0095 ' + 'ip ssh source-interface Vlan1       ' +space2  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0095 ' + 'ip ssh source-interface Vlan1        '+space2   + '\033[1;31;40m -------->FAIL \033[0;0m')
    if parse.find_lines(r'ip ssh version 2'):
       print('0100 ' + 'ip ssh version 2                    ' +space2  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0100 ' + 'ip ssh version 2                    '+space2   + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines(r'ip ssh server algorithm mac hmac-sha2-256 hmac-sha2-512 hmac-sha1'):
       print('0100 ' + 'ip ssh server algorithm mac hmac-sha2-256 hmac-sha2-512 hmac-sha1 ' +space4  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0100 ' + 'ip ssh server algorithm mac hmac-sha2-256 hmac-sha2-512 hmac-sha1 '+space4   + '\033[1;31;40m -------->FAIL \033[0;0m')
    if parse.find_lines(r'ip ssh client algorithm mac hmac-sha2-256 hmac-sha2-512 hmac-sha1'):
       print('0101 ' + 'ip ssh client algorithm mac hmac-sha2-256 hmac-sha2-512 hmac-sha1 ' +space4  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0101 ' + 'ip ssh client algorithm mac hmac-sha2-256 hmac-sha2-512 hmac-sha1 '+space4   + '\033[1;31;40m -------->FAIL \033[0;0m')
     
     
    if parse.find_lines(r'aaa new-model'):
        print('0102 ' + 'aaa new-model             ' +space  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0102 ' + 'aaa new-model              '+space   + '\033[1;31;40m -------->FAIL \033[0;0m')
    if parse.find_lines(r'radius server ISE-VIP-DCE'):
        print('0103 ' + 'radius server ISE-VIP-DCE          ' +space2  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0103 ' + 'radius server ISE-VIP-DCE           '+space2   + '\033[1;31;40m -------->FAIL \033[0;0m')
    if parse.find_lines(r'radius server ISE-VIP-APAC'):
       print('0104 ' + 'radius server ISE-VIP-APAC          ' +space2  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0104 ' + 'radius server ISE-VIP-APAC          '+space2   + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines(r'aaa group server radius ABC LTD-ISE'):
      print('0105 ' + 'aaa group server radiu ABC LTD-ISE' +space2  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
      print('0105 ' + 'aaa group server radiu ABC LTD-ISE'+space2   + '\033[1;31;40m -------->FAIL \033[0;0m')
    if parse.find_lines(r'aaa authentication dot1x default group ABC LTD-ISE'):
        print('0106 ' + 'aaa authentication dot1x default group ABC LTD-ISE ' +space3  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0106 ' + 'aaa authentication dot1x default group ABC LTD-ISE '+space3   + '\033[1;31;40m -------->FAIL \033[0;0m')
    if parse.find_lines(r'aaa authorization network default group ABC LTD-ISE'):
        print('0107 ' + 'aaa authorization network default group ABC LTD-ISE             ' +space4  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0107 ' + 'aaa authorization network default group ABC LTD-ISE              '+space4   + '\033[1;31;40m -------->FAIL \033[0;0m')
    
    if parse.find_lines(r'aaa authorization network auth-list group ABC LTD-ISE'):
        print('0108 ' + 'aaa authorization network auth-list grp ABC LTD-ISE' +space3  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0108 ' + 'aaa authorization network auth-list grp ABC LTD-ISE'+space3   + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines(r'aaa authorization network cts-list group ABC LTD-ISE'):
       print('0109 ' + 'aaa authorization network cts-list group ABC LTD-ISE' +space3  + '\033[1;32;40m ------->PASS \033[0;0m')
    else:
       print('0109 ' + 'aaa authorization network cts-list group ABC LTD-ISE'+space3   + '\033[1;31;40m ------->FAIL \033[0;0m')
       
    if parse.find_lines(r'aaa authorization credential-download cts-list group ABC LTD-ISE'):
        print('0110 ' + 'aaa authorization credential-download cts-list group ABC LTD-ISE' +space4  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0110 ' + 'aaa authorization credential-download cts-list group ABC LTD-ISE'+space4   + '\033[1;31;40m -------->FAIL \033[0;0m')
    if parse.find_lines(r'aaa authorization auth-proxy default group ABC LTD-ISE'):
        print('0111 ' + 'aaa authorization auth-proxy default group ABC LTD-ISE          ' +space4  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0111 ' + 'aaa authorization auth-proxy default group ABC LTD-ISE           '+space4   + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines(r'aaa accounting auth-proxy default start-stop group ABC LTD-ISE'):
       print('0112 ' + 'aaa accounting auth-proxy default start-stop group ABC LTD-ISE  ' +space4  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0112 ' + 'aaa accounting auth-proxy default start-stop group ABC LTD-ISE  '+space4   + '\033[1;31;40m -------->FAIL \033[0;0m')
    if parse.find_lines(r'aaa accounting dot1x default start-stop group ABC LTD-ISE'):
       print('0113 ' + 'aaa accounting dot1x default start-stop group ABC LTD-ISE       ' +space4  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0113 ' + 'aaa accounting dot1x default start-stop group ABC LTD-ISE       '+space4   + '\033[1;31;40m -------->FAIL \033[0;0m')
    if parse.find_lines(r'aaa accounting update newinfo periodic 55'):
        print('0114 ' + 'aaa accounting update newinfo periodic 55            ' +space3  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0114 ' + 'aaa accounting update newinfo periodic 55             '+space3   + '\033[1;31;40m -------->FAIL \033[0;0m')
    if parse.find_lines(r'aaa server radius dynamic-author'):
       print('0115 ' + 'aaa server radius dynamic-author                     ' +space3  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0115 ' + 'aaa server radius dynamic-author                     '+space3   + '\033[1;31;40m -------->FAIL \033[0;0m')
    if parse.find_lines(r'aaa session-id common'):   
        print('0116 ' + 'aaa session-id common               ' +space2  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0116 ' + 'aaa session-id common                '+space2   + '\033[1;31;40m -------->FAIL \033[0;0m')
    #print('### VLAN Testing from here #### ')        
    if parse.find_lines(r'VLAN 710'):
        print('0117 ' + 'VLAN 710                 ' +space  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0117 ' + 'VLAN 710                  '+space   + '\033[1;31;40m -------->FAIL \033[0;0m')   
    if parse.find_lines(r'vlan 801'):
       print('0118 ' + 'VLAN 801                  ' +space  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0118 ' + 'VLAN 801                  '+space   + '\033[1;31;40m -------->FAIL \033[0;0m')
    if parse.find_lines(r'vlan 802'):
       print('0119 ' + 'VLAN 802                  ' +space  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0119 ' + 'VLAN 802                  '+space   + '\033[1;31;40m -------->FAIL \033[0;0m')     
    if parse.find_lines(r'vlan 803'):
       print('0120 ' + 'VLAN 803                  ' +space  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0120 ' + 'VLAN 803                  '+space   + '\033[1;31;40m -------->FAIL \033[0;0m')       
    if parse.find_lines(r'vlan 804'):
       print('0121 ' + 'VLAN 804                  ' +space  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0121 ' + 'VLAN 804                  '+space   + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines(r'vlan 805'):
       print('0122 ' + 'VLAN 805                  ' +space  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0122 ' + 'VLAN 805                  '+space   + '\033[1;31;40m -------->FAIL \033[0;0m')
       
    if parse.find_lines(r'vlan 1000'):
       print('0123 ' + 'VLAN 806                  ' +space  + '\033[1;32;40m -------->PASS \033[0;0m')
    else:
       print('0123 ' + 'VLAN 806                  '+space   + '\033[1;31;40m -------->FAIL \033[0;0m')
       

