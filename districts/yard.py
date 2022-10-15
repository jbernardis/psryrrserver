import threading
import time

from district import District, CORNELL, EASTJCT, KALE, YARD, YARDSW
from rrobjects import Output, SignalOutput, TurnoutOutput, PulsedOutput, RelayOutput, IndicatorOutput
from bus import setBit

class Yard(District):
	def __init__(self, parent, name):
		District.__init__(self, parent, name)

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
                    "YSw17", "YSw19", "YSw21", "YSw23", "YSw25", "YSw27", "YSw29", "YSw33",
                    "YSw113", "YSw115", "YSw116", "YSw131", "YSw132", "YSw134" ])
		relayNames = sorted([ "Y11.srel", "Y20.srel", "Y21.srel", "L10.srel" ])
		indNames = sorted([ "CBKale", "CBEastEnd", "CBCornell", "CBEngineYard", "CBWaterman" ])

		ix = 0
		ix = self.AddOutputs(sigNames, SignalOutput, District.signal, ix)
		ix = self.AddOutputs(toNames, TurnoutOutput, District.turnout, ix)
		ix = self.AddOutputs(relayNames, RelayOutput, District.relay, ix)
		ix = self.AddOutputs(indNames, IndicatorOutput, District.indicator, ix)

		for n in toNames:
			self.SetTurnoutPulseLen(n, 2)

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

		if not self.verbose:
			print("Yard:Cornell Jct: Output bytes: {0:08b}  {1:08b}".format(outb[0], outb[1]))

		# inb, inbc = self.rrbus.sendRecv(CORNELL, outb, 2, swap=True)
		# if inb is None:
		# 	if self.verbose:
		# 		print("No data received from Yard:Cornell Jct")
		# 	return

		# if self.verbose:
		# 	print("Yard:Cornell Jct: Input bytes: {0:08b}  {1:08b}".format(inb[0], inb[1], inb[2]))


#    		YSw1.NI = CJIn[0].bit.b0;	//Switch positions
#    		YSw1.RI = CJIn[0].bit.b1;
#    		YSw3.NI = CJIn[0].bit.b2;
# 		YSw3.RI = CJIn[0].bit.b3;
#    		Y21.W  = CJIn[0].bit.b4;	//Detection
#    		Y21.M  = CJIn[0].bit.b5;
#  		Y21.E  = CJIn[0].bit.b6;
#    		CJOS1  = CJIn[0].bit.b7;

#    		CJOS2  = CJIn[1].bit.b0;
#    		L10.W  = CJIn[1].bit.b1;
#    		L10.M  = CJIn[1].bit.b2;


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

		if not self.verbose:
			print("Yard:East Jct: Output bytes: {0:08b}  {1:08b}".format(outb[0], outb[1]))

		# inb, inbc = self.rrbus.sendRecv(EASTJCT, outb, 2, swap=True)
		# if inb is None:
		# 	if self.verbose:
		# 		print("No data received from Yard:East Jct")
		# 	return

		# if self.verbose:
		# 	print("Yard:East Jct: Input bytes: {0:08b}  {1:08b}".format(inb[0], inb[1], inb[2]))


#    		YSw7.NI  = EJIn[0].bit.b0;		//Switch positions
#    		YSw7.RI  = EJIn[0].bit.b1;
#    		YSw9.NI  = EJIn[0].bit.b2;
#    		YSw9.RI  = EJIn[0].bit.b3;
#    		YSw11.NI = EJIn[0].bit.b4;
#    		YSw11.RI = EJIn[0].bit.b5;
#    		Y20.M = EJIn[0].bit.b6;			//Detection
#    		Y20.E = EJIn[0].bit.b7;

#    		EJOS1 = EJIn[1].bit.b0;
#    		EJOS2 = EJIn[1].bit.b1;
#    		Y11.W = EJIn[1].bit.b2;
#    		Y11.M = EJIn[1].bit.b3;



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

		if not self.verbose:
			print("Yard:Kale: Output bytes: {0:08b}  {1:08b}  {2:08b}  {3:08b}".format(outb[0], outb[1], outb[2], outb[3]))

		# inb, inbc = self.rrbus.sendRecv(KALE, outb, 4, swap=True)
		# if inb is None:
		# 	if self.verbose:
		# 		print("No data received from Yard:Kale")
		# 	return

		# if self.verbose:
		# 	print("Yard:Kale: Input bytes: {0:08b}  {1:08b}".format(inb[0], inb[1], inb[2]))


#     	YSw17.NI = KAIn[0].bit.b0;		//Switch positions
#     	YSw17.RI = KAIn[0].bit.b1;
#     	YSw19.NI = KAIn[0].bit.b2;
#     	YSw19.RI = KAIn[0].bit.b3;
#     	YSw21.NI = KAIn[0].bit.b4;
#     	YSw21.RI = KAIn[0].bit.b5;
#     	YSw23.NI = KAIn[0].bit.b6;
#     	YSw23.RI = KAIn[0].bit.b7;

#     	YSw25.NI = KAIn[1].bit.b0;
#     	YSw25.RI = KAIn[1].bit.b1;
#     	YSw27.NI = KAIn[1].bit.b2;
#     	YSw27.RI = KAIn[1].bit.b3;
#     	YSw29.NI = KAIn[1].bit.b4;
#     	YSw29.RI = KAIn[1].bit.b5;
#     	Y30.M = KAIn[1].bit.b6;       //Detection
#     	KAOS1 = KAIn[1].bit.b7;

#     	Y53.M = KAIn[2].bit.b0;
#     	Y52.M = KAIn[2].bit.b1;
#     	Y51.M = KAIn[2].bit.b2;
#     	Y50.M = KAIn[2].bit.b3;
#     	KAOS3 = KAIn[2].bit.b4;
#     	KAOS4 = KAIn[2].bit.b5;
#     	KAOS2 = KAIn[2].bit.b6;
#     	Y10.M = KAIn[2].bit.b7;





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

		print("signal levers 2:%s 4:%s 8:%s 10:%s 22:%s 24:%s 26:%s 34:%s" % (sigL2, sigL4, sigL8, sigL10, sigL22, sigL24, sigL26, sigL34))

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

		if not self.verbose:
			print("Yard:Yard: Output bytes: {0:08b}  {1:08b}  {2:08b}  {3:08b}  {4:08b}  {5:08b}".format(outb[0], outb[1], outb[2], outb[3], outb[4], outb[5]))

		# inb, inbc = self.rrbus.sendRecv(YARD, outb, 6, swap=True)
		# if inb is None:
		# 	if self.verbose:
		# 		print("No data received from Yard:Yard")
		# 	return

		# if self.verbose:
		# 	print("Yard:Yard: Input bytes: {0:08b}  {1:08b}".format(inb[0], inb[1], inb[2]))



#     if(Match)
#     {
#     	YSw33.NI = YDIn[0].bit.b0;		//Switch position
# 		YSw33.RI = YDIn[0].bit.b1;

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
# 		Y81W = YDIn[3].bit.b3;
# 		Y82W = YDIn[3].bit.b4;
# 		Y83W = YDIn[3].bit.b5;
# 		Y84W = YDIn[3].bit.b6;
# 		Y81E = YDIn[3].bit.b7;

# 		Y82E = YDIn[4].bit.b0;
# 		Y83E = YDIn[4].bit.b1;
# 		Y84E = YDIn[4].bit.b2;
# 		Y70.M = YDIn[4].bit.b3;         //Waterman detection
# 		WOS1 = YDIn[4].bit.b4;
# 	//	Y81.M = YDIn[4].bit.b5;
# 		Y82.M = YDIn[4].bit.b6;         //bad bit
# 		Y83.M = YDIn[4].bit.b7;

# 		Y84.M = YDIn[5].bit.b0;
# 		WOS2 = YDIn[5].bit.b1;
# 		Y87.M = YDIn[5].bit.b2;
# 		Y81.M = YDIn[5].bit.b3;
# 		// = YDIn[5].bit.b4;
# 		// = YDIn[5].bit.b5;
# 		// = YDIn[5].bit.b6;
# 		// = YDIn[5].bit.b7;
# 	}













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











		# outb = [0 for i in range(5)]
		# op = self.rr.GetOutput("HSw1").GetOutPulse()
		# outb[0] = setBit(outb[0], 0, 1 if op > 0 else 0)                   # switches
		# outb[0] = setBit(outb[0], 1, 1 if op < 0 else 0)
		
		# outb[3] = setBit(outb[3], 2, self.rr.GetOutput("H30.ind").GetStatus())        # block indicators
		# outb[3] = setBit(outb[3], 3, self.rr.GetOutput("H10.ind").GetStatus())
		# outb[3] = setBit(outb[3], 4, self.rr.GetOutput("H23.ind").GetStatus())
		# outb[3] = setBit(outb[3], 5, self.rr.GetOutput("N25.ind").GetStatus())
		# outb[3] = setBit(outb[3], 6, self.rr.GetOutput("H21.srel").GetStatus())	      # Stop relays
		# outb[3] = setBit(outb[3], 7, self.rr.GetOutput("H31.srel").GetStatus())

		# outb[4] = setBit(outb[4], 0, self.rr.GetOutput("CBHydeJct").GetStatus())      #Circuit breakers
		# outb[4] = setBit(outb[4], 1, self.rr.GetOutput("CBHydeWest").GetStatus()) 
		# outb[4] = setBit(outb[4], 2, self.rr.GetOutput("CBHydeEast").GetStatus()) 
		# outb[4] = setBit(outb[4], 3, self.rr.GetOutput("HydeWestPower").GetStatus())  #Power Control
		# outb[4] = setBit(outb[4], 4, self.rr.GetOutput("HydeEastPower").GetStatus()) 
