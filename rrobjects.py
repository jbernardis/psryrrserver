class Input:
	def __init__(self, name):
		self.name = name
		self.value = 0

	def SetRailRoad(self, rr):
		self.rr = rr

	def SetDistrict(self, d):
		self.district = d

	def GetName(self):
		return self.name

	def SetValue(self, v):
		self.value = v

	def GetValue(self):
		return self.value

class RouteInput(Input):
	def __init__(self, name):
		Input.__init__(self, name)

	def SetValue(self, nv):
		if nv == self.value:
			return
		print("setting turnouts based on route %s" % self.name)
		self.value = nv
		if nv == 1:
			self.district.MapRouteToTurnouts(self.name)

class BlockInput(Input):
	def __init__(self, name):
		Input.__init__(self, name)

	def SetValue(self, nv):
		if nv == self.value:
			return
		print("setting block value to %d" % nv)
		self.rr.RailroadEvent({"block": [{ "name": self.name, "state": nv}]})
		self.value = nv

class TurnoutInput(Input):
	def __init__(self, name):
		Input.__init__(self, name)
		self.state = "N"  # assume normal switch position to start

	def SetState(self, nb, rb):
		if nb != 0 and rb == 0:
			ns = 'N'
		elif rb != 0 and nb == 0:
			ns = 'R'
		else:
			# erroneous case - just assume normal
			ns = 'N'
		self.SetState(ns)

	def SetState(self, ns):
		if ns == self.state:
			return
		print("setting turnout state to %s" % ns)
		self.rr.RailroadEvent({"turnout": [{ "name": self.name, "state": ns}]})
		self.state = ns

	def GetState(self):
		return self.state

class Output:
	def __init__(self, name):
		self.name = name
		self.value = 0
		self.objName = type(self).__name__

	def SetRailRoad(self, rr):
		self.rr = rr

	def GetName(self):
		return self.name

class IndicatorOutput(Output):
	def __init__(self, name):
		Output.__init__(self, name)
		self.status = False

	def SetStatus(self, flag=True):
		if self.status != flag:
			self.status = flag

	def GetStatus(self):
		return self.status

class HandSwitchOutput(IndicatorOutput):
	def __init__(self, name):
		IndicatorOutput.__init__(self, name)

class RelayOutput(IndicatorOutput):
	def __init__(self, name):
		IndicatorOutput.__init__(self, name)

class SignalOutput(Output):
	def __init__(self, name):
		Output.__init__(self, name)
		self.aspect = 0

	def SetAspect(self, aspect):
		if aspect != self.aspect:
			self.aspect = aspect

		return True

	def IsAspectNonZero(self):
		return self.aspect != 0

	def GetAspect(self):
		return self.aspect

	def GetAspectBit(self, abit):
		mask = (1 << abit) & 0xff
		rv = mask & self.aspect
		return 1 if rv != 0 else 0

class PulsedOutput(Output):
	def __init__(self, name, pulseLen=1):
		Output.__init__(self, name)
		self.pulseLen = pulseLen

	def SetPulseLen(self, pulseLen):
		self.pulseLen = pulseLen

class TurnoutOutput(PulsedOutput):
	def __init__(self, name, pulseLen=1):
		PulsedOutput.__init__(self, name, pulseLen)
		self.normal = False;
		self.reverse = False;
		self.normalPulses = 0;
		self.reversePulses = 0;
		self.locked = False
		self.status = None

	def GetStatus(self):
		return self.status

	def SetLock(self, value):
		self.locked = value != 0

	def GetLock(self):
		return self.locked

	def SetOutPulse(self, status):
		if status == "N":
			self.normalPulses = self.pulseLen
			self.reversePulses = 0
			self.status = status
		elif status == "R":
			self.normalPulses = 0
			self.reversePulses = self.pulseLen
			self.status = status
		else:
			self.normalPulses = 0
			self.reversePulses = 0
			self.status = None

	def GetOutPulseValue(self):
		if self.normalPulses > 0:
			return self.normalPulses
		elif self.reversePulses > 0:
			return -self.reversePulses
		else:
			return 0

	def GetOutPulse(self):
		if self.normalPulses > 0:
			self.normalPulses -= 1
			self.rr.RailroadEvent({"refreshturnout": [{ "name": self.name, "normal": self.normalPulses}]})
			return 1
		elif self.reversePulses > 0:
			self.reversePulses -= 1
			self.rr.RailroadEvent({"refreshturnout": [{ "name": self.name, "reverse": self.reversePulses}]})
			return -1
		else:
			return 0