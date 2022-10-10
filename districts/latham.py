import threading
import time

from district import District
from rrobjects import Output, SignalOutput, TurnoutOutput, PulsedOutput, RelayOutput, IndicatorOutput
from bus import setBit

class Latham(District):
	def __init__(self, parent, name, address):
		District.__init__(self, parent, name, address)

		sigNames =  [ "L4R", "L4L",
						"L6RA", "L6RB", "L6L",
						"L8R", "L8L",
						"L14R", "L14L",
						"L16R",
						"L18R", "L18L" ]
		toNames = [ "LSw1", "LSw3", "LSw5", "LSw7", "LSw9", "LSw15", "LSw17" ] 
		indNames = [ "LSw11.ind", "LSw13.ind" ] 

		ix = 0
		ix = self.AddOutputs(sigNames, SignalOutput, District.signal, ix)
		ix = self.AddOutputs(toNames, TurnoutOutput, District.turnout, ix)
		ix = self.AddOutputs(indNames, IndicatorOutput, District.indicator, ix)

		for n in toNames:
			self.SetTurnoutPulseLen(n, 2)

	def OutIn(self):
		print("Latham out-in")
