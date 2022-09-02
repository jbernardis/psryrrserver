
class Switch:
	def __init__(self, rr, nm):
		self.rr = rr
		self.name = nm
		self.normal = False;
		self.reverse = False;
		self.normalPulses = 0;
		self.reversePulses = 0;
		self.locked = False

	# Normal/Reverse position of the turnout itself - inbound
	def setPosition(self, np):
		if np == 1:
			if not self.normal:
				self.rr.railroadEvent(self.name, "N")
			self.normal = True
			self.reverse = False
		elif np == -1:
			if not self.reverse:
				self.rr.railroadEvent(self.name, "R")
			self.normal = False
			self.reverse = True
		else:
			if self.reverse or self.normal:
				self.rr.railroadEvent(self.name, "?")
			self.normal = False
			self.reverse = False

	def getPosition(self): 
		return 1 if self.normal \
			else -1 if self.reverse \
			else 0

	# normal/reverse outbound command.  # indicates number of pulses
	def setOutPulse(self, nv):
		if nv > 0:
			self.normalPulses = nv
			self.reversePulses = 0
		elif nv < 0:
			self.normalPulses = 0
			self.reversePulses = -nv
		else:
			self.normalPulses = 0
			self.reversePulses = 0

	def getOutPulse(self):
		if self.normalPulses > 0:
			self.normalPulses -= 1
			return 1
		elif self.reversePulses > 0:
			self.reversePulses -= 1
			return -1
		else:
			return 0

	# switch locked status indicator - outbound
	def setLocked(self, flag=True):
		self.locked = flag
		self.rr.railroadEvent(self.name, "L")

	def getLocked(self):
		return 1 if self.locked else 0