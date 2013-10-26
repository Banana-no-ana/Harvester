## Harvester.py
import sys
import HarvesterServer
import HarvesterClient

mode = ""

def main():
	if len(sys.argv) < 2:
		print "Usage: Harvester <Server|Client> (Client address)"
		print "e.g.: Python Harvester.py Server"
		print "or: Python Harvester.py Client 10.0.10.1"
		sys.exit()	
			
	global mode
	mode = sys.argv[1]
	if mode == "server":
		myServer = HarvesterServer.HarvesterServer()
	elif mode == "client":
		if len(sys.argv) < 3:
			print "Need ip address as well"
		ip = sys.argv[2]
		myClient = HarvesterClient.HarvesterClient(ip)	


if __name__ == '__main__':
	main()
