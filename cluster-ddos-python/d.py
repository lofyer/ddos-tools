#!/usr/bin/env python
import socket
import os
import subprocess
import sys
import time
import logging
from daemon import Daemon

logger=logging.getLogger('ddoslogger')
logger.setLevel(logging.DEBUG)
logfd=logging.FileHandler('/tmp/ddos.log')
logfd.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logfd.setFormatter(formatter)
logger.addHandler(logfd)


class MyDaemon(Daemon):
	def run(self):
		address = ('localhost',30000)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(address)
		s.listen(5)
		while True:
			print "As daemon"
			ss, addr = s.accept()
			logger.info("Connected with %s", addr)
			ss.send('Welcome to server')
			try:
				rc = ss.recv(1024)
				output=open('postip.txt','a+')
			except Exception, e:
				logger.info(e)
				continue
			output.write(rc)
			output.close()
		ss.close()
		s.close()

if __name__ == "__main__":
	daemon = MyDaemon('/tmp/daemon-example.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			logging.info("Server start")
			daemon.start()
		elif 'stop' == sys.argv[1]:
			logging.info("Server stop")
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
