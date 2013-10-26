####HarvesterServer.py
###Server code for Harvester!
import gevent
from gevent import socket
from gevent import monkey
monkey.patch_all()
from gevent.server import StreamServer
import HarvesterLog

class HarvesterServer:
	def updateClients(self, address):
		pass

	def log(self, message):
		return self.logger.log(message)		
		
	def incomeHandle(self, socket, address):
		print self.log("incoming request from: " + str(address))
		self.updateClients(address)
		
	def listenForClients(self):
		self.log("Starting server on 127.0.0.1, with port:" + str(self.port))
		server = StreamServer(('127.0.0.1', self.port), self.incomeHandle)
		server.serve_forever()

	def __init__(self):
		print "Welcome to twitter Harvester server"	
		self.clientlist = []
		self.logger = HarvesterLog.HarvesterLog("server")
		self.port = 21002
		self.listenForClients()
		

