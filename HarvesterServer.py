####HarvesterServer.py
###Server code for Harvester!
import gevent
from gevent import socket
from gevent import monkey
monkey.patch_all()
from gevent.server import StreamServer
import HarvesterLog
from termcolor import colored
import pickle
import pdb

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
		gevent.sleep(3)
	
	def sendClientsList(self, mysocket, address):
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
		print "Current client list: ", self.clientList
		self.updateClients(address)
	
	def wtfHandle(self, wtfsocket, wtfaddress):
		print "Connection came in"
		print wtfaddress
		
	def listenForClients(self):
		self.log("Starting server with port:" + str(self.port))
		print "starting the server on IP: ", self.ip, "on port: ", self.port
		server = StreamServer((self.ip, self.port), self.incomeHandle)
		#testServer = StreamServer(('10.175.160.7', self.port), self.incomeHandle)
		server.serve_forever()
		testServer.serve_forever()

	def __init__(self, ip):
		print "Welcome to twitter Harvester server"
		self.ip = ip
		self.clientlist = []
		self.logger = HarvesterLog.HarvesterLog("server")
		self.port = 20002
		self.listenForClients()
		

