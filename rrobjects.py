class Input:
	def __init__(self, name):
		self.name = name
		self.value = 0

class Output:
	def __init__(self, name):
		self.name = name
		self.value = 0
		self.objName = type(self).__name__

class IndicatorOutput(Output):
	def __init__(self, name):
		Output.__init__(self, name)
		self.status = False

	def SetStatus(self, flag=True):
		if self.status != flag:
			self.status = flag
			self.rr.railroadEvent({self.objName: {self.name: flag}})

	def GetStatus(self):
		return self.status

class RelayOutput(IndicatorOutput):
	def __init__(self, name):
		IndicatorOutput.__init__(self, name)

class SignalOutput(Output):
	def __init__(self, name):
		Output.__init__(self, name)
		self.aspect = 0

	def SetAspect(self, av=1):
		if av != self.aspect:
			self.aspect = av
			self.rr.railroadEvent({self.objName: {self.name: av}})
		return True

	def IsAspectNonZero(self):
		return self.aspect != 0

	def GetAspect(self, abit):
		mask = (1 << abit) & 0xff
		rv = mask & self.aspect
		return 1 if rv != 0 else 0

class PulsedOutput(Output):
	def __init__(self, name, pulseLen):
		Output.__init__(self, name)
		self.pulseLen = pulseLen

class TurnoutOutput(PulsedOutput):
	def __init__(self, name, pulselen):
		PulsedOutput.__init__(self, name, pulselen)
		self.normal = False;
		self.reverse = False;
		self.normalPulses = 0;
		self.reversePulses = 0;

	def SetOutPulse(self, nv):
		if nv > 0:
			self.normalPulses = self.pulseLen
			self.reversePulses = 0
		elif nv < 0:
			self.normalPulses = 0
			self.reversePulses = -self.pulseLen
		else:
			self.normalPulses = 0
			self.reversePulses = 0

	def GetOutPulse(self):
		if self.normalPulses > 0:
			self.normalPulses -= 1
			return 1
		elif self.reversePulses > 0:
			self.reversePulses -= 1
			return -1
		else:
			return 0