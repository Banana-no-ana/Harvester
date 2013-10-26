####HarvesterClient.py
## THis is the client portion of the harvester
import sys
import HarvesterLog
from gevent import monkey
monkey.patch_all()
from gevent import socket
import pickle

class HarvesterClient:
	def log(self, message):
		self.logger.log(message)
		
	def receiveWelcomeMessage(self, mysocket):
		socketFileHandle = mysocket.makefile()
		print socketFileHandle.readline()
		
	#Server is sending a client a list of clients this client should connect to
	def updateClientsList(self, mysocket):
		fileSocket = mysocket.makefile()
		for line in fileSocket:
			print line
		
	def connectToServer(self, ip):
		self.log("Connecting to server on " + str(ip))
		mysocket = socket.create_connection((ip, 21002), 20)
		self.receiveWelcomeMessage(mysocket)
		self.updateClientsList(mysocket)

		
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
