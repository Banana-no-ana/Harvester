### Test gevent framework
###testGevent.py

import Harvester
 
def testGevent():
	import gevent
	

def testHarvester():
	Harvester.runServer()

def testLogger():
	import HarvesterLog
	log = HarvesterLog.HarvesterLog("server")
	log.log("shit's going down")
	log.log("Second line")
	log.close()

def main():
	#testGevent()
	#testHarvester()
	testLogger()



if __name__ == '__main__':
	main()


