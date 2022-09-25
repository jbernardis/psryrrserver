import threading
import time

from districts.bank import Bank
from districts.hyde import Hyde

# tower addresses
YARD      = 0x11;
KALE      = 0x12;
EASTJCT   = 0x13;
CORNELL   = 0x14;
YARDSW    = 0x15;
PARSONS   = 0x21;
PORTA     = 0x22;
PORTB     = 0x23;
LATHAM    = 0x31;
CARLTON   = 0x32;
DELL      = 0x41;
FOSS      = 0x42;
HYDEJCT   = 0x51;
HYDE      = 0x52;
SHORE     = 0x61;
KRULISH   = 0x71;
NASSAUW   = 0x72;
NASSAUE   = 0x73;
NASSAUNX  = 0x74;
BANK      = 0x81;
CLIVEDEN  = 0x91;
GREENMTN  = 0x92;
CLIFF     = 0x93;
SHEFFIELD = 0x95;



class Railroad(threading.Thread):
	def __init__(self, rrbus, eventQ, pollInterval=1): #0.25):
		threading.Thread.__init__(self)
		self.rrbus = rrbus
		self.eventQ = eventQ

		self.verbose = False
		self.pollInterval = pollInterval * 1000000000 # convert s to ns
		self.isRunning = False

		districtList = [
			[ "bank", BANK, Bank ],
			[ "hyde", HYDE, Hyde ],
		]

		self.districts = []
		self.outputs = {}
		self.inputs = {}
		for dname, daddr, dclass in districtList:
			self.districts.append(dclass(dname, daddr, self, self.rrbus))

	def AddOutput(self, name, output):
		self.outputs[name] = output

	def GetOutputs(self):
		return self.outputs

	def AddInput(self, name, input):
		self.inputs[name] = input

	def GetInputs(self):
		return self.inputs

	def setVerbose(self, flag=True):
		self.verbose = flag

	# def setSignalAspect(self, signm, aspv=1):
	# 	try:
	# 		sig = self.signals[signm]
	# 	except KeyError:
	# 		print("SetSignalAspect: No definition for signal %s" % signm)
	# 		return False

	# 	return sig.setAspect(aspv)

	# def setSwitchOutPulse(self, swnm, nv=1):
	# 	try:
	# 		sw = self.switches[swnm]
	# 	except KeyError:
	# 		print("SetSwitchNormalLever: No definition for switch %s" % swnm)
	# 		return False

	# 	return sw.setOutPulse(nv)

	# def setBlockIndicator(self, blknm, flag=True):
	# 	try:
	# 		blk = self.blocks[blknm]
	# 	except KeyError:
	# 		print("SetBlockIndicator: No definition for block %s" % blknm)
	# 		return False

	# 	return blk.setIndicator(flag)

	# def setStoppingRelay(self, srnm, flag=True):
	# 	try:
	# 		sr = self.relays[srnm]
	# 	except KeyError:
	# 		print("SetStoppingRelay: No definition for stopping relay %s" % srnm)
	# 		return False

	# 	return sr.setStatus(flag)

	def kill(self):
		self.isRunning = False

	# everything below this point is running in thread context

	def railroadEvent(self, msg):
		print("Reporting change: (%s)" % str(msg))
		self.eventQ.put(msg)

	def run(self):
		self.isRunning = True
		lastPoll = time.monotonic_ns() - self.pollInterval
		while self.isRunning:
			current = time.monotonic_ns()
			elapsed = current - lastPoll
			if self.isRunning and elapsed > self.pollInterval:
				self.allIO()
				lastPoll = current
			else:
				time.sleep(0.001)

	def GetOutput(self, oTag):
		try:
			return self.outputs[oTag]
		except KeyError:
			print("No output found for tag \"%s\"" % oTag)
			return None

	def GetInput(self, iTag):
		try:
			return self.inputs[iTag]
		except KeyError:
			print("No input found for tag \"%s\"" % iTag)
			return None

	# # these next methoda are for obtaining information from inbound messages
	# def setSwitchPosition(self, swnm, ibyte, maskn, maskr):
	# 	try:
	# 		sw = self.switches[swnm]
	# 	except KeyError:
	# 		print("setSwitchPosition: no switch definition for %s" % swnm)
	# 		return

	# 	spn = 1 if (ibyte & maskn) != 0 else 0		
	# 	spr = 1 if (ibyte & maskr) != 0 else 0
	# 	if spn == 1:
	# 		sp = 1
	# 	elif spr == 1:
	# 		sp = -1
	# 	else:
	# 		sp = 0
	# 	sw.setPosition(sp)

	# finally the IO methods themselves
	def allIO(self):
		for d in self.districts:
			d.OutIn()

