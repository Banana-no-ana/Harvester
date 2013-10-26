####HarvesterServer.py
###Server code for Harvester!

class HarvesterServer:
	def updateClients:
		pass

	def log(self, message):
		self.logger.write(message)

	def _init_(self):
		self.clientlist = []
		self.logger = HarvesterLog.HarvesterLog("server")
