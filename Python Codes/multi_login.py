import getpass
import telnetlib

HOST = "localhost"
user = input("Enter your Login Username: ")
password = getpass.getpass()

f = open ('inventory')

for IP in f:
	IP=IP.strip()
	print ("Configure the switches " + (IP))
	HOST = IP 
    tn = telnetlib.Telnet(HOST)
    tn.read_until(b"Username: ")
    tn.write(user.encode('ascii') + b"\n")
    if password:
       tn.read_until(b"Password: ")
       tn.write(user.encode('ascii') + b"\n")
	tn.write(b"enable\n")
	tn.write(b"cisco\n")
	tn.write(b"conf t\n")
	tn.write(b"vlan 10\n")
	tn.write(b"name SALES\n")
	tn.write(b"vlan 20\n")
	tn.write(b"name HR\n")
	tn.write(b"exit\n")
	tn.write(b"router eigrp 10\n")
	tn.write(b"network 0.0.0.0\n")
	tn.write(b"end\n")
	tn.write(b"exit\n")

    print (tn.read_all().decode('ascii'))