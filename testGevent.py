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
	
def testAuth():
	import twiAuth
	myCreds = twiAuth.twiAuth()
	data = myCreds.Api.GetStreamSample()
	for line in data:
		print line
def main():
	#testGevent()
	#testHarvester()
	#testLogger()
	#testAuth()



if __name__ == '__main__':
	main()


