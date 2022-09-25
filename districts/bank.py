import threading
import time

from district import District
from rrobjects import Output, SignalOutput, TurnoutOutput, PulsedOutput, RelayOutput, IndicatorOutput
from bus import setBit



class Bank(District):
	def __init__(self, name, address, rr, rrbus):
		District.__init__(self, name, address, rr, rrbus)

		# signals
		for sigName in [ "C18RA", "C18RB", "C18L", "C22R", "C22L", "C24R", "C24L" ]:
			self.rr.AddOutput(sigName, SignalOutput(sigName))

		# indicators
		for indName in [ "CBBank", "B10", "C13", "CSw19", "CSw21" ]:
			self.rr.AddOutput(indName, IndicatorOutput(indName))

		# turnouts
		for toName in [ "CSw17", "CSw23" ]:
			self.rr.AddOutput(toName, TurnoutOutput(toName, 1))

		# stopping relays
		for relayName in [ "B11", "B20", "B21" ]:
			self.rr.AddOutput(relayName, RelayOutput(relayName))
		self.verbose = self.rr.verbose

	def OutIn(self):
		outb = [0 for i in range(4)]
		outb[0] = setBit(outb[0], 0, self.rr.GetOutput("C22R").GetAspect(0))     # signal aspects
		outb[0] = setBit(outb[0], 1, self.rr.GetOutput("C24R").GetAspect(0))
		outb[0] = setBit(outb[0], 2, self.rr.GetOutput("C24R").GetAspect(1))
		outb[0] = setBit(outb[0], 3, self.rr.GetOutput("C24R").GetAspect(2))
		outb[0] = setBit(outb[0], 4, self.rr.GetOutput("C24L").GetAspect(0))
		outb[0] = setBit(outb[0], 5, self.rr.GetOutput("C24L").GetAspect(1))
		outb[0] = setBit(outb[0], 6, self.rr.GetOutput("C24L").GetAspect(2))
		outb[0] = setBit(outb[0], 7, self.rr.GetOutput("C22L").GetAspect(0))

		outb[1] = setBit(outb[1], 0, self.rr.GetOutput("C22L").GetAspect(1))
		outb[1] = setBit(outb[1], 1, self.rr.GetOutput("C22L").GetAspect(2))
		outb[1] = setBit(outb[1], 2, self.rr.GetOutput("C18RA").GetAspect(0))
		outb[1] = setBit(outb[1], 3, self.rr.GetOutput("C18RB").GetAspect(0))
		outb[1] = setBit(outb[1], 4, self.rr.GetOutput("C18RB").GetAspect(1))
		outb[1] = setBit(outb[1], 5, self.rr.GetOutput("C18RB").GetAspect(2))
		outb[1] = setBit(outb[1], 6, self.rr.GetOutput("C18L").GetAspect(0))
		outb[1] = setBit(outb[1], 7, self.rr.GetOutput("C18L").GetAspect(1))

		outb[2] = setBit(outb[2], 0, self.rr.GetOutput("C18L").GetAspect(2))
		outb[2] = setBit(outb[2], 1, self.rr.GetOutput("B10").GetStatus())         # block indicators
		outb[2] = setBit(outb[2], 2, self.rr.GetOutput("C13").GetStatus())
		outb[2] = setBit(outb[2], 3, self.rr.GetOutput("CSw21").GetStatus())        # hand thrown switches
		outb[2] = setBit(outb[2], 4, self.rr.GetOutput("CSw19").GetStatus())
		op = self.rr.GetOutput("CSw23").GetOutPulse()
		outb[2] = setBit(outb[2], 5, 1 if op > 0 else 0)                   # switches
		outb[2] = setBit(outb[2], 6, 1 if op < 0 else 0)
		op = self.rr.GetOutput("CSw17").GetOutPulse()
		outb[2] = setBit(outb[2], 7, 1 if op > 0 else 0)

		outb[3] = setBit(outb[3], 0, 1 if op < 0 else 0)
		outb[3] = setBit(outb[3], 1, self.rr.GetOutput("B20").GetStatus())	        # Stop relays
		outb[3] = setBit(outb[3], 2, self.rr.GetOutput("B11").GetStatus())
		outb[3] = setBit(outb[3], 3, self.rr.GetOutput("B21").GetStatus())
		outb[3] = setBit(outb[3], 4, self.rr.GetOutput("CBBank").GetStatus())          # panel indicators
		outb[3] = setBit(outb[3], 5, self.rr.GetOutput("C24L").IsAspectNonZero());		    #   Signal 24L indicator

		if self.verbose:
			print("BankIO: Output bytes: {0:08b}  {1:08b}  {2:08b}  {3:08b}".format(outb[0], outb[1], outb[2], outb[3]))

		inb, inbc = self.rrbus.sendRecv(self.address, outb, 4, swap=True)
		if inb is None:
			print("No data received from Bank")
			return
		if self.verbose:
			print("BankIO: Input bytes: {0:08b}  {1:08b}  {2:08b}  {3:08b}".format(inb[0], inb[1], inb[2], inb[3]))

		self.rr.setSwitchPosition("CSw23",  inb[0], 0x01, 0x02)   # Switch positions
		self.rr.setSwitchPosition("CSw21A", inb[0], 0x04, 0x08)
		self.rr.setSwitchPosition("CSw21B", inb[0], 0x10, 0x20)
		self.rr.setSwitchPosition("CSw19",  inb[0], 0x40, 0x80)

		self.rr.setSwitchPosition("CSw17",  inb[1], 0x01, 0x02)
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

