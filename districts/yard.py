import logging

from district import District, CORNELL, EASTJCT, KALE, YARD, YARDSW
from rrobjects import TurnoutInput, BlockInput, RouteInput, SignalOutput, TurnoutOutput, RelayOutput, IndicatorOutput
from bus import setBit, getBit

class Yard(District):
	def __init__(self, parent, name, settings):
		District.__init__(self, parent, name, settings)

		#OUTPUTS
		sigNames = sorted([
				"Y2L", "Y2R", 
				"Y4L", "Y4RA", "Y4RB",
                "Y8LA", "Y8LB", "Y8LC", "Y8R",
                "Y10L", "Y10R",
                "Y22L", "Y22R",
                "Y24LA", "Y24LB", 
                "Y26LA", "Y26LB", "Y26LC", "Y26R",
                "Y34L", "Y34RA", "Y34RB" ])
		toNames = sorted([ "YSw1", "YSw3",
                    "YSw7", "YSw9", "YSw11",
                    "YSw17", "YSw19", "YSw21", "YSw23", "YSw25", "YSw27", "YSw29", "YSw33"])
		relayNames = sorted([ "Y11.srel", "Y20.srel", "Y21.srel", "L10.srel" ])
		indNames = sorted([ "CBKale", "CBEastEnd", "CBCornell", "CBEngineYard", "CBWaterman" ])

		ix = 0
		ix = self.AddOutputs(sigNames, SignalOutput, District.signal, ix)
		ix = self.AddOutputs(toNames, TurnoutOutput, District.turnout, ix)
		ix = self.AddOutputs(relayNames, RelayOutput, District.relay, ix)
		ix = self.AddOutputs(indNames, IndicatorOutput, District.indicator, ix)

		for n in toNames:
			self.SetTurnoutPulseLen(n, 2)

		# INPUTS (also using toNames from above)
		blockNames = sorted([
			"Y21.W", "Y21", "Y21.E", "YOSCJW", "YOSCJE", "L10.W", "L10",
			"Y20", "Y20.E", "YOSEJW", "YOSEJE", "Y11.W", "Y11",
			"Y30", "YOSKL4", "Y53", "Y52", "Y51", "Y50", "YOSKL3", "YOSKL1", "YOSKL2", "Y10",
			"Y70", "Y87", "Y81", "Y82", "Y83", "Y84", "YOSWYE", "YOSWYW",
		])
		
		routeNames = sorted(["Y81W", "Y82W", "Y83W", "Y84W", "Y81E", "Y82E", "Y83E", "Y84E" ])
		self.routeMap = {
				"Y81W": [ ["YSw113", "N"], ["YSw115","N"], ["YSw116", "N"] ], 
				"Y82W": [ ["YSw113", "N"], ["YSw115","R"], ["YSw116", "R"] ],
				"Y83W": [ ["YSw113", "N"], ["YSw115","R"], ["YSw116", "N"] ],
				"Y84W": [ ["YSw113", "R"], ["YSw115","N"], ["YSw116", "N"] ],
				"Y81E": [ ["YSw131", "N"], ["YSw132","N"], ["YSw134", "N"] ], 
				"Y82E": [ ["YSw131", "R"], ["YSw132","R"], ["YSw134", "N"] ],
				"Y83E": [ ["YSw131", "N"], ["YSw132","R"], ["YSw134", "N"] ],
				"Y84E": [ ["YSw131", "N"], ["YSw132","N"], ["YSw134", "R"] ],
		}

		ix = 0
		ix = self.AddInputs(routeNames, RouteInput, District.route, ix)
		ix = self.AddInputs(blockNames, BlockInput, District.block, ix)
		ix = self.AddInputs(toNames, TurnoutInput, District.turnout, ix)
		
		# add "proxy" inputs for the waterman turnouts.  These will not be addressed directly, but through the  route table
		hiddenToNames = sorted([ "YSw113", "YSw115", "YSw116", "YSw131", "YSw132", "YSw134" ])
		for t in hiddenToNames:
			self.rr.AddInput(TurnoutInput(t, self), self, District.turnout)

	def OutIn(self):
		#Cornell Jct
		outb = [0 for i in range(2)]
		asp = self.rr.GetOutput("Y4L").GetAspect()
		outb[0] = setBit(outb[0], 0, 1 if asp in [1, 3, 5, 7] else 0)
		outb[0] = setBit(outb[0], 1, 1 if asp in [2, 3, 6, 7] else 0)
		outb[0] = setBit(outb[0], 2, 1 if asp in [4, 5, 6, 7] else 0)
		asp = self.rr.GetOutput("Y2L").GetAspect()
		outb[0] = setBit(outb[0], 3, 1 if asp != 0 else 0)
		asp = self.rr.GetOutput("Y2R").GetAspect()
		outb[0] = setBit(outb[0], 4, 1 if asp in [1, 3, 5, 7] else 0)
		outb[0] = setBit(outb[0], 5, 1 if asp in [2, 3, 6, 7] else 0)
		outb[0] = setBit(outb[0], 6, 1 if asp in [4, 5, 6, 7] else 0)
		asp = self.rr.GetOutput("Y4RA").GetAspect()
		outb[0] = setBit(outb[0], 7, 1 if asp in [1, 3, 5, 7] else 0)

		outb[1] = setBit(outb[1], 0, 1 if asp in [2, 3, 6, 7] else 0)
		outb[1] = setBit(outb[1], 1, 1 if asp in [4, 5, 6, 7] else 0)
		asp = self.rr.GetOutput("Y4RB").GetAspect()
		outb[1] = setBit(outb[1], 2, 1 if asp != 0 else 0)
		outb[1] = setBit(outb[1], 3, self.rr.GetOutput("Y21.srel").GetStatus())	      # Stop relays
		outb[1] = setBit(outb[1], 4, self.rr.GetOutput("L10.srel").GetStatus())

		logging.debug("Yard:Cornell Jct: Output bytes: {0:08b}  {1:08b}".format(outb[0], outb[1]))

		# inb, inbc = self.rrbus.sendRecv(CORNELL, outb, 2, swap=True)
		# if inb is None:
		# 		print("No data received from Yard:Cornell Jct")
		# 	return

		# 	print("Yard:Cornell Jct: Input bytes: {0:08b}  {1:08b}".format(inb[0], inb[1], inb[2]))
		inb = []
		inbc = 0
		if inbc == 2:
			ip = self.rr.GetInput("YSw1")  #Switches
			nb = getBit(inb[0], 0)
			rb = getBit(inb[0], 1)
			ip.SetState(nb, rb)
			ip = self.rr.GetInput("YSw3")
			nb = getBit(inb[0], 2)
			rb = getBit(inb[0], 3)
			ip.SetState(nb, rb)
			ip = self.rr.GetInput("Y21.W")  # Block detection
			ip.SetValue(getBit(inb[0], 4))
			ip = self.rr.GetInput("Y21")
			ip.SetValue(getBit(inb[0], 5))
			ip = self.rr.GetInput("Y21.E")
			ip.SetValue(getBit(inb[0], 6))
			ip = self.rr.GetInput("YOSCJW") # CJOS1
			ip.SetValue(getBit(inb[0], 7))

			ip = self.rr.GetInput("YOSCJE") # CJOS2
			ip.SetValue(getBit(inb[1], 0))
			ip = self.rr.GetInput("L10.W")
			ip.SetValue(getBit(inb[1], 1))
			ip = self.rr.GetInput("L10")
			ip.SetValue(getBit(inb[1], 2))

		# East Junction-----------------------------------------------------------------
		outb = [0 for i in range(2)]
		asp = self.rr.GetOutput("Y10L").GetAspect()
		outb[0] = setBit(outb[0], 0, 1 if asp in [1, 3, 5, 7] else 0)
		outb[0] = setBit(outb[0], 1, 1 if asp in [2, 3, 6, 7] else 0)
		outb[0] = setBit(outb[0], 2, 1 if asp in [4, 5, 6, 7] else 0)
		asp = self.rr.GetOutput("Y8LA").GetAspect()
		outb[0] = setBit(outb[0], 3, 1 if asp != 0 else 0)
		asp = self.rr.GetOutput("Y8LB").GetAspect()
		outb[0] = setBit(outb[0], 4, 1 if asp != 0 else 0)
		asp = self.rr.GetOutput("Y8LC").GetAspect()
		outb[0] = setBit(outb[0], 5, 1 if asp != 0 else 0)
		asp = self.rr.GetOutput("Y8R").GetAspect()
		outb[0] = setBit(outb[0], 6, 1 if asp in [1, 3, 5, 7] else 0)
		outb[0] = setBit(outb[0], 7, 1 if asp in [2, 3, 6, 7] else 0)

		outb[1] = setBit(outb[1], 0, 1 if asp in [4, 5, 6, 7] else 0)
		asp = self.rr.GetOutput("Y10R").GetAspect()
		outb[1] = setBit(outb[1], 1, 1 if asp != 0 else 0)
		outb[1] = setBit(outb[1], 2, self.rr.GetOutput("Y20.srel").GetStatus())	      # Stop relays
		outb[1] = setBit(outb[1], 3, self.rr.GetOutput("Y11.srel").GetStatus())

		logging.debug("Yard:East Jct: Output bytes: {0:08b}  {1:08b}".format(outb[0], outb[1]))

		# inb, inbc = self.rrbus.sendRecv(EASTJCT, outb, 2, swap=True)
		# if inb is None:
		# 		print("No data received from Yard:East Jct")
		# 	return

		# 	print("Yard:East Jct: Input bytes: {0:08b}  {1:08b}".format(inb[0], inb[1], inb[2]))

		inb = []
		inbc = 0
		if inbc == 2:
			ip = self.rr.GetInput("YSw7")  #Switch positions
			nb = getBit(inb[0], 0)
			rb = getBit(inb[0], 1)
			ip.SetState(nb, rb)
			ip = self.rr.GetInput("YSw9") 
			nb = getBit(inb[0], 2)
			rb = getBit(inb[0], 3)
			ip.SetState(nb, rb)
			ip = self.rr.GetInput("YSw11")  
			nb = getBit(inb[0], 4)
			rb = getBit(inb[0], 5)
			ip.SetState(nb, rb)
			ip = self.rr.GetInput("Y20")  # Detection
			ip.SetValue(getBit(inb[0], 6))
			ip = self.rr.GetInput("Y20.E") 
			ip.SetValue(getBit(inb[0], 7))

			ip = self.rr.GetInput("YOSEJW")  # EJOS1
			ip.SetValue(getBit(inb[1], 0))
			ip = self.rr.GetInput("YOSEJE")  # EJOS2
			ip.SetValue(getBit(inb[1], 1))
			ip = self.rr.GetInput("Y11.W")
			ip.SetValue(getBit(inb[1], 2))
			ip = self.rr.GetInput("Y11") 
			ip.SetValue(getBit(inb[1], 3))

		# Kale-----------------------------------------------------------------------
		outb = [0 for i in range(4)]
		asp = self.rr.GetOutput("Y22L").GetAspect()
		outb[0] = setBit(outb[0], 0, 1 if asp != 0 else 0)
		asp = self.rr.GetOutput("Y26LA").GetAspect()
		outb[0] = setBit(outb[0], 1, 1 if asp != 0 else 0)
		asp = self.rr.GetOutput("Y26LB").GetAspect()
		outb[0] = setBit(outb[0], 2, 1 if asp != 0 else 0)
		asp = self.rr.GetOutput("Y26LC").GetAspect()
		outb[0] = setBit(outb[0], 3, 1 if asp != 0 else 0)
		asp = self.rr.GetOutput("Y24LA").GetAspect()
		outb[0] = setBit(outb[0], 4, 1 if asp != 0 else 0)
		asp = self.rr.GetOutput("Y24LB").GetAspect()
		outb[0] = setBit(outb[0], 5, 1 if asp != 0 else 0)
#     KAOut[0].bit.b6 = Y20H;
#     KAOut[0].bit.b7 = Y20D;

		asp = self.rr.GetOutput("Y26R").GetAspect()
		outb[1] = setBit(outb[1], 0, 1 if asp != 0 else 0)
#     KAOut[1].bit.b1 = Y22Ra;
#     KAOut[1].bit.b2 = Y22Rb;

		logging.debug("Yard:Kale: Output bytes: {0:08b}  {1:08b}  {2:08b}  {3:08b}".format(outb[0], outb[1], outb[2], outb[3]))

		# inb, inbc = self.rrbus.sendRecv(KALE, outb, 4, swap=True)
		# if inb is None:
		# 		print("No data received from Yard:Kale")
		# 	return

		# 	print("Yard:Kale: Input bytes: {0:08b}  {1:08b}".format(inb[0], inb[1], inb[2]))


		inb = []
		inbc = 0
		if inbc == 4:
			ip = self.rr.GetInput("YSw17")  #Switch positions
			nb = getBit(inb[0], 0)
			rb = getBit(inb[0], 1)
			ip.SetState(nb, rb)
			ip = self.rr.GetInput("YSw19") 
			nb = getBit(inb[0], 2)
			rb = getBit(inb[0], 3)
			ip.SetState(nb, rb)
			ip = self.rr.GetInput("YSw21") 
			nb = getBit(inb[0], 4)
			rb = getBit(inb[0], 5)
			ip.SetState(nb, rb)
			ip = self.rr.GetInput("YSw23") 
			nb = getBit(inb[0], 6)
			rb = getBit(inb[0], 7)
			ip.SetState(nb, rb)

			ip = self.rr.GetInput("YSw25") 
			nb = getBit(inb[1], 0)
			rb = getBit(inb[1], 1)
			ip.SetState(nb, rb)
			ip = self.rr.GetInput("YSw27") 
			nb = getBit(inb[1], 2)
			rb = getBit(inb[1], 3)
			ip.SetState(nb, rb)
			ip = self.rr.GetInput("YSw29") 
			nb = getBit(inb[1], 4)
			rb = getBit(inb[1], 5)
			ip.SetState(nb, rb)
			ip = self.rr.GetInput("Y30") 
			ip.SetValue(getBit(inb[1], 6))   #detection
			ip = self.rr.GetInput("YOSKL4")  # KAOS1
			ip.SetValue(getBit(inb[1], 7)) 

			ip = self.rr.GetInput("Y53") 
			ip.SetValue(getBit(inb[2], 0))
			ip = self.rr.GetInput("Y52") 
			ip.SetValue(getBit(inb[2], 1))
			ip = self.rr.GetInput("Y51") 
			ip.SetValue(getBit(inb[2], 2))
			ip = self.rr.GetInput("Y50") 
			ip.SetValue(getBit(inb[2], 3))
			ip = self.rr.GetInput("YOSKL2")   #KAOS3
			ip.SetValue(getBit(inb[2], 4))
			ip = self.rr.GetInput("YOSKL1")   #KAOS4
			ip.SetValue(getBit(inb[2], 5))
			ip = self.rr.GetInput("YOSKL3")   #KAOS2
			ip.SetValue(getBit(inb[2], 6))
			ip = self.rr.GetInput("Y10") 
			ip.SetValue(getBit(inb[2], 7))

		# Yard-----------------------------------------------------------------------
		outb = [0 for i in range(6)]
		sigL2 = self.DetermineSignalLever(["Y2L"], ["Y2R"])
		outb[0] = setBit(outb[0], 0, 1 if sigL2 == "L" else 0)       # Signal Indicators
		outb[0] = setBit(outb[0], 1, 1 if sigL2 == "N" else 0)
		outb[0] = setBit(outb[0], 2, 1 if sigL2 == "R" else 0)
		sigL4 = self.DetermineSignalLever(["Y4L"], ["Y4RA", "Y4RB"])
		outb[0] = setBit(outb[0], 3, 1 if sigL4 == "L" else 0)    
		outb[0] = setBit(outb[0], 4, 1 if sigL4 == "N" else 0)
		outb[0] = setBit(outb[0], 5, 1 if sigL4 == "R" else 0)
		sigL8 = self.DetermineSignalLever(["Y8LA", "Y8LB", "Y8LC"], ["Y8R"])
		outb[0] = setBit(outb[0], 6, 1 if sigL8 == "L" else 0) 
		outb[0] = setBit(outb[0], 7, 1 if sigL8 == "N" else 0)

		outb[1] = setBit(outb[1], 0, 1 if sigL8 == "R" else 0)
		sigL10 = self.DetermineSignalLever(["Y10L"], ["Y10R"])
		outb[1] = setBit(outb[1], 1, 1 if sigL10 == "L" else 0)    
		outb[1] = setBit(outb[1], 2, 1 if sigL10 == "N" else 0)
		outb[1] = setBit(outb[1], 3, 1 if sigL10 == "R" else 0)
		sigL22 = self.DetermineSignalLever(["Y22L"], ["Y22R"])
		outb[1] = setBit(outb[1], 4, 1 if sigL22 == "L" else 0)    
		outb[1] = setBit(outb[1], 5, 1 if sigL22 == "N" else 0)
		outb[1] = setBit(outb[1], 6, 1 if sigL22 == "R" else 0)
		sigL24 = self.DetermineSignalLever(["Y24LA", "Y24LB"], []) 
		outb[1] = setBit(outb[1], 7, 1 if sigL24 == "L" else 0)    

		outb[2] = setBit(outb[2], 0, 1 if sigL24 == "N" else 0)
		sigL26 = self.DetermineSignalLever(["Y26LA", "Y26LB", "Y26LC"], ["Y26R"])
		outb[2] = setBit(outb[2], 1, 1 if sigL26== "L" else 0)    
		outb[2] = setBit(outb[2], 2, 1 if sigL26 == "N" else 0)
		outb[2] = setBit(outb[2], 3, 1 if sigL26 == "R" else 0)
		sigL34 = self.DetermineSignalLever(["Y34L"], ["Y34RA", "Y34RB"])
		outb[2] = setBit(outb[2], 4, 1 if sigL34== "L" else 0)    
		outb[2] = setBit(outb[2], 5, 1 if sigL34 == "N" else 0)
		outb[2] = setBit(outb[2], 6, 1 if sigL34 == "R" else 0)
		asp = self.rr.GetOutput("Y34RA").GetAspect()
		outb[2] = setBit(outb[2], 7, 1 if asp != 0 else 0)

		asp = self.rr.GetOutput("Y34RB").GetAspect()
		outb[3] = setBit(outb[3], 0, 1 if asp != 0 else 0)
		asp = self.rr.GetOutput("Y34L").GetAspect()
		outb[3] = setBit(outb[3], 1, 1 if asp in [1, 3, 5, 7] else 0)
		outb[3] = setBit(outb[3], 2, 1 if asp in [2, 3, 6, 7] else 0)
		outb[3] = setBit(outb[3], 3, 1 if asp in [4, 5, 6, 7] else 0)
		outb[3] = setBit(outb[3], 4, self.rr.GetOutput("CBKale").GetStatus())      #Circuit breakers
		outb[3] = setBit(outb[3], 5, self.rr.GetOutput("CBEastEnd").GetStatus())
		outb[3] = setBit(outb[3], 6, self.rr.GetOutput("CBCornell").GetStatus())
		outb[3] = setBit(outb[3], 7, self.rr.GetOutput("CBEngineYard").GetStatus()) 

		outb[4] = setBit(outb[4], 0, self.rr.GetOutput("CBWaterman").GetStatus()) 
#     YDOut[4].bit.b1 = L20.Blk;          //Adjacent block indicators
#     YDOut[4].bit.b2 = P50.Blk;
		outb[4] = setBit(outb[4], 3, self.rr.GetOutput("YSw1").GetLock())  # Switch Locks
		outb[4] = setBit(outb[4], 4, self.rr.GetOutput("YSw3").GetLock())  
		outb[4] = setBit(outb[4], 5, self.rr.GetOutput("YSw7").GetLock()) 
		outb[4] = setBit(outb[4], 6, self.rr.GetOutput("YSw9").GetLock()) 
		outb[4] = setBit(outb[4], 7, self.rr.GetOutput("YSw17").GetLock())  

		outb[5] = setBit(outb[5], 0, self.rr.GetOutput("YSw19").GetLock())
		outb[5] = setBit(outb[5], 1, self.rr.GetOutput("YSw21").GetLock())
		outb[5] = setBit(outb[5], 2, self.rr.GetOutput("YSw23").GetLock())
		outb[5] = setBit(outb[5], 3, self.rr.GetOutput("YSw25").GetLock())
		outb[5] = setBit(outb[5], 4, self.rr.GetOutput("YSw29").GetLock())
		outb[5] = setBit(outb[5], 5, self.rr.GetOutput("YSw33").GetLock())

		logging.debug("Yard:Yard: Output bytes: {0:08b}  {1:08b}  {2:08b}  {3:08b}  {4:08b}  {5:08b}".format(outb[0], outb[1], outb[2], outb[3], outb[4], outb[5]))

		# inb, inbc = self.rrbus.sendRecv(YARD, outb, 6, swap=True)
		# if inb is None:
		# 		print("No data received from Yard:Yard")
		# 	return

		# 	print("Yard:Yard: Input bytes: {0:08b}  {1:08b}".format(inb[0], inb[1], inb[2]))


		inb = []
		inbc = 0
		if inbc == 5:
			ip = self.rr.GetInput("YSw33")  #Switch positions
			nb = getBit(inb[0], 0)
			rb = getBit(inb[0], 1)
			ip.SetState(nb, rb)

# 		if(RBYard->Checked)
# 		{
# 			YSigL2.R = YDIn[0].bit.b2;      //Signals
# 			YSigL2.Callon = YDIn[0].bit.b3;
# 			YSigL2.L = YDIn[0].bit.b4;
# 			YSigL4.R = YDIn[0].bit.b5;
# 			YSigL4.Callon = YDIn[0].bit.b6;
# 			YSigL4.L = YDIn[0].bit.b7;

# 			YSigL8.R = YDIn[1].bit.b0;
# 			YSigL8.Callon = YDIn[1].bit.b1;
# 			YSigL8.L = YDIn[1].bit.b2;
# 			YSigL10.R = YDIn[1].bit.b3;
# 			YSigL10.Callon = YDIn[1].bit.b4;
# 			YSigL10.L = YDIn[1].bit.b5;
# 			YSigL22.R = YDIn[1].bit.b6;
# 			YSigL22.Callon = YDIn[1].bit.b7;

# 			YSigL22.L = YDIn[2].bit.b0;
# 			YSigL24.Callon = YDIn[2].bit.b1;
# 			YSigL24.L = YDIn[2].bit.b2;
# 			YSigL26.R = YDIn[2].bit.b3;
# 			YSigL26.Callon = YDIn[2].bit.b4;
# 			YSigL26.L = YDIn[2].bit.b5;
# 			YSigL34.R = YDIn[2].bit.b6;
# 			YSigL34.Callon = YDIn[2].bit.b7;

# 			YSigL34.L = YDIn[3].bit.b0;
# 		}

# 		YRelease = YDIn[3].bit.b1;
# 		WOS1Norm = YDIn[3].bit.b2;      //switches normal for WOS1 into Y70
			self.rr.GetInput("Y81W").SetValue(getBit(inb[3], 3)) 
			self.rr.GetInput("Y82W").SetValue(getBit(inb[3], 4)) 
			self.rr.GetInput("Y83W").SetValue(getBit(inb[3], 5)) 
			self.rr.GetInput("Y84W").SetValue(getBit(inb[3], 6)) 
			self.rr.GetInput("Y81E").SetValue(getBit(inb[3], 7)) 

			self.rr.GetInput("Y82E").SetValue(getBit(inb[4], 0)) 
			self.rr.GetInput("Y83E").SetValue(getBit(inb[4], 1)) 
			self.rr.GetInput("Y84E").SetValue(getBit(inb[4], 2))  
			self.rr.GetInput("Y70").SetValue(getBit(inb[4], 3))   # Waterman detection
			self.rr.GetInput("YOSWYW").SetValue(getBit(inb[4], 4))  # WOS1
			# bit 5 is bad
			self.rr.GetInput("Y82").SetValue(getBit(inb[4], 6))  
			self.rr.GetInput("Y83").SetValue(getBit(inb[4], 7))  

			self.rr.GetInput("Y84").SetValue(getBit(inb[5], 0))  
			self.rr.GetInput("YOSWYE").SetValue(getBit(inb[5], 1))  # WOS2
			self.rr.GetInput("Y87").SetValue(getBit(inb[5], 2))  
			self.rr.GetInput("Y81").SetValue(getBit(inb[5], 3))  

		# Yard and Waterman switch control by dispatcher
		outb = [0 for i in range(5)]
		op = self.rr.GetOutput("YSw1").GetOutPulse()
		outb[0] = setBit(outb[0], 0, 1 if op > 0 else 0)                   # switches
		outb[0] = setBit(outb[0], 1, 1 if op < 0 else 0)
		op = self.rr.GetOutput("YSw3").GetOutPulse()
		outb[0] = setBit(outb[0], 2, 1 if op > 0 else 0)
		outb[0] = setBit(outb[0], 3, 1 if op < 0 else 0)
		op = self.rr.GetOutput("YSw7").GetOutPulse()
		outb[0] = setBit(outb[0], 4, 1 if op > 0 else 0)
		outb[0] = setBit(outb[0], 5, 1 if op < 0 else 0)
		op = self.rr.GetOutput("YSw9").GetOutPulse()
		outb[0] = setBit(outb[0], 6, 1 if op > 0 else 0)
		outb[0] = setBit(outb[0], 7, 1 if op < 0 else 0)

		op = self.rr.GetOutput("YSw11").GetOutPulse()
		outb[1] = setBit(outb[1], 0, 1 if op > 0 else 0)                   # switches
		outb[1] = setBit(outb[1], 1, 1 if op < 0 else 0)
		op = self.rr.GetOutput("YSw17").GetOutPulse()
		outb[1] = setBit(outb[1], 2, 1 if op > 0 else 0)
		outb[1] = setBit(outb[1], 3, 1 if op < 0 else 0)
		op = self.rr.GetOutput("YSw19").GetOutPulse()
		outb[1] = setBit(outb[1], 4, 1 if op > 0 else 0)
		outb[1] = setBit(outb[1], 5, 1 if op < 0 else 0)
		op = self.rr.GetOutput("YSw21").GetOutPulse()
		outb[1] = setBit(outb[1], 6, 1 if op > 0 else 0)
		outb[1] = setBit(outb[1], 7, 1 if op < 0 else 0)

		op = self.rr.GetOutput("YSw23").GetOutPulse()
		outb[2] = setBit(outb[2], 0, 1 if op > 0 else 0)                   # switches
		outb[2] = setBit(outb[2], 1, 1 if op < 0 else 0)
		op = self.rr.GetOutput("YSw25").GetOutPulse()
		outb[2] = setBit(outb[2], 2, 1 if op > 0 else 0)
		outb[2] = setBit(outb[2], 3, 1 if op < 0 else 0)
		op = self.rr.GetOutput("YSw27").GetOutPulse()
		outb[2] = setBit(outb[2], 4, 1 if op > 0 else 0)
		outb[2] = setBit(outb[2], 5, 1 if op < 0 else 0)
		op = self.rr.GetOutput("YSw29").GetOutPulse()
		outb[2] = setBit(outb[2], 6, 1 if op > 0 else 0)
		outb[2] = setBit(outb[2], 7, 1 if op < 0 else 0)

		logging.debug("Yard:Waterman: Output bytes: {0:08b}  {1:08b}  {2:08b}".format(outb[0], outb[1], outb[2]))


# 	YSWOut[3].bit.b0 = SBY51W;
# 	YSWOut[3].bit.b1 = SBY50W;
# //	YSWOut[3].bit.b2 = ;
# //	YSWOut[3].bit.b3 = ;
# //	YSWOut[3].bit.b4 = ;
# //	YSWOut[3].bit.b5 = ;
# //	YSWOut[3].bit.b6 = ;
# //	YSWOut[3].bit.b7 = ;

# 	YSWOut[4].bit.b0 = SBY81W;
# 	YSWOut[4].bit.b1 = SBY82W;
# 	YSWOut[4].bit.b2 = SBY83W;
# 	YSWOut[4].bit.b3 = SBY84W;
# 	YSWOut[4].bit.b4 = SBY81E;
# 	YSWOut[4].bit.b5 = SBY82E;
# 	YSWOut[4].bit.b6 = SBY83E;
# 	YSWOut[4].bit.b7 = SBY84E;

# 	SendPacket(YARDSW, &YardSWAborts, &YSWIn[0], &YSWOld[0], &YSWOut[0], 5, true);
# 	YSWText = "YardSW\t" + OutText;
		# No inputs from this node