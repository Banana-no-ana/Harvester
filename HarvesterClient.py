####HarvesterClient.py
## THis is the client portion of the harvester
import sys
import HarvesterLog
from gevent import monkey
from gevent import Greenlet
monkey.patch_all()
from gevent import socket
import gevent
from gevent import pool
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
			print "Database connected"
			row = cursor.fetchone()
			print "server version:", row[0]		
		except ValueError:
			return ValueError
		
	
	def connectToDB(self):
		conn = MySQLdb.connect(host = "harvesterSQL2.cloudapp.net",
                           user = "client",
                           passwd = "pass4Harvester",
                           db = "harvestDB")		
		return conn;
	
	def FolderGrabber(self):
		IDfiles = glob.glob('*.txt')
		moreFiles = glob.glob('IDfiles/*')
		IDfiles = IDfiles + moreFiles
		dbconn = self.connectToDB()
		cursor = dbconn.cursor()
		time = datetime.datetime.now()
		realtime = "2013-11-18 20:29:20" 
		geo = "49.168236527256,-122.857360839844,50km"
		for file in IDfiles:
			myfp = open(file)
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
	
	def grabIDs(self):
		#TODO: automatically grab IDs given a particular location
		#Right now only takes IDs from a file
		#put IDs grabbed into self.IDqueue
		#3 sample IDs:496655421, 14601890, 194357523
		
		samples = [496655421, 14601890, 194357523]
		time = datetime.datetime.now()
		geo = "49.168236527256,-122.857360839844,50km"
		for ID in samples:
			self.IDqueue.put((ID, time, geo))
	
	def putIDs(self):
		#TODO: take ID from self.IDqueueu
		#GeoCode: 49.168236527256,-122.857360839844,50km
		while True:
			ID, time, geo =  self.IDqueue.get(True)
			dbcursor = self.dbConn.cursor()
			try:
				dbcursor.execute("INSERT INTO userIDs(UserID, DateAdded, Location) VALUES(%s, %s, %s)", (str(ID), time, geo))
			except MySQLdb.IntegrityError:
				#If the ID is duplicate, ignore it. 
				pass
			self.dbConn.commit()
			
	def GrabIDFromDatabase(self):
		#Fake Some IDS to put onto the TweetGrabQueue 
		#FakeIDS = [944411568, 574672888, 533567950, 732122174, 163931867, 148540517, 499086419]
		dbconn = self.connectToDB()
		cursor = dbconn.cursor()
		while True:
			cursor.execute("SELECT * FROM userIDs WHERE NotScanned=0 LIMIT 5")
			rows = cursor.fetchall()
			for row in rows:
				ID = row[0]
				self.TweetIDQueue.put(ID, True)
				cursor.execute("Update userIDs SET NotScanned=1 Where UserID=%s ;", str(ID))
			dbconn.commit()
			gevent.sleep(540)
			
		#TODO: Set The scanned time to now. 
	
	def resetUserDatabase(self):
		dbconn = self.connectToDB()
		cursor = dbconn.cursor()
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
			
	
	def putUserTweetsInDatabase(self, ID):
		api = self.TwiApi
		dbConnection = self.connectToDB()
		cursor = dbConnection.cursor()
		cutoff = datetime.datetime(2012, 01, 01)
		#This tweet ID is about Nov.16, 2013 
		lastTweetID = 1401925121566576641
		realtime = datetime.datetime.now()
		numTweets = 0
		#TODO: Put into the USERID database that This is the last Tweet we got from them
		
		#While the year is still after 2012, keep searching for more tweets. Remember to sleep
		while (realtime > cutoff and numTweets < 3200):
			statuses = api.get_user_timeline(user_id=ID, count=200, max_id=lastTweetID)
			self.logger.log("Getting Twitter user timeline: " + str(ID) + ", already gotten: " + str(numTweets))
			for status in statuses:
				#I need: Text, UserID, Tweet ID, Time, Hashtags
				text = status[u'text'].encode('UTF-8')
				UID = status[u'user'][u'id']
				TweetID = status[u'id']
				HashTags = status[u'entities'][u'hashtags']
				Time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(status[u'created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
				try:
					print statuses.index(status), UID, TweetID, Time				
					cursor.execute("INSERT INTO testTweets(UserID, TweetID, Text, Time, HashTags) VALUES(%s, %s, %s, %s, %s)", (str(UID), str(TweetID), text, Time, str(HashTags)))
					#print "inserting into the database: UserID, TweetID, Text, Time, Hashtags: ", (str(UID), str(TweetID), text, Time, str(HashTags))
					
				except MySQLdb.IntegrityError:
					#If the ID is duplicate, ignore it. 
					pass
				dbConnection.commit()
				#print UID, TweetID, text, Time, str(HashTags)
			
			realtime = datetime.datetime.strptime(Time, "%Y-%m-%d %H:%M:%S")
			lastTweetID = UID
			numTweets = numTweets + 200
			
		self.logger.log("Done with user timeline: " + str(ID) + ", already gotten: " + str(numTweets))
	
	def TweetInserter(self):
		print "Spawned a tweet inserter into database"
		self.log("Spawned a tweet inserter into database")
		dbConnection = self.connectToDB()
		cursor = dbConnection.cursor()
		numInserts = 0
		while True:
			status = self.TweetGrabbedQueue.get(True)
			text, UID, TweetID, HashTags, Time = status
			try:
				cursor.execute("INSERT INTO testTweets(UserID, TweetID, Text, Time, HashTags) VALUES(%s, %s, %s, %s, %s)", (str(UID), str(TweetID), text, Time, str(HashTags)))
			except MySQLdb.IntegrityError:
				#If the ID is duplicate, ignore it. 
				pass
			numInserts = numInserts +1
			if numInserts > 10:
				dbConnection.commit()
				numInserts = 0
		
	def GrabTweetsByID(self, ID):
		print "In producer"
		api = self.TwiApi
		cutoff = datetime.datetime(2012, 01, 01)
		lastTweetID = 1401925121566576641
		realtime = datetime.datetime.now()
		numTweets = 0
		while (realtime > cutoff and numTweets < 3200):
			try:
				statuses = api.get_user_timeline(user_id=ID, count=200, max_id=lastTweetID)
			except twython.TwythonRateLimitError:
				self.log("Hitting the limit, this ID Grabber is gonna back off for 300 seconds\n")
				sys.stderr.write("Hitting the limit, this ID Grabber is gonna back off for 300 seconds")
				gevent.sleep(300)
			for status in statuses:
				text = status[u'text'].encode('UTF-8')
				UID = status[u'user'][u'id']
				TweetID = status[u'id']
				HashTags = status[u'entities'][u'hashtags']
				Time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(status[u'created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
				self.TweetGrabbedQueue.put((text, UID, TweetID, HashTags, Time), True)
				
			realtime = datetime.datetime.strptime(Time, "%Y-%m-%d %H:%M:%S")
			lastTweetID = UID
			numTweets = numTweets + 200
		
	
	#Block until there's an ID to process on TweetGrabQueue
	def TweetGrabWorker(self):		
		while True:
			ID = self.TweetIDQueue.get()
			self.GrabTweetsByID(ID)
			
	
	def __init__(self, ip):
		self.peerlist = []
		self.logger = HarvesterLog.HarvesterLog("client")
		self.numAPICalls = 0
		
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
		
		
		'''
		### ID Grabbing Module 
		print "Starting ID grabbing module"
		self.IDqueue = Queue.Queue()
		self.IDGrabber = Greenlet.spawn(self.grabIDs)
		self.IDputter = Greenlet.spawn(self.putIDs)
		### // ID grabbing module
		'''
		
		'''
		### Input ID from Folder Module
		self.IDFolderGrabber = Greenlet.spawn(self.FolderGrabber)
		### // Input ID Module
		'''
		
		'''
		### Chat Module
		print "Initializing chat module"
		self.clientListener = Greenlet.spawn(self.listenOnSocket)
		### // Chat Module
		'''
		
		
		### Tweet Grabber Module
		self.TwiAuth = twiAuth.twiAuth()
		self.TwiApi = self.TwiAuth.Api
		self.TweetIDQueue = Queue.Queue()
		self.TweetGrabbedQueue = Queue.Queue()
		self.IDGrabber = Greenlet.spawn(self.GrabIDFromDatabase)
		self.TweetInsertPool = gevent.pool.Pool(10)
		self.TweetGrabPool = gevent.pool.Pool(4)
		while True:
			self.TweetGrabPool.spawn(self.TweetGrabWorker)
			self.TweetInsertPool.spawn(self.TweetInserter)
		#self.resetUserDatabase()
		
		while True:
			gevent.sleep(30)
		
		#TODO: Gracefully shutdown the program by shutdown
		
		### // Twwet Grabber Module
		
		 
		
		
