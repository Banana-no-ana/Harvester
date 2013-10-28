####HarvesterClient.py
## THis is the client portion of the harvester
import sys
import HarvesterLog
from gevent import monkey
monkey.patch_all()
from gevent import socket
import gevent
import pickle
from termcolor import colored

class HarvesterClient:
	def log(self, message):
		self.logger.log(message)
		
	def receiveWelcomeMessage(self, mysocket):
		socketFileHandle = mysocket.makefile()
		readaline = socketFileHandle.readline()
		print colored(readaline, "red")
		
	#Server is sending a client a list of clients this client should connect to
	def updateClientsList(self, mysocket):
		socket.wait_read(mysocket.fileno())
		socketFileHandle = mysocket.makefile()
		readaline = socketFileHandle.read()
		server_clients = pickle.loads(readaline)	
		self.peerlist.append(server_clients)
	
		
	#The socket should be the command socket
	def connectToServer(self, ip):
		self.log("Connecting to server on " + str(ip))
		mysocket = socket.create_connection((ip, self.server_port), 20)
		self.receiveWelcomeMessage(mysocket)
		self.updateClientsList(mysocket)
		return mysocket
		
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
	
	def connectToOtherClients(self, mysocket):
		print "connecting to other clients"

	def listenOnSocket(self, mysocket):
		while 1:
			print "Still listening"
			gevent.sleep(10)
	
	def __init__(self, ip):
		self.peerlist = []
		self.logger = HarvesterLog.HarvesterLog("client")
		print "In client mode, attempting to connect to ", ip
		self.validateIP(ip)
		self.server_ip = ip
		self.server_port = 20002
		#create its own chat socket
		self.chatComm = self.connectToServer(self.server_ip)
		self.connectToOtherClients(self.chatComm)
		self.listenOnSocket(self.chatComm)
		
		
