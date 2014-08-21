#!/usr/bin/python
import subprocess
import socket
import sys

if (len(sys.argv) != 2):
	print "Usage: control.py cmd"
	sys.exit(0)
# generate ip: ipRange("192.168.0.0","192.168.1.1")
def ipRange(start_ip, end_ip):
	start = list(map(int, start_ip.split(".")))
	end = list(map(int, end_ip.split(".")))
	temp = start
	ip_range = []
	ip_range.append(start_ip)

	while temp != end:
		start[3] += 1
		for i in (3, 2, 1):
			if temp[i] == 256:
				temp[i] = 0
				temp[i-1] += 1
		ip_range.append(".".join(map(str, temp)))    

	return ip_range
# parse config.txt in conf{}
config_file = sys.argv[1]
f = file(config_file,'r')
conf={}
for line in f.read().split('\n'):
	if line != '':
		try:
			if line.startswith('#'):
				continue
			else:
				k, v = line.split('=',1)
				print ("k=%s, v=%s" % (k, v))
				conf[k]=v
		except Exception, e:
			print e
	else:
		pass
#print conf

# here were going to build cmd
cmd = "hping3"

#a=subprocess.Popen("curl ifconfig.me",stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)

#postip=a.stdout.read()

try:
	address = ('localhost', 30000)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(address)
	data = s.recv(1024)
	print "Received data is ", data
	print cmd
	s.send(cmd)
	s.close()
except Exception, e:
	print e
