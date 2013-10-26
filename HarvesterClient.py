####HarvesterClient.py
## THis is the client portion of the harvester
import sys
import HarvesterLog
from gevent import monkey
monkey.patch_all()
from gevent.socket import create_connection

class HarvesterClient:
	def log(self, message):
		self.logger.log(message)
		
	def connectToServer(self, ip):
		self.log("Connecting to server on " + str(ip))
		mysocket = create_connection((ip, 21002), 20)

		
	def validateIP(self, ip):
		from IPy import IP
		if ip == "localhost":
			print ip
			ip = "0.0.0.0"
		try:
			IP(ip)
			self.log("IP: " + str(ip) + "is valid, connecting now")
		except ValueError:
			print ip, "is not a valid IP address"
			sys.exit()
		
	
	def __init__(self, ip):
		self.peerlist = []
		self.logger = HarvesterLog.HarvesterLog("client")
		print "In client mode, attempting to connect to ", ip
		self.validateIP(ip)
		self.server_ip = ip
		self.connectToServer(self.server_ip)
