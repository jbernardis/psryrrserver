
class Block:
	def __init__(self, rr, nm):
		self.rr = rr
		self.name = nm
		self.occupied = False
		self.indicator = False
		self.objName = type(self).__name__

	def setAspect(self, av=1):
		if av != self.aspect:
			self.aspect = av
			self.rr.railroadEvent({self.objName: {self.name: av}})
		return True

	def getAspect(self, abit):
		mask = (1 << abit) & 0xff
		rv = mask & self.aspect
		return 1 if rv != 0 else 0