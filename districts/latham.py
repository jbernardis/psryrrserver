import threading
import time

from district import District, LATHAM
from rrobjects import SignalOutput, TurnoutOutput, HandSwitchOutput
from bus import setBit

class Latham(District):
	def __init__(self, parent, name):
		District.__init__(self, parent, name)

		sigNames =  sorted([ "L4R", "L4L",
						"L6RA", "L6RB", "L6L",
						"L8R", "L8L",
						"L14R", "L14L",
						"L16R",
						"L18R", "L18L" ])
		toNames = sorted([ "LSw1", "LSw3", "LSw5", "LSw7", "LSw9", "LSw15", "LSw17" ]) 
		handswitchNames = sorted([ "LSw11.hand", "LSw13.hand" ]) 

		ix = 0
		ix = self.AddOutputs(sigNames, SignalOutput, District.signal, ix)
		ix = self.AddOutputs(toNames, TurnoutOutput, District.turnout, ix)
		ix = self.AddOutputs(handswitchNames, HandSwitchOutput, District.handswitch, ix)

		for n in toNames:
			self.SetTurnoutPulseLen(n, 2)

	def OutIn(self):
		print("Latham out-in")
