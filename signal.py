
class Signal:
	def __init__(self, rr, nm):
		self.rr = rr
		self.name = nm
		self.aspect = 0

	def setAspect(self, av=1):
		if av != self.aspect:
			self.aspect = av
			self.rr.railroadEvent(self.name, av)
		return True

	def getAspect(self, abit):
		mask = (1 << abit) & 0xff
		rv = mask & self.aspect
		return 1 if rv != 0 else 0
