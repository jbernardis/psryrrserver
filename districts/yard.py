import threading
import time

from district import District
from rrobjects import Output, SignalOutput, TurnoutOutput, PulsedOutput, RelayOutput, IndicatorOutput
from bus import setBit

class Yard(District):
	def __init__(self, parent, name, address):
		District.__init__(self, parent, name, address)

		sigNames = [
				"Y2L", "Y2R", 
				"Y4L", "Y4RA", "Y4RB",
                "Y8LA", "Y8LB", "Y8LC", "Y8R",
                "Y10L", "Y10R",
                "Y22L", "Y22R",
                "Y24LA", "Y24LB", 
                "Y26LA", "Y26LB", "Y26LC", "Y26R",
                "Y34L", "Y34RA", "Y34RB" ]
		toNames = [ "YSw1", "YSw3",
                    "YSw7", "YSw9", "YSw11",
                    "YSw17", "YSw19", "YSw21", "YSw23", "YSw25", "YSw27", "YSw29", "YSw33",
                    "YSw113", "YSw115", "YSw116", "YSw131", "YSw132", "YSw134" ]

		ix = 0
		ix = self.AddOutputs(sigNames, SignalOutput, District.signal, ix)
		ix = self.AddOutputs(toNames, TurnoutOutput, District.turnout, ix)

		for n in toNames:
			self.SetTurnoutPulseLen(n, 2)

	def OutIn(self):
		print("Yard out-in")
