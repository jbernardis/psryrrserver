import logging

from district import District, DELL
from rrobjects import SignalOutput, TurnoutOutput, HandSwitchOutput, RelayOutput, IndicatorOutput, BreakerInput, BlockInput, TurnoutInput
from bus import setBit, getBit

class Dell(District):
	def __init__(self, parent, name, settings):
		District.__init__(self, parent, name, settings)

		sigNames =  sorted([ "D4RA", "D4RB", "D4L",
						"D6RA", "D6RB", "D6L",
						"DXO", 
						"D10R", "D10L",
						"D12R", "D12L",
						"RXO", "R10W"
						])
		toNames = sorted([ "DSw1", "DSw3", "DSw5", "DSw7", "DSw11" ]) 
		handswitchNames = sorted([ "DSw9.hand" ]) 
		relayNames = sorted([ "D20.srel", "H23.srel", "D11.srel", "D21.srel", "S10.srel", "R10.srel" ])
		indNames = sorted([ "H13.ind", "S20.ind", "D10.ind" ])

		ix = 0
		ix = self.AddOutputs(sigNames, SignalOutput, District.signal, ix)
		ix = self.AddOutputs(toNames, TurnoutOutput, District.turnout, ix)
		ix = self.AddOutputs(handswitchNames, HandSwitchOutput, District.handswitch, ix)
		ix = self.AddOutputs(indNames, IndicatorOutput, District.indicator, ix)
		ix = self.AddOutputs(relayNames, RelayOutput, District.relay, ix)

		for n in toNames:
			self.SetTurnoutPulseLen(n, 2)

		blockNames = sorted([ "D20", "D20.E", "H23", "H23.E", "DOS1", "DOS2", "D11.W", "D11A", "D11B", "D11.E",
							"D21.W", "D21A", "D21B", "D21.E", "MFOS1", "MFOS2", "S10.W", "S10A", "S10B" "S10C",
							"R10.E", "R10A", "R10B", "R10C", "R11", "R12"])

		ix = 0
		ix = self.AddInputs(blockNames, BlockInput, District.block, ix)
		ix = self.AddInputs(toNames, TurnoutInput, District.turnout, ix)

	def OutIn(self):
		#Dell
		outb = [0 for i in range(4)]
		asp = self.rr.GetOutput("D4RA").GetAspect()
		outb[0] = setBit(outb[0], 0, 1 if asp in [1, 3, 5, 7] else 0)  # eastbound signals
		outb[0] = setBit(outb[0], 1, 1 if asp in [2, 3, 6, 7] else 0)
		outb[0] = setBit(outb[0], 2, 1 if asp in [4, 5, 6, 7] else 0)
		asp = self.rr.GetOutput("D4RB").GetAspect()
		outb[0] = setBit(outb[0], 3, 1 if asp in [1, 3, 5, 7] else 0) 
		outb[0] = setBit(outb[0], 4, 1 if asp in [2, 3, 6, 7] else 0)
		outb[0] = setBit(outb[0], 5, 1 if asp in [4, 5, 6, 7] else 0)
		asp = self.rr.GetOutput("D6RA").GetAspect()
		outb[0] = setBit(outb[0], 6, 1 if asp != 0 else 0)
		asp = self.rr.GetOutput("D6RB").GetAspect()
		outb[0] = setBit(outb[0], 7, 1 if asp != 0 else 0)

		asp = self.rr.GetOutput("D4L").GetAspect()
		outb[1] = setBit(outb[1], 0, 1 if asp in [1, 3, 5, 7] else 0)  # westbound signals
		outb[1] = setBit(outb[1], 1, 1 if asp in [2, 3, 6, 7] else 0)
		outb[1] = setBit(outb[1], 2, 1 if asp in [4, 5, 6, 7] else 0)
		asp = self.rr.GetOutput("D6L").GetAspect()
		outb[1] = setBit(outb[1], 3, 1 if asp in [1, 3, 5, 7] else 0) 
		outb[1] = setBit(outb[1], 4, 1 if asp in [2, 3, 6, 7] else 0)
		outb[1] = setBit(outb[1], 5, 1 if asp in [4, 5, 6, 7] else 0)
		asp = self.rr.GetOutput("DXO").GetAspect()
		outb[1] = setBit(outb[1], 6, 1 if asp != 0 else 0) # laporte crossing signal
		outb[1] = setBit(outb[1], 7, self.rr.GetOutput("H13.ind").GetStatus())  #block indicators

		outb[2] = setBit(outb[2], 0, self.rr.GetOutput("D10.ind").GetStatus())
		outb[2] = setBit(outb[2], 1, self.rr.GetOutput("S20.ind").GetStatus())
		outb[2] = setBit(outb[2], 2, 0 if self.rr.GetOutput("DSw9.hand").GetStatus() != 0 else 1) 
		op = self.rr.GetOutput("DSw1").GetOutPulse()
		outb[2] = setBit(outb[2], 3, 1 if op > 0 else 0)                   # switches
		outb[2] = setBit(outb[2], 4, 1 if op < 0 else 0)
		op = self.rr.GetOutput("DSw3").GetOutPulse()
		outb[2] = setBit(outb[2], 5, 1 if op > 0 else 0)
		outb[2] = setBit(outb[2], 6, 1 if op < 0 else 0)
		op = self.rr.GetOutput("DSw5").GetOutPulse()
		outb[2] = setBit(outb[2], 7, 1 if op > 0 else 0) 

		outb[3] = setBit(outb[3], 0, 1 if op < 0 else 0)
		op = self.rr.GetOutput("DSw7").GetOutPulse()
		outb[3] = setBit(outb[3], 1, 1 if op > 0 else 0)
		outb[3] = setBit(outb[3], 2, 1 if op < 0 else 0)
		op = self.rr.GetOutput("DSw11").GetOutPulse()
		outb[3] = setBit(outb[3], 3, 1 if op > 0 else 0)
		outb[3] = setBit(outb[3], 4, 1 if op < 0 else 0)
		outb[3] = setBit(outb[3], 5, self.rr.GetOutput("D20.srel").GetStatus())	# Stop relays
		outb[3] = setBit(outb[3], 6, self.rr.GetOutput("H23.srel").GetStatus())
		outb[3] = setBit(outb[3], 7, self.rr.GetOutput("D11.srel").GetStatus())

		logging.debug("Dell:Dell:: Output bytes: {0:08b}  {1:08b}  {2:08b}  {3:08b}".format(outb[0], outb[1], outb[2], outb[3]))

		# inb, inbc = self.rrbus.sendRecv(DELL, outb, 4, swap=True)
		# if inb is None:
		# 		print("No data received from Latham:Latham")
		# 	return

		# 	print("Latham:Latham: Input bytes: {0:08b}  {1:08b}  {2:08b}  {3:08b}".format(inb[0], inb[1], inb[2], inb[3]))
		inb = []
		inbc = 0
		if inbc == 5:
			nb = getBit(inb[0], 0)  # Switch positions
			rb = getBit(inb[0], 1)
			self.rr.GetInput("DSw1").SetState(nb, rb)
			nb = getBit(inb[0], 2) 
			rb = getBit(inb[0], 3)
			self.rr.GetInput("DSw3").SetState(nb, rb)
			nb = getBit(inb[0], 4) 
			rb = getBit(inb[0], 5)
			self.rr.GetInput("DSw5").SetState(nb, rb)
			nb = getBit(inb[0], 6) 
			rb = getBit(inb[0], 7)
			self.rr.GetInput("DSw7").SetState(nb, rb)

			nb = getBit(inb[1], 0)  
			rb = getBit(inb[1], 1)
			self.rr.GetInput("DSw9").SetState(nb, rb)
			nb = getBit(inb[1], 2)  
			rb = getBit(inb[1], 3)
			self.rr.GetInput("DSw11").SetState(nb, rb)
			self.rr.GetInput("D20").SetValue(getBit(inb[1], 4))  # Detection
			self.rr.GetInput("D20.E").SetValue(getBit(inb[1], 5))
			self.rr.GetInput("H23").SetValue(getBit(inb[1], 6)) 
			self.rr.GetInput("H23.E").SetValue(getBit(inb[1], 7))

			self.rr.GetInput("DOS1").SetValue(getBit(inb[2], 0)) #DOS1
			self.rr.GetInput("DOS2").SetValue(getBit(inb[2], 1)) #DOS2
			self.rr.GetInput("D11.W").SetValue(getBit(inb[2], 2))
			self.rr.GetInput("D11A").SetValue(getBit(inb[2], 3))
			self.rr.GetInput("D11B").SetValue(getBit(inb[2], 4))
			self.rr.GetInput("D11.E").SetValue(getBit(inb[2], 5))

		# Foss
		outb = [0 for i in range(3)]
		asp = self.rr.GetOutput("D10R").GetAspect()
		outb[0] = setBit(outb[0], 0, 1 if asp in [1, 3, 5, 7] else 0)  # eastbound signals
		outb[0] = setBit(outb[0], 1, 1 if asp in [2, 3, 6, 7] else 0)
		outb[0] = setBit(outb[0], 2, 1 if asp in [4, 5, 6, 7] else 0)
		asp = self.rr.GetOutput("D12R").GetAspect()
		outb[0] = setBit(outb[0], 3, 1 if asp in [1, 3, 5, 7] else 0) 
		outb[0] = setBit(outb[0], 4, 1 if asp in [2, 3, 6, 7] else 0)
		outb[0] = setBit(outb[0], 5, 1 if asp in [4, 5, 6, 7] else 0)

		asp = self.rr.GetOutput("D10L").GetAspect()
		outb[1] = setBit(outb[1], 0, 1 if asp in [1, 3, 5, 7] else 0)  # westbound signals
		outb[1] = setBit(outb[1], 1, 1 if asp in [2, 3, 6, 7] else 0)
		outb[1] = setBit(outb[1], 2, 1 if asp in [4, 5, 6, 7] else 0)
		asp = self.rr.GetOutput("D12L").GetAspect()
		outb[1] = setBit(outb[1], 3, 1 if asp in [1, 3, 5, 7] else 0) 
		outb[1] = setBit(outb[1], 4, 1 if asp in [2, 3, 6, 7] else 0)
		outb[1] = setBit(outb[1], 5, 1 if asp in [4, 5, 6, 7] else 0)
		outb[1] = setBit(outb[1], 6, self.rr.GetOutput("D21.srel").GetStatus())	# Stop relays
		outb[1] = setBit(outb[1], 7, self.rr.GetOutput("D21.srel").GetStatus())

		# bit 2:0 is bad
		outb[2] = setBit(outb[2], 1, self.rr.GetOutput("R10.srel").GetStatus())
		asp = self.rr.GetOutput("RXO").GetAspect()
		outb[2] = setBit(outb[2], 2, 1 if asp != 0 else 0)  # rocky hill crossing signal
		asp = self.rr.GetOutput("D10L").GetAspect()
		outb[2] = setBit(outb[2], 3, 1 if asp in [1, 3, 5, 7] else 0)  # rocky hill distant for nassau
		outb[2] = setBit(outb[2], 4, 1 if asp in [2, 3, 6, 7] else 0)
		outb[2] = setBit(outb[2], 5, 1 if asp in [4, 5, 6, 7] else 0)

		logging.debug("Dell:Foss: Output bytes: {0:08b}  {1:08b}  {2:08b}".format(outb[0], outb[1], outb[2]))

		# inb, inbc = self.rrbus.sendRecv(FOSS, outb, 3, swap=True)
		# if inb is None:
		# 		print("No data received from Latham:Latham")
		# 	return

		# 	print("Latham:Latham: Input bytes: {0:08b}  {1:08b}  {2:08b}  {3:08b}".format(inb[0], inb[1], inb[2], inb[3]))
		inb = []
		inbc = 0
		if inbc == 5:
			pass

			self.rr.GetInput("D21.W").SetValue(getBit(inb[0], 0))  # Detection
			self.rr.GetInput("D21A").SetValue(getBit(inb[0], 1))
			self.rr.GetInput("D21B").SetValue(getBit(inb[0], 2))
			self.rr.GetInput("D21.E").SetValue(getBit(inb[0], 3))
			self.rr.GetInput("MFOS1").SetValue(getBit(inb[0], 4)) #MFOS1
			self.rr.GetInput("MFOS2").SetValue(getBit(inb[0], 5)) #MFOS2
			self.rr.GetInput("S10.W").SetValue(getBit(inb[0], 6))
			self.rr.GetInput("S10A").SetValue(getBit(inb[0], 7))

			self.rr.GetInput("S10B").SetValue(getBit(inb[1], 0))
			self.rr.GetInput("S10C").SetValue(getBit(inb[1], 1))
			self.rr.GetInput("S10.E").SetValue(getBit(inb[1], 2))
			self.rr.GetInput("R10.W").SetValue(getBit(inb[1], 3))
			self.rr.GetInput("R10A").SetValue(getBit(inb[1], 4)) 
			self.rr.GetInput("R10B").SetValue(getBit(inb[1], 5)) 
			self.rr.GetInput("R10C").SetValue(getBit(inb[1], 6))
			self.rr.GetInput("R11").SetValue(getBit(inb[1], 7))

			self.rr.GetInput("R12").SetValue(getBit(inb[2], 0))

# 		D21 = D21A || D21B;
# 		S10 = S10A || S10B || S10C;
# 		R10 = R10A || R10B || R10C;
