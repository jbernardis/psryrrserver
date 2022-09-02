import threading
import time

from signal import Signal
from block import Block
from switch import Switch
from indicator import Indicator
from stoppingrelay import StoppingRelay

sigNames = [
	"C18RA", "C18RB", "C18L", "C22R", "C22L", "C24R", "C24L",		# Bank
	]
blkNames = [
	"B10", "C13",													# Bank
	]
swNames = [
	"CSw17", "CSw19", "CSw21", "CSw23",								# Bank
	]

relayNames = [
	"B11", "B20", "B21",                                            # Bank
]

indicatorNames = [
	"CBBank", "C24L",                                               # Bank
]

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

def set_bit(obyte, obit, val):
	if val != 0:
		return (obyte | (1 << obit)) & 0xff
	else:
		return obyte

class Railroad(threading.Thread):
	def __init__(self, rrbus, eventQ, pollInterval=0.25):
		threading.Thread.__init__(self)
		self.rrbus = rrbus
		self.eventQ = eventQ

		self.signals = { sn: Signal(self, sn) for sn in sigNames }
		self.blocks = { bn: Block(self, bn) for bn in blkNames }
		self.switches = { swn: Switch(self, swn) for swn in swNames }
		self.relays = { srn: StoppingRelay(self, srn) for srn in relayNames }
		self.indicators = { indn: Indicator(self, indn) for indn in indicatorNames }

		self.verbose = False
		self.pollInterval = pollInterval * 1000000000 # convert s to ns
		self.isRunning = False

	def setVerbose(self, flag=True):
		self.verbose = flag

	def setSignalAspect(self, signm, aspv=1):
		try:
			sig = self.signals[signm]
		except KeyError:
			print("SetSignalAspect: No definition for signal %s" % signm)
			return False

		return sig.setAspect(aspv)

	def setSwitchOutPulse(self, swnm, nv=1):
		try:
			sw = self.switches[swnm]
		except KeyError:
			print("SetSwitchNormalLever: No definition for switch %s" % swnm)
			return False

		return sw.setOutPulse(nv)

	def setBlockIndicator(self, blknm, flag=True):
		try:
			blk = self.blocks[blknm]
		except KeyError:
			print("SetBlockIndicator: No definition for block %s" % blknm)
			return False

		return blk.setIndicator(flag)

	def kill(self):
		self.isRunning = False

	# everything below this point is running in thread context

	def railroadEvent(self, name, value):
		print("Reporting change for object (%s) to value (%s)" % (name, str(value)))
		self.eventQ.put({name: value})

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

	# these next methoda are for obtaining information for outbound messages
	def getSignalAspect(self, signm, aspect):
		try:
			sig = self.signals[signm]
		except KeyError:
			print("getSignalAspect: No signal definition for %s" % signm)
			return 0

		return 1 if sig.getAspect(aspect) != 0 else 0
	
	def getBlockIndicator(self, blknm):
		try:
			blk = self.blocks[blknm]
		except KeyError:
			print("getBlockIndicator: no block definition for %s" % blknm)
			return 0
		
		return 1 if blk.getIndicator() else 0

	def getSwitchLocked(self, swnm):
		try:
			sw = self.switches[swnm]
		except KeyError:
			print("getSwitchLocked: no switch definition for %s" % swnm)
			return 0

		return 1 if sw.getLocked() != 0 else 0

	def getSwitchOutPulse(self, swnm):
		try:
			sw = self.switches[swnm]
		except KeyError:
			print("getSwitchOutPulsed: no switch definition for %s" % swnm)
			return 0

		return sw.getOutPulse()

	def getStoppingRelay(self, srnm):
		try:
			sr = self.relays[srnm]
		except KeyError:
			print("getStoppingRelay: no stopping relay definition for %s" % srnm)
			return 0

		return 1 if sr.getStatus() else 0

	def getIndicator(self, indnm):
		try:
			ind = self.indicators[indnm]
		except KeyError:
			print("getIndicator: no indicator definition for %s" % indnm)
			return 0

		return 1 if ind.getStatus() else 0

	# these next methoda are for obtaining information from inbound messages
	def setSwitchPosition(self, swnm, ibyte, maskn, maskr):
		try:
			sw = self.switches[swnm]
		except KeyError:
			print("setSwitchPosition: no switch definition for %s" % swnm)
			return

		spn = 1 if (ibyte & maskn) != 0 else 0		
		spr = 1 if (ibyte & maskr) != 0 else 0
		if spn == 1:
			sp = 1
		elif spr == 1:
			sp = -1
		else:
			sp = 0
		sw.setPosition(sp)

	# finally the IO methods themselves
	def allIO(self):
		self.BankIO()

	def BankIO(self):
		outb = [0 for i in range(4)]
		outb[0] = set_bit(outb[0], 0, self.getSignalAspect("C22R", 0))     # signal aspects
		outb[0] = set_bit(outb[0], 1, self.getSignalAspect("C24R", 0))
		outb[0] = set_bit(outb[0], 2, self.getSignalAspect("C24R", 1))
		outb[0] = set_bit(outb[0], 3, self.getSignalAspect("C24R", 2))
		outb[0] = set_bit(outb[0], 4, self.getSignalAspect("C24L", 0))
		outb[0] = set_bit(outb[0], 5, self.getSignalAspect("C24L", 1))
		outb[0] = set_bit(outb[0], 6, self.getSignalAspect("C24L", 2))
		outb[0] = set_bit(outb[0], 7, self.getSignalAspect("C22L", 0))

		outb[1] = set_bit(outb[1], 0, self.getSignalAspect("C22L", 1))
		outb[1] = set_bit(outb[1], 1, self.getSignalAspect("C22L", 2))
		outb[1] = set_bit(outb[1], 2, self.getSignalAspect("C18RA", 0))
		outb[1] = set_bit(outb[1], 3, self.getSignalAspect("C18RB", 0))
		outb[1] = set_bit(outb[1], 4, self.getSignalAspect("C18RB", 1))
		outb[1] = set_bit(outb[1], 5, self.getSignalAspect("C18RB", 2))
		outb[1] = set_bit(outb[1], 6, self.getSignalAspect("C18L", 0))
		outb[1] = set_bit(outb[1], 7, self.getSignalAspect("C18L", 1))

		outb[2] = set_bit(outb[2], 0, self.getSignalAspect("C18L", 2))
		outb[2] = set_bit(outb[2], 1, self.getBlockIndicator("B10"))         # block indicators
		outb[2] = set_bit(outb[2], 2, self.getBlockIndicator("C13"))
		outb[2] = set_bit(outb[2], 3, self.getSwitchLocked("CSw21"))        # hand thrown switches
		outb[2] = set_bit(outb[2], 4, self.getSwitchLocked("CSw19"))
		op = self.getSwitchOutPulse("CSw23")
		outb[2] = set_bit(outb[2], 5, 1 if op > 0 else 0)                   # switches
		outb[2] = set_bit(outb[2], 6, 1 if op < 0 else 0)
		op = self.getSwitchOutPulse("CSw17")
		outb[2] = set_bit(outb[2], 7, 1 if op > 0 else 0)

		outb[3] = set_bit(outb[3], 0, 1 if op < 0 else 0)
		outb[3] = set_bit(outb[3], 1, self.getStoppingRelay("B20"))	        # Stop relays
		outb[3] = set_bit(outb[3], 2, self.getStoppingRelay("B11"))
		outb[3] = set_bit(outb[3], 3, self.getStoppingRelay("B21"))
		outb[3] = set_bit(outb[3], 4, self.getIndicator("CBBank"))          # panel indicators
		outb[3] = set_bit(outb[3], 5, self.getIndicator("C24L"));		    #   Signal 24L indicator

		if self.verbose:
			print("BankIO: Output bytes: {0:08b}  {1:08b}  {2:08b}  {3:08b}".format(outb[0], outb[1], outb[2], outb[3]))

		inb, inbc = self.rrbus.sendRecv(BANK, outb, 4, swap=True)
		if inb is None:
			print("No data received from Bank")
			return
		if self.verbose:
			print("BankIO: Input bytes: {0:08b}  {1:08b}  {2:08b}  {3:08b}".format(inb[0], inb[1], inb[2], inb[3]))

		self.setSwitchPosition("CSw23",  inb[0], 0x01, 0x02)   # Switch positions
		self.setSwitchPosition("CSw21A", inb[0], 0x04, 0x08)
		self.setSwitchPosition("CSw21B", inb[0], 0x10, 0x20)
		self.setSwitchPosition("CSw19",  inb[0], 0x40, 0x80)

		self.setSwitchPosition("CSw17",  inb[1], 0x01, 0x02)
#//        B20.M    = BKIn[1].bit.b2;		//Detection
#//        B20.E    = BKIn[1].bit.b3;
#//        BKOS1    = BKIn[1].bit.b4;
#//        BKOS2    = BKIn[1].bit.b5;
#//        B11.W    = BKIn[1].bit.b6;
#//        B11.M    = BKIn[1].bit.b7;

#//        B21.W    = BKIn[2].bit.b0;
#//        B21.M    = BKIn[2].bit.b1;
#//        B21.E    = BKIn[2].bit.b2;
#//        BKOS3    = BKIn[2].bit.b3;
#//        CktBkr[9]      = !BKIn[2].bit.b4;	//South	Bank
#//        CktBkr[10]     = !BKIn[2].bit.b5;   //  "		Kale
##//        CktBkr[11]     = !BKIn[2].bit.b6;   //	 "		Waterman
#//        CktBkr[12]     = !BKIn[2].bit.b7;   //  "		Engine Yard

#//        CktBkr[13]		= !BKIn[3].bit.b0;   //  "		East End Jct.
#//        CktBkr[14]     = !BKIn[3].bit.b1;   //  "		Shore
#//        CktBkr[15]     = !BKIn[3].bit.b2;   //	 "		Rocky Hill
#//        CktBkr[16]     = !BKIn[3].bit.b3;   //  "		Harper's Ferry
#//        CktBkr[17]     = !BKIn[3].bit.b4;   //  "		Block Y30
#//        CktBkr[18]     = !BKIn[3].bit.b5;   //	 "		Block Y81

#//        CSw21.NI = CSw21A.NI && CSw21B.NI;
#//        CSw21.RI = CSw21A.RI || CSw21B.RI;

