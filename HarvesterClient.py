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
import twiAuth

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
		conn = MySQLdb.connect(host = "harvesterSQL.cloudapp.net",
                           user = "client",
                           passwd = "pass4Harvester",
                           db = "harvestDB")		
		return conn;
	
	def grabIDs(self):
		#TODO: automatically grab IDs given a particular location
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
		FakeIDS = [944411568, 574672888, 533567950, 732122174, 163931867, 148540517, 499086419]
		for ID in FakeIDS:
			self.TweetGrabQueue.put(ID, True)
			
	def getYear(self, lastOne):
		TweetTime = lastOne[0][u'created_at']
		year =  TweetTime.split(' ')[-1].encode('UTF-8')
		return year
	
	def putUserTweetsInDatabase(self, ID):
		api = self.TwiApi
		dbConnection = self.connectToDB()
		curosr = dbConnection.cursor()
		#Get the latest one, and work your way backwards. 
		lastOne = api.get_user_timeline(user_id=ID, count=1)
		lastTweetID = lastOne[0][u'id']
		year = self.getYear(lastOne)
		
			
		
		

		
		
		#TODO: Fill in raw tweets into the database
	
	#Block until there's an ID to process on TweetGrabQueue
	def TweetGrabWorker(self):		
		myPool = pool.Pool(3)
		while True:
			ID = self.TweetGrabQueue.get()
			myPool.spawn(self.putUserTweetsInDatabase, ID)
			
			#TODO: Duplicate the 
			
				
	
	def __init__(self, ip):
		self.peerlist = []
		self.logger = HarvesterLog.HarvesterLog("client")
		
		### Server module
		print "In client mode, attempting to connect to ", ip
		self.validateIP(ip)
		self.server_ip = ip
		self.server_port = 20002
		#self.chatComm = self.connectToServer(self.server_ip)
		#self.connectToOtherClients(self.chatComm)
		### // Server Module
		
		'''
		### Database Module
		print "Client attempting to connect to database"
		self.dbConn = self.connectToDB()
		self.testDBConn(self.dbConn)
		### // Database Module
		'''
		
		'''
		### ID Grabbing Module 
		print "Starting ID grabbing module"
		self.IDqueue = Queue.Queue()
		self.IDGrabber = Greenlet.spawn(self.grabIDs)
		self.IDputter = Greenlet.spawn(self.putIDs)
		### // ID grabbing module
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
		self.TweetGrabQueue = Queue.Queue()
		self.IDGrabber = Greenlet.spawn(self.GrabIDFromDatabase)
		self.TweetGrabber = Greenlet.spawn(self.TweetGrabWorker)	
		
		### // Twwet Grabber Module
		
		gevent.sleep(10)
		
		#TODO: Need to make client constantly check the client list. 
		
		
