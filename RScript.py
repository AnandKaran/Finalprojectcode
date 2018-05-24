import paramiko
import time

ip = input("enter the ip address:")
username = input("enter the username:")
password = input("enter the password:")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())"""Auto add policy is used to add keys  such as username and passwords"""
ssh.connect(hostname=ip,username=username,password=password)

channel = ssh.invoke_shell()

channel.send("configure terminal\n")
channel.send("int loop 0\n")
channel.send("ip address 1.1.1.1 255.255.255.255\n")
channel.send("int loop 1\n")
channel.send("ip address 2.2.2.2 255.255.255.255\n")
channel.send("router ospf 1\n")
channel.send("network 0.0.0.0 255.255.255.255 area 0\n")



time.sleep(10)
output = channel.recv(65535)


ssh.close()
