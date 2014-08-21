#!/usr/bin/python
import socket, os, subprocess, sys, time, logging, fcntl, struct, array
from daemon import Daemon

logger=logging.getLogger('ddos')
logger.setLevel(logging.DEBUG)
logfd=logging.FileHandler('/tmp/ddos.log')
logfd.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logfd.setFormatter(formatter)
logger.addHandler(logfd)

def all_interfaces():
	max_possible = 128  # arbitrary. raise if needed.
	bytes = max_possible * 32
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	names = array.array('B', '\0' * bytes)
	outbytes = struct.unpack('iL', fcntl.ioctl(s.fileno(),0x8912,  # SIOCGIFCONF
			struct.pack('iL', bytes, names.buffer_info()[0])
			))[0]
	namestr = names.tostring()
	lst = []
	for i in range(0, outbytes, 40):
		name = namestr[i:i+16].split('\0', 1)[0]
		ip = namestr[i+20:i+24]
		if name.startswith('eth'):
			lst.append((name, ip))
	return lst

def format_ip(addr):
	return str(ord(addr[0])) + '.' + \
	str(ord(addr[1])) + '.' + \
	str(ord(addr[2])) + '.' + \
	str(ord(addr[3]))

#ifs = all_interfaces()
#for i in ifs:
	print "%12s   %s" % (i[0], format_ip(i[1]))

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
				logger.info(rc)
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
