import wx

from district import District, HYDE
from rrobjects import Output, SignalOutput, TurnoutOutput, PulsedOutput, RelayOutput, IndicatorOutput, RouteInput, BlockInput
from bus import setBit

class Hyde(District):
	def __init__(self, parent, name):
		District.__init__(self, parent, name)

		# OUTPUTS
		sigNames = [
				"H4LA", "H4LB", "H4LC",  "H4LD",  "H4R", 
				"H6LA", "H6LB", "H6LC", "H6LD", "H6R",  
				"H8L", "H8R",  
				"H10L","H10RA", "H10RB", "H10RC", "H10RD", "H10RE", 
				"H12RA", "H12RB", "H12RC", "H12RD", "H12RE", "H12L"]
		toNames =[ "HSw1", "HSw3", "HSw7", "HSw9", "HSw11", "HSw15", "HSw17", "HSw19", "HSw21", "HSw23", "HSw25", "HSw27", "HSw29" ]
		indNames = [ "CBHydeJct", "CBHydeEast", "CBHydeWest", "HydeEastPower", "HydeWestPower", "H30.ind", "H10.ind", "H23.ind", "N25.ind" ]
		relayNames = [ "H21.srel", "H31.srel" ]

		ix = 0
		ix = self.AddOutputs(sigNames, SignalOutput, District.signal, ix)
		ix = self.AddOutputs(toNames, TurnoutOutput, District.turnout, ix)
		ix = self.AddOutputs(indNames, IndicatorOutput, District.indicator, ix)
		ix = self.AddOutputs(relayNames, RelayOutput, District.relay, ix)

		for n in toNames:
			self.SetTurnoutPulseLen(n, 2)

		# INPUTS
		routeNames = sorted([ "H12W", "H34W", "H33W", "H30E", "H31W", "H32W", "H22W", "H43W",
				"H42W", "H41W", "H41E", "H42E", "H43E", "H22E", "H40E", "H12E",
				"H34E", "H33E", "H32E", "H31E" ])
		self.routeMap = {
				"H12W": [ {"name": "HSw1", "state": "N"}, {"name": "HSw3", "state": "N"} ], 
				"H34W": [ {"name": "HSw1", "state": "N"}, {"name": "HSw3", "state": "R"} ],
				"H33W": [ {"name": "HSw1", "state": "R"}, {"name": "HSw3", "state": "N"}, {"name": "HSw5", "state": "N"} ], 
				"H32W": [ {"name": "HSw1", "state": "R"}, {"name": "HSw3", "state": "R"}, {"name": "HSw5", "state": "R"}, {"name": "HSw7", "state": "N"} ], 
				"H31W": [ {"name": "HSw1", "state": "R"}, {"name": "HSw3", "state": "R"}, {"name": "HSw5", "state": "R"}, {"name": "HSw7", "state": "R"} ], 

				"H12E": [ {"name": "HSw15", "state": "N"}, {"name": "HSw17", "state": "N"}, {"name": "HSw19", "state": "N"}, {"name": "HSw21", "state": "N"} ], 
				"H34E": [ {"name": "HSw15", "state": "R"}, {"name": "HSw17", "state": "N"}, {"name": "HSw19", "state": "N"}, {"name": "HSw21", "state": "N"} ], 
				"H33E": [ {"name": "HSw15", "state": "N"}, {"name": "HSw17", "state": "R"}, {"name": "HSw19", "state": "N"}, {"name": "HSw21", "state": "N"} ], 
				"H32E": [ {"name": "HSw15", "state": "N"}, {"name": "HSw17", "state": "N"}, {"name": "HSw19", "state": "R"}, {"name": "HSw21", "state": "N"} ], 
				"H31E": [ {"name": "HSw15", "state": "N"}, {"name": "HSw17", "state": "N"}, {"name": "HSw19", "state": "N"}, {"name": "HSw21", "state": "R"} ], 
				"H30E": [ {"name": "HSw1", "state": "N"} ],

				"H22W": [ {"name": "HSw9", "state": "N"}, {"name": "HSw11", "state": "N"}, {"name": "HSw13", "state": "N"} ], 
				"H43W": [ {"name": "HSw9", "state": "N"}, {"name": "HSw11", "state": "R"}, {"name": "HSw13", "state": "R"} ], 
				"H42W": [ {"name": "HSw9", "state": "R"}, {"name": "HSw11", "state": "N"}, {"name": "HSw13", "state": "N"} ], 
				"H41W": [ {"name": "HSw9", "state": "R"}, {"name": "HSw11", "state": "R"}, {"name": "HSw13", "state": "R"} ], 

				"H22E": [ {"name": "HSw23", "state": "N"}, {"name": "HSw25", "state": "N"}, {"name": "HSw27", "state": "N"}, {"name": "HSw29", "state": "N"} ], 
				"H43E": [ {"name": "HSw23", "state": "N"}, {"name": "HSw25", "state": "R"}, {"name": "HSw27", "state": "R"}, {"name": "HSw29", "state": "N"} ], 
				"H42E": [ {"name": "HSw23", "state": "R"}, {"name": "HSw25", "state": "N"}, {"name": "HSw27", "state": "R"}, {"name": "HSw29", "state": "N"} ], 
				"H41E": [ {"name": "HSw23", "state": "N"}, {"name": "HSw25", "state": "N"}, {"name": "HSw27", "state": "R"}, {"name": "HSw29", "state": "N"} ], 
				"H40E": [ {"name": "HSw23", "state": "N"}, {"name": "HSw25", "state": "N"}, {"name": "HSw27", "state": "N"}, {"name": "HSw29", "state": "R"} ], 
		}

		blockNames = sorted([ "H21", "H21.E", "H23", "HOSWW2", "HOSWW",
				"HOSWE", "H31", "H33", "H34", "H12", "H22", "H43",
				"H42", "H41", "H40", "HOSEW", "HOSEE", "H13.W", "H13" ])

		ix = 0
		ix = self.AddInputs(routeNames, RouteInput, District.route, ix)
		ix = self.AddInputs(blockNames, BlockInput, District.block, ix)

	def MapRouteToTurnouts(self, rname):
		try:
			return({"turnout": self.routeMap[rname]})
		except Exception as e:
			print("Unknown route name: %s" % rname)
			print(str(e))
			return None

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

		if not self.verbose:
			print("HydeIO: Output bytes: {0:08b}  {1:08b}  {2:08b}  {3:08b}".format(outb[0], outb[1], outb[2], outb[3], outb[4]))

		# inb, inbc = self.rrbus.sendRecv(HYDE, outb, 5, swap=True)
		# if inb is None:
		# 	if self.verbose:
		# 		print("No data received from Hyde")
		# 	return

		# if self.verbose:
		# 	print("HydeIO: Input bytes: {0:08b}  {1:08b}  {2:08b}  {3:08b}".format(inb[0], inb[1], inb[2], inb[3], inb[4]))

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
		# HOSWW2 HOS4  = HIn[2].bit.b6;
		# HOSWW HOS5  = HIn[2].bit.b7;

		# HOSWE HOS6  = HIn[3].bit.b0;
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
		# HOSEW  HOS7  = HIn[4].bit.b3;
		# HOSEE  HOS8  = HIn[4].bit.b4;
		# H13.W = HIn[4].bit.b5;
		# H13.M = HIn[4].bit.b6;

