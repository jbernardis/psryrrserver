
class Indicator:
	def __init__(self, rr, nm):
		self.rr = rr
		self.name = nm
		self.status = False

	def setStatus(self, flag=True):
		if self.status != flag:
			self.status = flag
			self.rr.railroadEvent(self.name, flag)

	def getStatus(self):
		return self.status