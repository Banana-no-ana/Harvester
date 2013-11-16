### Test gevent framework
###testGevent.py

import Harvester
 
def testGevent():
	import gevent
	

def testHarvester():
	#Harvester.runServer()
	pass

def testLogger():
	import HarvesterLog
	log = HarvesterLog.HarvesterLog("server")
	log.log("shit's going down")
	log.log("Second line")
	log.close()
	
def testTwitAuth():
	import twiAuth
	myCreds = twiAuth.twiAuth()
	data = myCreds.Api.get_user_timeline(user_id=944411568, count=200)
	for line in data:
		print line[u'created_at']
		
def testDBConnection():
	import HarvesterClient
	import socket
	import gevent
	ip = socket.gethostbyname('play4trickster.cloudapp.net')
	myClient = HarvesterClient.HarvesterClient(ip)
	mycursor = myClient.connectToDB()
	
def main():
	#testGevent()
	#testHarvester()
	#testLogger()
	testTwitAuth()
	#testDBConnection()
	pass


if __name__ == '__main__':
	main()


