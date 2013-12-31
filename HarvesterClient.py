####HarvesterClient.py
## THis is the client portion of the harvester
import sys
import HarvesterLog
import HarvesterIDGrabber
import HarvesterDatabaseIDGrabber
from gevent import monkey
from gevent import Greenlet
monkey.patch_all()
from gevent import socket
from gevent import pool
import gevent
import pickle
from termcolor import colored
import MySQLdb
import Queue
import datetime
import time
import twiAuth
import glob
import twython


class HarvesterClient:
	
			
	def log(self, message):
		self.logger.log(message)
		self.logger2.log(message)
		
	def log2(self, message):
		self.logger2.log(message)		
		
	def receiveWelcomeMessage(self, mysocket):
		socketFileHandle = mysocket.makefile()
		readaline = socketFileHandle.readline()
		print colored(readaline, "red")
		
	#Server is sending a client a list of clients this client should connect to
	def updateClientsList(self, mysocket):
		socket.wait_read(mysocket.fileno())
		socketFileHandle = mysocket.makefile()
		readaline = socketFileHandle.read()
		server_clients = pickle.loads(readaline)	
		self.peerlist.append(server_clients)
	
		
	#The socket should be the command socket
	def connectToServer(self, ip):
		self.log("Connecting to server on " + str(ip))
		mysocket = socket.create_connection((ip, self.server_port), 20)
		self.receiveWelcomeMessage(mysocket)
		self.updateClientsList(mysocket)
		return mysocket
	
	#TODO: When new clients join, server pings client and checks the client version. 
		
	def validateIP(self, ip):
		from IPy import IP
		if ip == "localhost":
			ip = "0.0.0.0"
		try:
			IP(ip)
			self.log("IP: " + str(ip) + "is valid, connecting now")
		except ValueError:
			print ip, "is not a valid IP address"
			sys.exit()
			
	def spawnStreamCapture(self):
		#TODO: Write client code to get client commands
		pass
	
	def connectToOtherClients(self, mysocket):
		if len(self.peerlist) < 1:
			print "I'm the first client"
		else:
			print "Trying to connect to other clients, listed here: ", self.peerlist
			#TODO: figure out if I need to open sockets with other clients, or just use the chat channel. 

	def parseIncoming(self, *args, **kwargs):
		print args, kwargs

	def listenOnSocket(self):
		#TODO: Listen to other clients connection attempts
		while 1:
			print "waiting for server or clients to contact..."
			socketfileno = self.chatComm.fileno()
			gevent.socket.wait_read(socketfileno, event=self.parseIncoming)
	
	def testDBConn(self, conn):
		cursor = conn.cursor()
		try: 
			#Test the connection
			cursor.execute ("SELECT VERSION()")
			print colored("Harvester SQL Database connected", "green")
			row = cursor.fetchone()
			print "\t mysql database server version:", row[0]		
		except ValueError:
			return ValueError
		
	
	def connectToDB(self):
		conn = MySQLdb.connect(host = "harvesterSQL2.cloudapp.net",
                           user = "client",
                           passwd = "pass4Harvester",
                           db = "harvestDB")		
		return conn;
	
	def FolderGrabber(self):
		print "\tSpawned a ID grabber to grab IDs in the neighbouring folders"
		IDfiles = glob.glob('*.txt')
		moreFiles = glob.glob('IDfiles/*')
		IDfiles = IDfiles + moreFiles
		dbconn = self.connectToDB()
		cursor = dbconn.cursor()
		realtime = "2013-11-18 20:29:20" 
		geo = "49.168236527256,-122.857360839844,50km"
		for myfile in IDfiles:
			print "Openign IDFile: ", file
			myfp = open(myfile)
			mycount = 0
			for line in myfp:
				ID = line.strip()
				try:
					cursor.execute("INSERT INTO userIDs(UserID, DateAdded, Location) VALUES(%s, %s, %s)", (str(ID), realtime, geo))
				except MySQLdb.IntegrityError:
					#If the ID is duplicate, ignore it. 
					pass
				mycount = mycount + 1
				if mycount > 10:
					mycount = 0
					dbconn.commit()
	
	def parseStatus(self, status):
		text = status[u'text'].encode('UTF-8')
		UID = status[u'user'][u'id']
		TweetID = status[u'id']
		HashTags = status[u'entities'][u'hashtags']
		Time = status[u'created_at']
		return UID, TweetID, text, HashTags, Time
		
	def grabIDSpawners(self):
		geo = "49.168236527256,-122.857360839844,50km"
		sinceID = self.lastIDGrabbed
		myGrabber = HarvesterIDGrabber.HarvesterIDGrabber(geo, sinceID)
		
		msg = "HarvesterID Grabber is starting to gather IDs beginning from tweetID: " + str(myGrabber.lastID)
		self.log(msg)
		print colored(msg, "yellow")
		
		IDgrabbernum = 1
		print colored("Spawning Tweet Grabbers based on location for ID harvesting")
		while True:
			self.grabIDs(IDgrabbernum, geo, myGrabber)
			IDgrabbernum = IDgrabbernum + 1
		
	
	def grabIDs(self, grabIDnum, geo, myGrabber):
		#Right now only takes IDs from a file
		#Since ID: Starting with 253018723156381696, which is an ID in 2012-10-02
		myname = "[Location-Based Tweet Grabber " + str(grabIDnum) + "] "
		self.log(myname + "is spawned")
		statuses = myGrabber.grabOneSet()
		while len(statuses) < 1:
			gevent.sleep(300)
			statuses = myGrabber.grabOneSet()
		msg = myname + "has grabbed One Set (200) Tweets, extracting UserID and tweets now"
		self.log2(msg)
		priority = 9999

		for status in statuses:
			UID, tweetID, text, HashTags, Time = self.parseStatus(status)
			self.IDqueue.put((UID, tweetID, text, geo, HashTags, Time, priority))
			self.TweetGrabbedQueue.put((text, UID, tweetID, HashTags, Time, priority))			
		myGrabber.lastID = tweetID
		self.lastIDGrabbed = tweetID
			
	def insertStatusIntoNewIDTable(self, status, cursor):
		(UID, tweetID, text, geo, HashTags, Time, priority) = status
		mymsg = "INSERT INTO UserID2(UserID, TweetDate, Location, Frequency) VALUES(%s, %s, %s, 1) ON DUPLICATE KEY UPDATE Frequency = Frequency + 1"
		try:
			cursor.execute(mymsg, (str(UID), str(Time), geo))
		except Exception as e:
			msg = "HarvestClient.insertStatusIntoNewIDTable errored with: " + str(e)
			print colored(msg, "red")
			self.log(msg) 
		
		
	def IDPutter(self, PutterID):
		#GeoCode: 49.168236527256,-122.857360839844,50km
		myName = "[ID Putter " + str(PutterID) + "] "
		msg = myName + "Has spawned"
		print colored(msg, "green")
		self.log(msg)
		numPutted = 0
		
		dbconn = self.connectToDB()
		dbcursor = dbconn.cursor()
		while numPutted < 300:
			status =  self.IDqueue.get(True)
			self.insertStatusIntoNewIDTable(status, dbcursor)
			numPutted += 1
			if numPutted % 10 == 0:
				dbconn.commit()				
		dbconn.commit()
			
		msg = myName + "has made " +str(numPutted) + " insertions, shutting down now. "
		self.log(msg)
		print colored(msg, "green")
		
		dbconn.close()
			
	def spawnIDPutters(self):
		PutterID = 1
		while True:
			self.IDputterPool.spawn(self.IDPutter, PutterID)
			PutterID = PutterID + 1
			gevent.sleep(1)			
		
			
	def print_moduleCompleted(self, moduleName, extramessage=""):
		msg = moduleName + "is successful" + extramessage
		print colored(msg, "green")
		self.log(msg)
	
	def GrabIDFromDatabase(self, GrabberID):		
		myName = "[DB ID Grabber " + str(GrabberID) + "] "	
		self.print_moduleIsSpawned(myName)
		
		#TODO: Change module so that it doesn't rely on using the same table name
		IDGrabber = HarvesterDatabaseIDGrabber.HarvesterDatabaseIDGrabber(self, myName)
		
		IDrow = IDGrabber.grabIDRow()
		ID, frequency = IDGrabber.parseRow(IDrow)
		
		try:
			self.TweetIDQueue.put((ID, frequency), True, 30)
			#FIXME Change the TweetIDQueue.get
		except Queue.Full:
			self.log("[DB ID Grabber " + str(GrabberID) + "] ID Queue is Full, waiting for 5 seconds")
			IDGrabber.closeDBConnection()
			gevent.sleep(5)
			return
		
		IDGrabber.updateRowIntoDatabase(ID)
		IDGrabber.closeDBConnection()

		msg = "and it got the ID: " + str(ID)
		self.print_moduleCompleted(myName, msg)
		#TODO: Set The scanned time to now. 
	
	def resetUserDatabase(self):
		dbconn = self.connectToDB()
		cursor = dbconn.cursor()
		self.log("Clearing all rows that have been grabbed form the user database")
		while True:
			cursor.execute("SELECT * FROM userIDs WHERE NotScanned=1 LIMIT 1000")
			rows = cursor.fetchall()
			if len(rows) < 1:
				return
			for row in rows:
				ID = row[0]
				self.TweetGrabQueue.put(ID, True)
				cursor.execute("Update userIDs SET NotScanned=0 Where UserID=%s ;", str(ID))
				print ID
			dbconn.commit()
			
	def TweetInserter(self, InserterID, InsertTable='newTweets'):
		timeout = gevent.Timeout(800)
		timeout.start()
		try:
			myName = "[Tweet Inserter " + str(InserterID) +  "] "
			msg = myName + "is spawned \t\t"
			print colored(("\t" + msg),"white","on_grey")
			self.log(msg)
			dbConnection = self.connectToDB()
			cursor = dbConnection.cursor()
			self.log2(myName + "Made connection to database, with " + str(dbConnection))
			insertions = 0
			while insertions < 300:
				try:
					status = self.TweetGrabbedQueue.get(True, 10)
					text, UID, TweetID, HashTags, Time, Priority = status
					try:
						#print (InsertTable, str(UID), str(TweetID), text, str(Time), str(HashTags), str(Priority))
						cursor.execute("INSERT INTO newTweets(UserID, TweetID, Text, Time, HashTags, Relevance) VALUES(%s, %s, %s, %s, %s, %s)", (str(UID), TweetID, text, str(Time), str(HashTags), Priority))
					except MySQLdb.IntegrityError:
						msg = myName + "Encountered MYSQL Integrity error with status: " + str(status) + ", Tweet already in database, skipping for now"
						self.log2(msg)
				except Queue.Empty:
					message = myName + "Queue empty timeout (probably due to deadlock), temporarily giving up control"
					gevent.sleep()
					self.log(message)			
				
					#If the ID is duplicate, ignore it. e
				dbConnection.commit()
				insertions = insertions + 1
			finishMsg = "Tweet Inserter " + str(InserterID) + " has made " +str(insertions) + " insertions, shutting down now. "
			self.log(finishMsg)
			print colored(finishMsg, "green")			
		except gevent.Timeout, t:
			if t is not gevent.Timeout:
				msg = myName + "Errored not with a timeout, this is the error message: " + str(t)
				self.log(msg)
			else:
				msg = myName + "Module timed out after 800 seconds. Cleaning up now. "
				self.log(msg)
				print colored(msg, "yellow")
		finally:
			timeout.cancel()
			dbConnection.commit()
			dbConnection.close()
			msg = "[Tweet Inserter "+ str(InserterID) +"] There are " + str(self.TweetGrabbedQueue.qsize()) + " still left in the Tweet Grabbed Queue"
			self.log(msg)
		return 
	
	def print_moduleIsSpawned(self, moduleName):
		msg = moduleName + "is spawned \t\t"
		print colored(('\t' + msg), "white", "on_grey")
		self.log(msg)

	def getStauses(self, UID, lastTweetID, myName):
		api = self.TwiApi
		statuses = api.get_user_timeline(user_id=UID, count=200, max_id=lastTweetID)
		
		msg = myName + "Just got a stack of statuses of size: " + str(len(statuses))
		self.log2(msg)
		
		if len(statuses) == 0:
			stderrMessage = myName + "Empty status queue is returned by Twitter, Assuming there's no more status in the user's history"
			self.log(stderrMessage)
			raise EmptyStatusStack("Empty stack of statuses received. ")
		
		return statuses
		
	def QueueFullError(self, moduleName):
		msg = moduleName + "just hit 10 second queue full timeout (probably due to deadlock), yielding cycles for now, for 5 seconds at least"
		self.log2(msg)
		gevent.sleep(5)
		
	def logTwythonRateLimitError(self, moduleName):
		msg = moduleName + "Hitting the limit (Twython returned twitter error), this ID Grabber is gonna back off for 300 seconds\n"
		self.log(msg)
		sys.stderr.write(colored(msg, "blue"))
		gevent.sleep(750)
	
	def unUsedCode(self):
		pass
		#=======================================================================
		# try: 
		# 	realtime = datetime.datetime.strptime(Time, "%Y-%m-%d %H:%M:%S")
		# except UnboundLocalError as e:
		# 	self.log("Unobund local error from using realtime, even though it's defined at the top of the method")
		# 	print colored(str(e), "yellow")
		#=======================================================================
		
	def handleGrabTweetTimeout(self, e, myName):
		if gevent.Timeout in e:
			msg = myName + "timed out after 1200 seconds. Cleaning up now. "
			self.log(msg)
			print colored(msg, "yellow")
		else:
			msg = myName + "Errored with: " + str(e)
			self.log(msg)
			print colored(msg, "yellow")
			
	def caughtUnknownError(self, moduleName, e):
		msg = moduleName + "Errored with: " + str(e)
		sys.stderr.write(colored(msg, "red"))
		self.log(msg)
	
	def GrabTweetsByID(self, (UID, Frequency), Grabbernum):
		timeout = gevent.Timeout(1200)
		timeout.start()
		try:
			myName = "[Tweet Grabber " + str(Grabbernum) +  "] "
			self.print_moduleIsSpawned(myName)
			cutoff = datetime.datetime(2012, 11, 01)
			lastTweetID = 415486363714590720
			#Time = time.strptime("11 Nov 13", "%d %b %y") ## This line works but makes no sense. I have no clue why it's working. 
			realtime = datetime.datetime.now()
			numTweets = 0
			while (realtime > cutoff and numTweets < 3200):
				try:
					statuses = self.getStauses(UID, lastTweetID, myName)
					for status in statuses:
						UID, tweetID, text, HashTags, Time = self.parseStatus(status)
						try:
							self.TweetGrabbedQueue.put((text, UID, tweetID, HashTags, Time, Frequency), True, 10)
						except Queue.Full:
							self.QueueFullError(myName)
				except (twython.TwythonRateLimitError, twython.TwythonError, EmptyStatusStack) as e:
					if EmptyStatusStack in e:
						break
					elif twython.TwythonRateLimitError in e:
						self.logTwythonRateLimitError(myName)
						continue
					elif twython.TwythonError:
						gevent.sleep(3)
					else:
						self.caughtUnknownError(myName, e)
				else:					
					lastTweetID = tweetID -1
					numTweets = numTweets + len(statuses)
		except (gevent.Timeout, Exception) as e:
			self.handleGrabTweetTimeout(e, myName)
		
		timeout.cancel()
		msg = myName + "Done grabbing tweets User: " + str(UID) + " and grabbed a total of: " + str(numTweets) + " Tweets."
		self.log(msg)
		print colored(msg, "green")
		msg = myName + "There are " + str(self.TweetGrabbedQueue.qsize()) + " still left in the Tweet Grabbed Queue"
		print colored(msg, "green")
		self.log(msg)
		return 
			
	def spawnTweetGrabbers(self):
		Producer = 1
		while True:
			ID, frequency = self.TweetIDQueue.get()
			self.TweetGrabPool.spawn(self.GrabTweetsByID, (ID, frequency), Producer)
			Producer = Producer +1
			gevent.sleep(1)
			
	def spawnTweetInserters(self):
		Consumer = 1
		while True:
			self.TweetInsertPool.spawn(self.TweetInserter, Consumer)
			Consumer = Consumer + 1
			gevent.sleep(1)			
		
	def spawnIDDBGrabbers(self):
		msg = "Spawning Grabbers to get IDs from database now"
		print colored(msg, "green")
		self.log(msg)
		IDGrabberNum = 1
		while True:
			if self.TweetIDQueue.full():
				gevent.sleep(10)
			else:
				self.IDGrabberPool.spawn(self.GrabIDFromDatabase, IDGrabberNum)
				IDGrabberNum = IDGrabberNum + 1
	
	def MonitorThread(self):
		#Monitors the varies pools and Queues make them print their own statuses into the log files.
		#If something is running for more than 20 minutes, kill it. 
		
		while True:
			gevent.sleep(10)
			msg = "[Montior] The pool thinks there are " + str(self.IDGrabberPool.free_count()) + " ID grabber slots, working on a current queue size of: " + str(self.TweetIDQueue.qsize()) + " out of :" + str(self.TweetIDQueue.maxsize)
			self.log(msg)
			for greenlet in self.IDGrabberPool:
				msg = "[Monitor] Currently alive ID Grabber: " + str(greenlet)
				if "kwargs" in dir(greenlet):
					msg = "[Monitor] Currently alive ID Grabber: " + str(greenlet.kwargs)
				elif "args" in dir(greenlet):
					msg = "[Monitor] Currently alive ID Grabber: " + str(greenlet.args)
				self.log2(msg)
			
			msg = "[Montior] The pool thinks there are " + str(self.TweetGrabPool.free_count()) + " available Tweet Grabber slots, and " + str(self.TweetInsertPool.free_count()) + " available Tweet Inserters slots on a current queue size of: " + str(self.TweetGrabbedQueue.qsize())
			self.log(msg)
			for greenlet in self.TweetGrabPool:
				if "args" in dir(greenlet):
					msg = "[Monitor] Currently alive Tweet Grabber: " + str(greenlet.args)
				else:
					msg = "[Monitor] Currently alive Tweet Grabber: " + str(greenlet)
				self.log2(msg)
			for greenlet in self.TweetInsertPool:
				if "args" in dir(greenlet):
					msg = "[Monitor] Currently alive Tweet Inserter: " + str(greenlet.args)
				else:
					msg = "[Monitor] Currently alive Tweet Inserter: " + str(greenlet)
				self.log2(msg)
				
	def printCurrentTime(self):
		msg = "Harvester client STarting time: " + str(datetime.datetime.now())
		print msg
		
	def __init__(self, ip):
		self.peerlist = []
		self.logger = HarvesterLog.HarvesterLog("client")
		self.logger2 = HarvesterLog.HarvesterLog("client_debug")
		self.numAPICalls = 0
		self.printCurrentTime()
		
		#Twitter Auth Stuff
		self.TwiAuth = twiAuth.twiAuth()
		self.TwiApi = self.TwiAuth.Api
		'''
		### Server module
		print "In client mode, attempting to connect to ", ip
		self.validateIP(ip)
		self.server_ip = ip
		self.server_port = 20002
		self.chatComm = self.connectToServer(self.server_ip)
		self.connectToOtherClients(self.chatComm)
		### // Server Module
		'''
		
		### Database Module
		print "Client attempting to connect to database"
		self.dbConn = self.connectToDB()
		self.testDBConn(self.dbConn)
		### // Database Module		
		
		
		### ID Grabbing Module 
		print colored("Starting ID grabbing module", "green")
		self.IDqueue = Queue.Queue(400)
		self.lastIDGrabbed = 253018723156381696
		self.IDGrabber = Greenlet.spawn(self.grabIDSpawners)
		
		self.IDputterPool = gevent.pool.Pool(1)
		Greenlet.spawn(self.spawnIDPutters)
		### // ID grabbing module
		
				
		### Input ID from Folder Module
		#FIXME: Put back the ID folder grabber module
		#self.IDFolderGrabber = Greenlet.spawn(self.FolderGrabber)
		### // Input ID Module
		
		'''
		### Chat Module
		print "Initializing chat module"
		self.clientListener = Greenlet.spawn(self.listenOnSocket)
		### // Chat Module
		'''
		
		### Tweet Grabber Module
		self.TweetIDQueue = Queue.Queue(4)
		self.IDGrabberPool = gevent.pool.Pool(1)
		Greenlet.spawn(self.spawnIDDBGrabbers)
		
		self.TweetGrabbedQueue = Queue.Queue(600)
		self.TweetInsertPool = gevent.pool.Pool(2)
		Greenlet.spawn(self.spawnTweetInserters)
		
		self.TweetGrabPool = gevent.pool.Pool(3)
		Greenlet.spawn(self.spawnTweetGrabbers)				
		
		#=======================================================================
		# self.resetUserDatabase()		
		#=======================================================================
		
		### Monitor Module
		#FIXME: put back the monitor module
		#------------------------------------ Greenlet.spawn(self.MonitorThread)
		### //Monitor Module

		while True:
			gevent.sleep(10)
		
		#TODO: Gracefully shutdown the program by shutdown
		
		### // Twwet Grabber Module
class EmptyStatusStack(Exception):
		def __init__(self, value):
			self.value = value
		def __str__(self):
			return repr(self.value)

