import logging

from district import District
from rrobjects import SignalOutput, TurnoutOutput, HandSwitchOutput, RelayOutput, IndicatorOutput, BreakerInput, BlockInput, TurnoutInput
from bus import setBit, getBit


class Port(District):
	def __init__(self, parent, name, settings):
		District.__init__(self, parent, name, settings)

		sigNames =  [ "PB14R", "PB12R", "PB14L", "PB12L" ]
		toNames = [ "PBSw11", "PBSw13" ]
		hsNames = [ "PBSw5", "PBSw15a", "PBSw15b" ]
		handswitchNames = [ "PBSw5.hand", "PBSw15a.hand", "PBSw15b.hand" ]
		relayNames = [ "P31.srel", "P41.srel", "L32.srel", "P42.srel" ]

		ix = 0
		ix = self.AddOutputs(sigNames, SignalOutput, District.signal, ix)
		ix = self.AddOutputs(toNames, TurnoutOutput, District.turnout, ix)
		ix = self.AddOutputs(handswitchNames, HandSwitchOutput, District.handswitch, ix)
		ix = self.AddOutputs(relayNames, RelayOutput, District.relay, ix)

		for n in toNames:
			self.SetTurnoutPulseLen(n, 2)

		blockNames = [ "P31.W", "P31", "P31.E", "P41.W", "P41", "P41.E", "P32.W", "P32", "P32.E", "P42.W", "P42", "P42.E",
						"POSCJ1", "POSCJ2", ]

		ix = 0
		ix = self.AddInputs(blockNames, BlockInput, District.block, ix)
		ix = self.AddInputs(toNames+hsNames, TurnoutInput, District.turnout, ix)

	def OutIn(self):
		pass
		#  PBOS3 = POSCJ2
		#  PBOS4 = POSCJ1