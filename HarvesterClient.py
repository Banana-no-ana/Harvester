####HarvesterClient.py
## THis is the client portion of the harvester

class HarvesterClient:
	def log(self, message):
		self.logger.write(message)
	
	def _init_(self):
		self.peerlist = []
		self.logger = HarvesterLog.HarvesterLog("client")
