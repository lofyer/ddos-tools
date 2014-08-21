#!/usr/bin/python
import subprocess
import socket
import sys

if (len(sys.argv) != 2):
	print "Usage: control.py cmd"
	sys.exit(0)

cmd = sys.argv[1]

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
