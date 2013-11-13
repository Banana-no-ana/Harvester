####HarvesterServer.py
###Server code for Harvester!
import gevent
from gevent import socket
from gevent import monkey
monkey.patch_all()
from gevent.server import StreamServer
import HarvesterLog
import pickle
#import pdb

class HarvesterServer:
	def updateClients(self, address):
		if address not in self.clientlist:
			self.clientlist.append(address)
		self.log("Adding client" + str(address) + "to clientList")

	def log(self, message):
		return self.logger.log(message)		
	
	def welcomeClient(self, mysocket, address):
		hello_message = "SERVER: Just received a connection from you at " + str(address) + ", sending client list soon \n"
		socketfile = mysocket.makefile()
		socketfile.write(hello_message)
		socketfile.flush()
		self.log("Sent client " + str(address) + "Welcome message")
		gevent.sleep(1)
		
	def checkClients(self):
		#TODO: Fill in check clients code
		pass
	
	def sendClientsList(self, mysocket, address):
		#Check client list to see if they're still online, remove the ones that aren't
		self.checkClients()
		socketFile = mysocket.makefile()
		if self.clientlist:
			self.log("Sent client list of clients" + str(self.clientlist))
		else:
			self.log("Empty client list not sent to clients")
		pickled = pickle.dumps(self.clientlist)
		socketFile.write(pickled)
		socketFile.flush()
		
	def incomeHandle(self, mysocket, address):
		print self.log("incoming request from: " + str(address))
		self.welcomeClient(mysocket, address)
		self.sendClientsList(mysocket, address)
		self.updateClients(address)
		print "Current client list: ", self.clientlist
		
		
	def listenForClients(self):
		self.log("Starting server with port:" + str(self.port))
		print "starting the server on port: ", self.port
		server = StreamServer(('', self.port), self.incomeHandle)
		server.serve_forever()
		print "listening...."
		
	def __init__(self):
		print "Welcome to twitter Harvester server"
		self.clientlist = []
		self.logger = HarvesterLog.HarvesterLog("server")
		self.port = 20002
		self.listenForClients()
		self.commandQueue = []
		

