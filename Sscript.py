import paramiko
import time
ip = input("enter the ip address :")
username = input("enter the username:")
password = input("enter the password:")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=ip,username=username,password=password)

channel = ssh.invoke_shell()

channel.send("config t\n")

for n in range (2,21):
    print ("VLAN " + str(n)+ " Created")
    channel.send("vlan " + str(n) +  "\n")
    channel.send("name Python_VLAN " + str(n) +  "\n")
    time.sleep(1)

channel.send("end\n")

time.sleep(1)
output = channel.recv(65535)

ssh.close()
