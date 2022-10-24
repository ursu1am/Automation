import getpass
import telnetlib

HOST = "192.168.122.1"
user = input("Enter your Login Username: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)

tn.read_until(b"Username: ")
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(user.encode('ascii') + b"\n")

tn.write(b"enable\n")
tn.write(b"cisco\n")
tn.write(b"conf t\n")
tn.write(b"interface loopback1\n")
tn.write(b"1.1.1.1 255.255.255.255\n")
tn.write(b"interface loopback2\n")
tn.write(b"1.1.1.2 255.255.255.255\n")
tn.write(b"router eigrp 10\n")
tn.write(b"network 0.0.0.0\n")
tn.write(b"end\n")
tn.write(b"exit\n")

print (tn.read_all().decode('ascii'))