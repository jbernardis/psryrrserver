
class Block:
	def __init__(self, rr, nm):
		self.rr = rr
		self.name = nm
		self.occupied = False
		self.indicator = False

	def getOccupied(self):
		return self.occupied

	def setOccupied(self, flag=True):
		self.occupied = flag

	def getIndicator(self):
		return self.indicator

	def setIndicator(self, flag=True):
		if self.indicator != flag:
			self.indicator = flag
			self.rr.railroadEvent(self.name, flag)