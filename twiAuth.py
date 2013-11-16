##twiAuth.py
##Harvester Twitter Authentication module
import glob
from twython import Twython
import twython
import twitter
from termcolor import colored

class twiAuth:
	def loadCredentialfile(self):
		credFile = glob.glob("Auth*")
		if len(credFile) > 1:
			print colored("ERROR: Why are there more than Auth file in your inventory? Sell that to a merchant.", "yellow")
			return False
		if len(credFile) < 1:
			print colored("ERROR: There are no Auth files detected", "yellow")
			return False
		self.mycredFile = open(credFile[0])
			
	def parseCredFile(self):
		for line in self.mycredFile:
			myType, cred = line.split('\t')
			myType = myType.rstrip()
			cred = cred.rstrip()
			if myType == "Consumer_key":
				self.ck = cred
			elif myType == "Consumer_secret":
				self.cks = cred
			elif myType == "Access_token":
				self.at = cred
			elif myType == "Access_token_secret":
				self.ats = cred
		
	def authCreds(self):
		testApi = Twython(self.ck, self.cks, self.at, self.ats) 
		#twitter.Api(consumer_key=self.ck, consumer_secret=self.cks, access_token_key=self.at, access_token_secret=self.ats)
		try: 
			testApi.verify_credentials()
		except twython.exceptions.TwythonAuthError:
			print "Twitter authentication failed with the given authenticators. "
		else:
			return testApi
	
	def __init__(self):
		self.ck = ""
		self.cks = ""
		self.at = ""
		self.ats = ""
		self.mycredFile = file
		if self.loadCredentialfile() == False:
			return
		self.parseCredFile()
		self.Api = self.authCreds()
		
		

		
