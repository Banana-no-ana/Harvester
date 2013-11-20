##HarvesterLog.py
from __future__ import print_function
from easytime import easytime

class HarvesterLog:
	def now(self):
		mytime = easytime.utcnow().convert('Canada/Pacific')
		dateTime = str(mytime).split(".")[0]
		date, Time = dateTime.split(" ")		
		return date + " " + Time
		
	def log(self, message):
		self.open()
		curTime = self.now()
		myMessage = curTime + " : " + message
		print(myMessage, file=self.file)
		self.close()
		return myMessage
		
	def open(self):	
		self.file = open(self.name, 'a')
		
	def close(self):
		self.file.close()
		
	def __init__(self, HarvesterType):
		#Make a new log file.
		self.myType = HarvesterType
		logfolder = 'log/'
		startTime = self.now()
		self.name = logfolder + self.myType + startTime + '.log'
		self.file = open(self.name, 'w')
		self.file.close()
		
	
