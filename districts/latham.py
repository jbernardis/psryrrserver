import logging

from district import District, LATHAM
from rrobjects import SignalOutput, TurnoutOutput, HandSwitchOutput, RelayOutput, IndicatorOutput, BreakerInput, BlockInput, TurnoutInput
from bus import setBit, getBit

class Latham(District):
	def __init__(self, parent, name, settings):
		District.__init__(self, parent, name, settings)

		sigNames =  sorted([ "L4R", "L4L",
						"L6RA", "L6RB", "L6L",
						"L8R", "L8L",
						"L14R", "L14L",
						"L16R",
						"L18R", "L18L",
						"S21E", "N20W", "S11E", "N10W" ])
		toNames = sorted([ "LSw1", "LSw3", "LSw5", "LSw7", "LSw9", "LSw15", "LSw17" ]) 
		handswitchNames = sorted([ "LSw11.hand", "LSw13.hand" ]) 
		relayNames = sorted([ "L11.srel", "L20.srel", "L21.srel", "P21.srel", "P50.srel", "L31.srel", "D10.srel", "S21.srel", "N25.srel" ])
		indNames = sorted([ "L10.ind", "L31.ind", "P11.ind" ])

		ix = 0
		ix = self.AddOutputs(sigNames, SignalOutput, District.signal, ix)
		ix = self.AddOutputs(toNames, TurnoutOutput, District.turnout, ix)
		ix = self.AddOutputs(handswitchNames, HandSwitchOutput, District.handswitch, ix)
		ix = self.AddOutputs(indNames, IndicatorOutput, District.indicator, ix)
		ix = self.AddOutputs(relayNames, RelayOutput, District.relay, ix)

		for n in toNames:
			self.SetTurnoutPulseLen(n, 2)

		brkrNames = sorted([ "CBCliveden", 	"CBLatham",  "CBCornellJct", "CBParsonsJct", "CBSouthJct", "CBCircusJct", "CBSouthport",
						"CBLavinYard", "CBReverserP31", "CBReverserP41", "CBReverserP50", "CBReverserC22C23" ])
		blockNames = sorted([ "L20", "L20.E", "LOSLAW", "LOSLAM", "LOSLAE", "L11.W", "L11", "L21.W", "L21", "L21.E",
						"L31", "LOSCAE", "LOSCAM", "LOSCAW", "D10", "D20", "P21", "P21.E" ])

		ix = 0
		ix = self.AddInputs(blockNames, BlockInput, District.block, ix)
		ix = self.AddInputs(toNames, TurnoutInput, District.turnout, ix)
		ix = self.AddInputs(brkrNames, BreakerInput, District.breaker, ix)

	def OutIn(self):
		#Latham
		outb = [0 for i in range(5)]
		op = self.rr.GetOutput("LSw1").GetOutPulse()
		outb[0] = setBit(outb[0], 0, 1 if op > 0 else 0)                   # switches
		outb[0] = setBit(outb[0], 1, 1 if op < 0 else 0)
		op = self.rr.GetOutput("LSw3").GetOutPulse()
		outb[2] = setBit(outb[2], 2, 1 if op > 0 else 0)    #output bit 0:2 is bad - using 2:2              
		outb[0] = setBit(outb[0], 3, 1 if op < 0 else 0)
		op = self.rr.GetOutput("LSw5").GetOutPulse()
		outb[0] = setBit(outb[0], 4, 1 if op > 0 else 0) 
		outb[0] = setBit(outb[0], 5, 1 if op < 0 else 0)
		op = self.rr.GetOutput("LSw7").GetOutPulse()
		outb[0] = setBit(outb[0], 6, 1 if op > 0 else 0) 
		outb[0] = setBit(outb[0], 7, 1 if op < 0 else 0)

		op = self.rr.GetOutput("LSw9").GetOutPulse()
		outb[1] = setBit(outb[1], 0, 1 if op > 0 else 0) 
		outb[1] = setBit(outb[1], 1, 1 if op < 0 else 0)
		asp = self.rr.GetOutput("L4R").GetAspect()
		outb[1] = setBit(outb[1], 2, 1 if asp in [1, 3, 5, 7] else 0)  # signals
		outb[1] = setBit(outb[1], 3, 1 if asp in [2, 3, 6, 7] else 0)
		outb[1] = setBit(outb[1], 4, 1 if asp in [4, 5, 6, 7] else 0)
		asp = self.rr.GetOutput("L6RB").GetAspect()
		outb[1] = setBit(outb[1], 5, 1 if asp != 0 else 0) 
		asp = self.rr.GetOutput("L6RA").GetAspect()
		outb[1] = setBit(outb[1], 6, 1 if asp in [1, 3, 5, 7] else 0)  # signals
		outb[1] = setBit(outb[1], 7, 1 if asp in [2, 3, 6, 7] else 0)

		outb[2] = setBit(outb[2], 0, 1 if asp in [4, 5, 6, 7] else 0)
		asp = self.rr.GetOutput("L8R").GetAspect()
		outb[2] = setBit(outb[2], 1, 1 if asp != 0 else 0) 
		# bit 2:2 is used above for LSw3
		# bit 2:3 is unused
		asp = self.rr.GetOutput("L4L").GetAspect()
		outb[2] = setBit(outb[2], 4, 1 if asp != 0 else 0) 
		asp = self.rr.GetOutput("L6L").GetAspect()
		outb[2] = setBit(outb[2], 5, 1 if asp in [1, 3, 5, 7] else 0)  # signals
		outb[2] = setBit(outb[2], 6, 1 if asp in [2, 3, 6, 7] else 0)
		outb[2] = setBit(outb[2], 7, 1 if asp in [4, 5, 6, 7] else 0)

		asp = self.rr.GetOutput("L8L").GetAspect()
		outb[3] = setBit(outb[3], 0, 1 if asp in [1, 3, 5, 7] else 0)  # signals
		outb[3] = setBit(outb[3], 1, 1 if asp in [2, 3, 6, 7] else 0)
		outb[3] = setBit(outb[3], 2, 1 if asp in [4, 5, 6, 7] else 0)
		outb[3] = setBit(outb[3], 3, self.rr.GetOutput("L10.ind").GetStatus())  #block indicators
		outb[3] = setBit(outb[3], 4, self.rr.GetOutput("L31.ind").GetStatus()) 
		outb[3] = setBit(outb[3], 5, self.rr.GetOutput("P11.ind").GetStatus()) 
		outb[3] = setBit(outb[3], 6, self.rr.GetOutput("L20.srel").GetStatus())	# Stop relays
		outb[3] = setBit(outb[3], 7, self.rr.GetOutput("P21.srel").GetStatus())

		outb[4] = setBit(outb[4], 0, self.rr.GetOutput("L11.srel").GetStatus())
		outb[4] = setBit(outb[4], 1, self.rr.GetOutput("L21.srel").GetStatus())
		outb[4] = setBit(outb[4], 2, self.rr.GetOutput("P50.srel").GetStatus())

		logging.debug("Latham:Latham: Output bytes: {0:08b}  {1:08b}  {2:08b}  {3:08b}  {4:08b}".format(outb[0], outb[1], outb[2], outb[3], outb[4]))

		# inb, inbc = self.rrbus.sendRecv(LATHAM, outb, 5, swap=True)
		# if inb is None:
		# 		print("No data received from Latham:Latham")
		# 	return

		# 	print("Latham:Latham: Input bytes: {0:08b}  {1:08b}  {2:08b}  {3:08b}  {4:08b}".format(inb[0], inb[1], inb[2], inb[3], inb[4]))
		inb = []
		inbc = 0
		if inbc == 5:
			nb = getBit(inb[0], 0)  # Switch positions
			rb = getBit(inb[0], 1)
			self.rr.GetInput("LSw1").SetState(nb, rb)
			nb = getBit(inb[0], 2) 
			rb = getBit(inb[0], 3)
			self.rr.GetInput("LSw3").SetState(nb, rb)
			nb = getBit(inb[0], 4) 
			rb = getBit(inb[0], 5)
			self.rr.GetInput("LSw5").SetState(nb, rb)
			nb = getBit(inb[0], 6) 
			rb = getBit(inb[0], 7)
			self.rr.GetInput("LSw7").SetState(nb, rb)

			nb = getBit(inb[1], 0) 
			rb = getBit(inb[1], 1)
			self.rr.GetInput("LSw9").SetState(nb, rb)
			self.rr.GetInput("L20").SetValue(getBit(inb[1], 2))  # Detection
			self.rr.GetInput("L20.E").SetValue(getBit(inb[1], 3))
			self.rr.GetInput("P21").SetValue(getBit(inb[1], 4))
			self.rr.GetInput("P21.E").SetValue(getBit(inb[1], 5))
			self.rr.GetInput("LOSLAW").SetValue(getBit(inb[1], 6)) #LOS1
			self.rr.GetInput("LOSLAM").SetValue(getBit(inb[1], 7)) #LOS2

			self.rr.GetInput("LOSLAE").SetValue(getBit(inb[2], 0)) #LOS3
			self.rr.GetInput("L11.W").SetValue(getBit(inb[2], 1)) 
			self.rr.GetInput("L11").SetValue(getBit(inb[2], 2)) 
			self.rr.GetInput("L21.W").SetValue(getBit(inb[2], 3)) 
			self.rr.GetInput("L21").SetValue(getBit(inb[2], 4)) 
			self.rr.GetInput("L21.E").SetValue(getBit(inb[2], 5)) 
			self.rr.GetInput("CBClivedon").SetValue(getBit(inb[2], 6)) # Breakers
			self.rr.GetInput("CBLatham").SetValue(getBit(inb[2], 7))

			self.rr.GetInput("CBCornellJct").SetValue(getBit(inb[3], 0))
			self.rr.GetInput("CBParsonsJct").SetValue(getBit(inb[3], 1))
			self.rr.GetInput("CBSouthJct").SetValue(getBit(inb[3], 2))
			self.rr.GetInput("CBCircusJct").SetValue(getBit(inb[3], 3))
			self.rr.GetInput("CBSouthport").SetValue(getBit(inb[3], 4))
			self.rr.GetInput("CBLavinYard").SetValue(getBit(inb[3], 5))
			self.rr.GetInput("CBReverserP31").SetValue(getBit(inb[3], 6))
			self.rr.GetInput("CBReverserP41").SetValue(getBit(inb[3], 7))

			self.rr.GetInput("CBReverserP50").SetValue(getBit(inb[4], 0))
			self.rr.GetInput("CBReverserC22C23").SetValue(getBit(inb[4], 1))


		# Carlton (includes Krulish West tracks and signals
		outb = [0 for i in range(5)]
		asp = self.rr.GetOutput("L16R").GetAspect()
		outb[0] = setBit(outb[0], 0, 1 if asp in [1, 3, 5, 7] else 0)  # signals
		outb[0] = setBit(outb[0], 1, 1 if asp in [2, 3, 6, 7] else 0)
		outb[0] = setBit(outb[0], 2, 1 if asp in [4, 5, 6, 7] else 0)
		asp = self.rr.GetOutput("L18R").GetAspect()
		outb[0] = setBit(outb[0], 3, 1 if asp != 0 else 0)  
		asp = self.rr.GetOutput("L14R").GetAspect()
		outb[0] = setBit(outb[0], 4, 1 if asp in [1, 3, 5, 7] else 0) 
		outb[0] = setBit(outb[0], 5, 1 if asp in [2, 3, 6, 7] else 0)
		outb[0] = setBit(outb[0], 6, 1 if asp in [4, 5, 6, 7] else 0)
		asp = self.rr.GetOutput("L14L").GetAspect()
		outb[0] = setBit(outb[0], 7, 1 if asp != 0 else 0)  

		asp = self.rr.GetOutput("L18R").GetAspect()
		outb[1] = setBit(outb[1], 0, 1 if asp in [1, 3, 5, 7] else 0) 
		outb[1] = setBit(outb[1], 1, 1 if asp in [2, 3, 6, 7] else 0)
		outb[1] = setBit(outb[1], 2, 1 if asp in [4, 5, 6, 7] else 0)
		outb[1] = setBit(outb[1], 3, 0 if self.rr.GetOutput("LSw11.hand").GetStatus() != 0 else 1) # hand switch unlocks
		outb[1] = setBit(outb[1], 4, 0 if self.rr.GetOutput("LSw13.hand").GetStatus() != 0 else 1) 
		op = self.rr.GetOutput("LSw15").GetOutPulse()
		outb[1] = setBit(outb[1], 5, 1 if op > 0 else 0) 
		outb[1] = setBit(outb[1], 6, 1 if op < 0 else 0)
		op = self.rr.GetOutput("LSw17").GetOutPulse()
		outb[1] = setBit(outb[1], 7, 1 if op > 0 else 0) 

		outb[2] = setBit(outb[2], 0, 1 if op < 0 else 0)
		outb[2] = setBit(outb[2], 1, self.rr.GetOutput("L31.srel").GetStatus())	# Stop relays
		outb[2] = setBit(outb[2], 2, self.rr.GetOutput("D10.srel").GetStatus())	
		asp = self.rr.GetOutput("S21E").GetAspect()
		outb[2] = setBit(outb[2], 3, 1 if asp in [1, 3, 5, 7] else 0)  # S21/N20 block signals
		outb[2] = setBit(outb[2], 4, 1 if asp in [2, 3, 6, 7] else 0)
		outb[2] = setBit(outb[2], 5, 1 if asp in [4, 5, 6, 7] else 0)
		asp = self.rr.GetOutput("N20W").GetAspect()
		outb[2] = setBit(outb[2], 6, 1 if asp in [1, 3, 5, 7] else 0)
		outb[2] = setBit(outb[2], 7, 1 if asp in [2, 3, 6, 7] else 0)

		outb[3] = setBit(outb[3], 0, 1 if asp in [4, 5, 6, 7] else 0)
		# bits 1, 2, 3 unused
		asp = self.rr.GetOutput("S11E").GetAspect()
		outb[3] = setBit(outb[3], 4, 1 if asp in [1, 3, 5, 7] else 0)  # S11/N10 block signals
		outb[3] = setBit(outb[3], 5, 1 if asp in [2, 3, 6, 7] else 0)
		outb[3] = setBit(outb[3], 6, 1 if asp in [4, 5, 6, 7] else 0)
		asp = self.rr.GetOutput("N10W").GetAspect()
		outb[3] = setBit(outb[3], 7, 1 if asp in [1, 3, 5, 7] else 0)

		outb[4] = setBit(outb[4], 0, 1 if asp in [2, 3, 6, 7] else 0)
		outb[4] = setBit(outb[4], 1, 1 if asp in [4, 5, 6, 7] else 0)
		outb[4] = setBit(outb[4], 2, self.rr.GetOutput("S21.srel").GetStatus())	# Krulish West stopping relays
		outb[4] = setBit(outb[4], 3, self.rr.GetOutput("N25.srel").GetStatus())	

		logging.debug("Latham:Carlton: Output bytes: {0:08b}  {1:08b}  {2:08b}  {3:08b}  {4:08b}".format(outb[0], outb[1], outb[2], outb[3], outb[4]))

		# inb, inbc = self.rrbus.sendRecv(CARLTON, outb, 5, swap=True)
		# if inb is None:
		# 		print("No data received from Latham:Carlton")
		# 	return

		# 	print("Latham:Latham: Input bytes: {0:08b}  {1:08b}  {2:08b}  {3:08b}  {4:08b}".format(inb[0], inb[1], inb[2], inb[3], inb[4]))
		inb = []
		inbc = 0
		if inbc == 5:
			nb = getBit(inb[0], 0)  # Carlton switch positions
			rb = getBit(inb[0], 1)
			self.rr.GetInput("LSw11").SetState(nb, rb)
			nb = getBit(inb[0], 2) 
			rb = getBit(inb[0], 3)
			self.rr.GetInput("LSw13").SetState(nb, rb)
			nb = getBit(inb[0], 4) 
			rb = getBit(inb[0], 5)
			self.rr.GetInput("LSw15").SetState(nb, rb)
			nb = getBit(inb[0], 6) 
			rb = getBit(inb[0], 7)
			self.rr.GetInput("LSw17").SetState(nb, rb)

			self.rr.GetInput("L31").SetValue(getBit(inb[1], 0))  # Carlton Detection
			self.rr.GetInput("L31.E").SetValue(getBit(inb[1], 1)) 
			self.rr.GetInput("LOSCAW").SetValue(getBit(inb[1], 2)) 
			self.rr.GetInput("LOSCAM").SetValue(getBit(inb[1], 3)) 
			self.rr.GetInput("LOSCAE").SetValue(getBit(inb[1], 4)) 
			self.rr.GetInput("D10.W").SetValue(getBit(inb[1], 5)) 
			self.rr.GetInput("D10").SetValue(getBit(inb[1], 6)) 

			self.rr.GetInput("S21.W").SetValue(getBit(inb[2], 0))  # Krulish west Detection
			self.rr.GetInput("S21").SetValue(getBit(inb[2], 1)) 
			self.rr.GetInput("S21.E").SetValue(getBit(inb[2], 2)) 
			self.rr.GetInput("N25.W").SetValue(getBit(inb[2], 3)) 
			self.rr.GetInput("N25").SetValue(getBit(inb[2], 4)) 
			self.rr.GetInput("N25.E").SetValue(getBit(inb[2], 5)) 
