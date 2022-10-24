import getpass
import telnetlib

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
     tn.write(b"terminal length 0\n")
     tn.write(b'show running \n')
     tn.write(b'show ip interface brief \n')
     tn.write(b'show ip route \n')
     tn.write(b'exit\n')

     readoutput = tn.read_all()
     saveoutput = open("switch" + HOST, "w")
     saveoutput.write(readoutput.decode('ascii'))
     saveoutput.write("n")
     saveoutput.close
