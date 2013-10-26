###Harvester base program
###Two modes: server, or client
###Harvester.py

from __future__ import print_function
import sys
import argparse
import gevent
from gevent import socket
from gevent import monkey
monkey.patch_all()
from gevent.server import StreamServer
from gevent.socket import create_connection
from easytime import easytime	

clients = []
Server_Port = 20002
mode = ""
time = str(easytime.utcnow().convert('Canada/Pacific')).split(".")[0]
log_file = open('log/log'+mode+time+'.log', 'w')

def logwrite(message):
	global log_file
	print(message, log_file)

def welcomeClient(socket, address):
	hello_message = "Just receieved a connection from you at" + str(address)
	socketfile = socket.makefile()
	socketfile.write(hello_message)
	socketfile.flush()
	logwrite("sent message to: " + hello_message)
	
#Incoming server requests are handlded here
def incomeHandle(socket, address):
	logwrite("received inc request from: " + str(address))
	welcomeClient(socket, address)
	

#Starts a server and listens on the Server_Port
def listen():
	global clients
	global Server_Port
	server = StreamServer(('127.0.0.1', Server_Port), incomeHandle)
	server.serve_forever()
	

def runServer():
	(print, "In server mode")
	listen()


def validateIP(ip):
	from IPy import IP
	try:
		IP(ip)
		(print, "IP valid, checking to see if server is online")
	except ValueError:
		(print,  "IP:",  ip, "seems to be invalid")
		sys.exit()
		
def pingServer(ip):
	(print, "Pinging server on", ip)
	(print, "creating connectino with", ip, "at port", Server_Port)
	mysocket = create_connection((ip, Server_Port), 20)
	socketFile = mysocket.makefile()
	for line in socketFile:
		(print, line)
	
def runClient(ip):
	(print,  "In client mode, attempting to connect to ", ip)
	if ip == "localhost":
		ip = "0.0.0.0"
	else:
		validateIP(ip)
	pingServer(ip)
	

def main():
	(print, "Welcome to Twitter Harvester")

	if len(sys.argv) < 2:
		(print,"Usage: Harvester <Server|Client> (Client address)")
		(print, "e.g.: Python Harvester.py Server")
		(print, "or: Python Harvester.py Client 10.0.10.1")
		sys.exit()	
			
	global mode
	mode = sys.argv[1]
	if mode == "server":
		runServer()
	elif mode == "client":
		if len(sys.argv) < 3:
			(print, "Need ip address as well")
		ip = sys.argv[2]
		runClient(ip)	


if __name__ == '__main__':
	main()

