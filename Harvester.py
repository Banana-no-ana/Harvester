## Harvester.py
import sys
import HarvesterServer
import HarvesterClient
import socket

mode = ""

def serverMode():
	#How should the server get its own ip?
	#I'm expecting users to put in an ip
	myServer = HarvesterServer.HarvesterServer()
	
	
def clientMode(ip):
	myClient = HarvesterClient.HarvesterClient(ip)
	#Assuming client is at this point ready to go
	
	myClient.spawnStreamCapture()	
	#wait for user to input a command, then queue up that command

def main():
	if len(sys.argv) < 2:
		print "Usage: Harvester <Server|Client> (IP address)"
		print "e.g.: Python Harvester.py Server"
		print "or: Python Harvester.py Client 10.0.10.1"
		sys.exit()	
			
	global mode
	mode = sys.argv[1]
	if mode == "server":
		if len(sys.argv) == 2:
			serverMode()
		
	elif mode == "client":
		if len(sys.argv) == 3:
			print "Connecting to your own server with ip: ", sys.argv[2]
			ip = sys.argv[2]
			if ip is "localhost":
				ip = '127.0.0.1'
		if len(sys.argv) == 2:
			print "Defaulting to using developer's cluster"
			ip = socket.gethostbyname('play4trickster.cloudapp.net')
		clientMode(ip)	


if __name__ == '__main__':
	main()
