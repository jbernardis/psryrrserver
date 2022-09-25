import threading
import time

from district import District
from rrobjects import Output, SignalOutput, TurnoutOutput, PulsedOutput, RelayOutput, IndicatorOutput
from bus import setBit



class Hyde(District):
	def __init__(self, name, address, rr, rrbus):
		District.__init__(self, name, address, rr, rrbus)

		# Turnouts
		for toName in [ "HSw1", "HSw3", "HSw7", "HSw9", "HSw11", "HSw15", "HSw17", "HSw19", "HSw21", "HSw23", "HSw25", "HSw27", "HSw29" ]:
			self.rr.AddOutput(toName, TurnoutOutput(toName, 1))

		# indicators
		for indName in [ "CBHydeJct", "CBHydeEast", "CBHydeWest", "HydeEastPower", "HydeWestPower", "H30.ind", "H10.ind", "H23.ind", "N25.ind" ]:
			self.rr.AddOutput(indName, IndicatorOutput(indName))

		# stopping relays
		for relayName in [ "H21.srel", "H31.srel" ]:
			self.rr.AddOutput(relayName, RelayOutput(relayName))
		self.verbose = self.rr.verbose

	def OutIn(self):
		outb = [0 for i in range(5)]
		op = self.rr.GetOutput("HSw1").GetOutPulse()
		outb[0] = setBit(outb[0], 0, 1 if op > 0 else 0)                   # switches
		outb[0] = setBit(outb[0], 1, 1 if op < 0 else 0)
		op = self.rr.GetOutput("HSw3").GetOutPulse()
		outb[0] = setBit(outb[0], 2, 1 if op > 0 else 0)           
		outb[0] = setBit(outb[0], 3, 1 if op < 0 else 0)
		op = self.rr.GetOutput("HSw7").GetOutPulse()
		outb[0] = setBit(outb[0], 4, 1 if op > 0 else 0)           
		outb[0] = setBit(outb[0], 5, 1 if op < 0 else 0)
		op = self.rr.GetOutput("HSw9").GetOutPulse()
		outb[0] = setBit(outb[0], 6, 1 if op > 0 else 0)           
		outb[0] = setBit(outb[0], 7, 1 if op < 0 else 0)

		op = self.rr.GetOutput("HSw11").GetOutPulse()
		outb[1] = setBit(outb[1], 0, 1 if op > 0 else 0)
		outb[1] = setBit(outb[1], 1, 1 if op < 0 else 0)
		op = self.rr.GetOutput("HSw23").GetOutPulse()
		outb[1] = setBit(outb[1], 2, 1 if op > 0 else 0)           
		outb[1] = setBit(outb[1], 3, 1 if op < 0 else 0)
		op = self.rr.GetOutput("HSw25").GetOutPulse()
		outb[1] = setBit(outb[1], 4, 1 if op > 0 else 0)           
		outb[1] = setBit(outb[1], 5, 1 if op < 0 else 0)
		op = self.rr.GetOutput("HSw27").GetOutPulse()
		outb[1] = setBit(outb[1], 6, 1 if op > 0 else 0)           
		outb[1] = setBit(outb[1], 7, 1 if op < 0 else 0)

		op = self.rr.GetOutput("HSw29").GetOutPulse()
		outb[2] = setBit(outb[2], 0, 1 if op > 0 else 0)
		outb[2] = setBit(outb[2], 1, 1 if op < 0 else 0)
		op = self.rr.GetOutput("HSw15").GetOutPulse()
		outb[2] = setBit(outb[2], 2, 1 if op > 0 else 0)           
		outb[2] = setBit(outb[2], 3, 1 if op < 0 else 0)
		op = self.rr.GetOutput("HSw17").GetOutPulse()
		outb[2] = setBit(outb[2], 4, 1 if op > 0 else 0)           
		outb[2] = setBit(outb[2], 5, 1 if op < 0 else 0)
		op = self.rr.GetOutput("HSw19").GetOutPulse()
		outb[2] = setBit(outb[2], 6, 1 if op > 0 else 0)           
		outb[2] = setBit(outb[2], 7, 1 if op < 0 else 0)

		op = self.rr.GetOutput("HSw21").GetOutPulse()
		outb[3] = setBit(outb[3], 0, 1 if op > 0 else 0)
		outb[3] = setBit(outb[3], 1, 1 if op < 0 else 0)
		outb[3] = setBit(outb[3], 2, self.rr.GetOutput("H30.ind").GetStatus())        # block indicators
		outb[3] = setBit(outb[3], 3, self.rr.GetOutput("H10.ind").GetStatus())
		outb[3] = setBit(outb[3], 4, self.rr.GetOutput("H23.ind").GetStatus())
		outb[3] = setBit(outb[3], 5, self.rr.GetOutput("N25.ind").GetStatus())
		outb[3] = setBit(outb[3], 6, self.rr.GetOutput("H21.srel").GetStatus())	      # Stop relays
		outb[3] = setBit(outb[3], 7, self.rr.GetOutput("H31.srel").GetStatus())

		outb[4] = setBit(outb[4], 0, self.rr.GetOutput("CBHydeJct").GetStatus())      #Circuit breakers
		outb[4] = setBit(outb[4], 1, self.rr.GetOutput("CBHydeWest").GetStatus()) 
		outb[4] = setBit(outb[4], 2, self.rr.GetOutput("CBHydeEast").GetStatus()) 
		outb[4] = setBit(outb[4], 3, self.rr.GetOutput("HydeWestPower").GetStatus())  #Power Control
		outb[4] = setBit(outb[4], 4, self.rr.GetOutput("HydeEastPower").GetStatus()) 

		if self.verbose:
			print("HydeIO: Output bytes: {0:08b}  {1:08b}  {2:08b}  {3:08b}".format(outb[0], outb[1], outb[2], outb[3], outb[4]))

		inb, inbc = self.rrbus.sendRecv(self.address, outb, 5, swap=True)
		if inb is None:
			print("No data received from Hyde")
			return
		if self.verbose:
			print("HydeIO: Input bytes: {0:08b}  {1:08b}  {2:08b}  {3:08b}".format(inb[0], inb[1], inb[2], inb[3], inb[4]))

	# HOut[0].bit.b0 = HSw1.NO;			//Switch outputs
	# HOut[0].bit.b1 = HSw1.RO;
	# HOut[0].bit.b2 = HSw3.NO;
	# HOut[0].bit.b3 = HSw3.RO;
	# HOut[0].bit.b4 = HSw7.NO;
	# HOut[0].bit.b5 = HSw7.RO;
	# HOut[0].bit.b6 = HSw9.NO;
	# HOut[0].bit.b7 = HSw9.RO;

	# HOut[1].bit.b0 = HSw11.NO;
	# HOut[1].bit.b1 = HSw11.RO;
	# HOut[1].bit.b2 = HSw23.NO;
	# HOut[1].bit.b3 = HSw23.RO;
	# HOut[1].bit.b4 = HSw25.NO;
	# HOut[1].bit.b5 = HSw25.RO;
	# HOut[1].bit.b6 = HSw27.NO;
	# HOut[1].bit.b7 = HSw27.RO;

	# HOut[2].bit.b0 = HSw29.NO;
	# HOut[2].bit.b1 = HSw29.RO;
	# HOut[2].bit.b2 = HSw15.NO;
	# HOut[2].bit.b3 = HSw15.RO;
	# HOut[2].bit.b4 = HSw17.NO;
	# HOut[2].bit.b5 = HSw17.RO;
	# HOut[2].bit.b6 = HSw19.NO;
	# HOut[2].bit.b7 = HSw19.RO;

	# HOut[3].bit.b0 = HSw21.NO;
	# HOut[3].bit.b1 = HSw21.RO;
	# HOut[3].bit.b2 = H30.Blk;		//Block indicators
	# HOut[3].bit.b3 = H10.Blk;
	# HOut[3].bit.b4 = H23.Blk;
	# HOut[3].bit.b5 = N25.Blk;
	# HOut[3].bit.b6 = H21.Srel;		//Stopping relays
	# HOut[3].bit.b7 = H13.Srel;

	# HOut[4].bit.b0 = CBHydeJct;	//Circuit breakers
	# HOut[4].bit.b1 = CBHydeWest;
	# HOut[4].bit.b2 = CBHydeEast;
	# HOut[4].bit.b3 = HydeWestPower;		//Power control
	# HOut[4].bit.b4 = HydeEastPower;


		# H12W = HIn[0].bit.b0;	//Switch positions
		# H34W = HIn[0].bit.b1;
		# H33W = HIn[0].bit.b2;
		# H30E = HIn[0].bit.b3;
		# H31W = HIn[0].bit.b4;
		# H32W = HIn[0].bit.b5;
		# H22W = HIn[0].bit.b6;
		# H43W = HIn[0].bit.b7;

		# H42W = HIn[1].bit.b0;
		# H41W = HIn[1].bit.b1;
		# H41E = HIn[1].bit.b2;
		# H42E = HIn[1].bit.b3;
		# H43E = HIn[1].bit.b4;
		# H22E = HIn[1].bit.b5;
		# H40E = HIn[1].bit.b6;
		# H12E = HIn[1].bit.b7;

		# H34E = HIn[2].bit.b0;
		# H33E = HIn[2].bit.b1;
		# H32E = HIn[2].bit.b2;
		# H31E = HIn[2].bit.b3;
		# H21.M = HIn[2].bit.b4;		//Detection
		# H21.E = HIn[2].bit.b5;
		# HOS4  = HIn[2].bit.b6;
		# HOS5  = HIn[2].bit.b7;

		# HOS6  = HIn[3].bit.b0;
		# H31.M = HIn[3].bit.b1;
		# H32.M = HIn[3].bit.b2;
		# H33.M = HIn[3].bit.b3;
		# H34.M = HIn[3].bit.b4;
		# H12.M = HIn[3].bit.b5;
		# H22.M = HIn[3].bit.b6;
		# H43.M = HIn[3].bit.b7;

		# H42.M = HIn[4].bit.b0;
		# H41.M = HIn[4].bit.b1;
		# H40.M = HIn[4].bit.b2;
		# HOS7  = HIn[4].bit.b3;
		# HOS8  = HIn[4].bit.b4;
		# H13.W = HIn[4].bit.b5;
		# H13.M = HIn[4].bit.b6;

