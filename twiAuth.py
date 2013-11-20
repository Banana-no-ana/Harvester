##twiAuth.py
##Harvester Twitter Authentication module
import glob
from twython import Twython
import twython
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
		#Test if the API keys are the developers:
		if self.ck in 'UmTtg8DMpMXcgzkbIErSQ':
			print colored("WARNING: You're using the developer's Twitter API keys. Did you forget to change the keys in the AuthFile?" , 'yellow') 
		try: 
			testApi.verify_credentials()
		except twython.exceptions.TwythonAuthError:
			print "Twitter authentication failed with the given authenticators. "
		else:
			print colored("Twitter Authentication seems to be successful", "green")
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
		
		

		
