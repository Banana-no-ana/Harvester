####HarvesterServer.py
###Server code for Harvester!
import gevent
from gevent import socket
from gevent import monkey
from gevent import Greenlet
monkey.patch_all()
from gevent.server import StreamServer
import HarvesterLog
import pickle
#import pdb

class HarvesterServer:
	def updateClients(self, socket, address):
		if address not in self.clientlist:
			self.clientlist.append((socket, address))
		self.log("Adding client" + str(address) + "to clientList")

	def log(self, message):
		return self.logger.log(message)
	
	def welcomeClient(self, mysocket, address):
		hello_message = "SERVER: Just received a connection from you at " + str(address) + ", sending client list soon \n"
		socketfile = mysocket.makefile()
		socketfile.write(hello_message)
		socketfile.flush()
		self.log("Sent client " + str(address) + "Welcome message")
		gevent.sleep(0.5)
		
	def checkClient(self, client):
		#Ping client, if it responds, then don't worry
		#if it doesn't, then remove it from self.clientlist
		socket, address = client
		socketFile = socket.makefile()
		socketFile.write('pinging, are you online?')
		socketFile.flush()
		socketFile.close()
		
	def checkClients(self):
		#TODO: Go through client list and see if they're online
		for client in self.clientlist:
			Greenlet.spawn(self.checkClient, client)
		
	
	def sendClientsList(self, mysocket, address):
		#Check client list to see if they're still online, remove the ones that aren't
		self.checkClients()
		socketFile = mysocket.makefile()
		if self.clientlist:
			self.log("Sent client list of clients" + str(self.clientlist))
		else:
			self.log("Empty client list not sent to clients")
		#TODO: Pickle only the addresses
		addressOnly = []
		for client in self.clientlist:
			socket, address = client
			addressOnly.append(address)
		pickled = pickle.dumps(addressOnly)
		socketFile.write(pickled)
		socketFile.flush()
		
	def incomeHandle(self, mysocket, address):
		print self.log("incoming request from: " + str(address))
		self.welcomeClient(mysocket, address)
		self.sendClientsList(mysocket, address)
		self.updateClients(mysocket, address)
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
		

