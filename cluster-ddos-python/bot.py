#!/usr/bin/env python
import socket, os, subprocess, sys, time, logging
from daemon import Daemon

logger=logging.getLogger('ddos')
logger.setLevel(logging.DEBUG)
logfd=logging.FileHandler('/tmp/ddos.log')
logfd.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logfd.setFormatter(formatter)
logger.addHandler(logfd)

def excute_cmd(cmd):
	if cmd == "test":
		logger.info("test received")

class MyDaemon(Daemon):
	def run(self):
		address = ('localhost',30000)
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind(address)
			s.listen(5)
			logger.info("Now listening on 30000")
		except Exception, e:
			logger.info(e)

		while True:
			ss, addr = s.accept()
			logger.info("Connected with %s", addr)
			ss.send('Welcome to server')
			try:
				rc = ss.recv(1024)
			except Exception, e:
				logger.info(e)
				continue
		ss.close()
		s.close()

if __name__ == "__main__":
	daemon = MyDaemon('/tmp/ddos-daemon.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			logger.info("Daemon start")
			daemon.start()
		elif 'stop' == sys.argv[1]:
			logger.info("Daemon stop")
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
