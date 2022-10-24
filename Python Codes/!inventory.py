!inventory.py

f = open ('inventory')

for IP in f:
    print(IP)

 !
!inventory

192.168.122.10
192.168.122.11
192.168.122.12
192.168.122.13

##
apt-get update
apt-get install python3
apt-get install python3-pip
pip3 install -U netmiko
