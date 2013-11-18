### Test gevent framework
###testGevent.py

import Harvester
apiCalls = 0
dbInsertions = 0
 
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
	
def limitTester(myCreds, max_id):
	global apiCalls
	import twython
	apicalls = 0
	while True:
		try:
			data = myCreds.Api.get_user_timeline(user_id=944411568, count=200, max_id=max_id)
			for tweet in data:
				print tweet[u'id'], tweet[u'text']
			apiCalls = apiCalls + 1
			max_id = max_id - 1000
		except twython.exceptions.TwythonRateLimitError:
			return
		
def testTwitAuth():
	import twython 
	import twiAuth
	import gevent
	#gevent.sleep(900)
	myCreds = twiAuth.twiAuth()
	randomNum = 1401925121566576641
	mypool = gevent.pool.Pool(20)
	spawned = 0
	while True: 
		spawned = spawned + 1
		mypool.spawn(limitTester, myCreds, randomNum)
		randomNum = randomNum - 1000000
		if spawned is 30:
			break
		
		#totalderp = totalderp + int(myderp.value)
	global apiCalls
	print "made this many apiCalls: ", apiCalls
			
def testDBConnection():
	import HarvesterClient
	import socket
	import gevent
	ip = socket.gethostbyname('play4trickster.cloudapp.net')
	myClient = HarvesterClient.HarvesterClient(ip)
	mycursor = myClient.connectToDB()
	
def tonsOfGreenlets():
	import MySQLdb
	import HarvesterClient
	conn = MySQLdb.connect(host = "harvesterSQL.cloudapp.net",
                           user = "client",
                           passwd = "pass4Harvester",
                           db = "harvestDB")
	cursor = conn.cursor()
	global dbInsertions
	numRun = 0
	while numRun < 1000:
		cursor.execute('INSERT INTO testDBCapabilities(UserID, TweetID, Text, Time, HashTags) VALUES(5000, %s, "Mytweet, please.", "2013-03-11 12:05:10", "[blah blahb lahb alsdflasjkbl ]")', (str(dbInsertions)))
		dbInsertions = dbInsertions + 1
		numRun = numRun + 1
		conn.commit()
	
def testDBCapabilities():
	#hammer the database and see if it takes everything. 
	import gevent
	num = 0
	mypool = gevent.pool.Pool(40)
	while num < 50:
		mypool.spawn(tonsOfGreenlets)
		num = num + 1
	mypool.join()
	global dbInsertions
	print "Ran this many times: ", dbInsertions
	
def main():
	#testGevent()
	#testHarvester()
	#testLogger()
	testTwitAuth()
	#testDBConnection()
	#testDBCapabilities()
	


if __name__ == '__main__':
	main()


