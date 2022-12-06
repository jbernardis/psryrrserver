import logging

from district import District
from rrobjects import SignalOutput, TurnoutOutput, HandSwitchOutput, RelayOutput, IndicatorOutput, BreakerInput, BlockInput, TurnoutInput
from bus import setBit, getBit


class Port(District):
	def __init__(self, parent, name, settings):
		District.__init__(self, parent, name, settings)

		sigNames = [ "PA12R", "PA12LA", "PA12LB", "PS12LC", "PA10RA", "PA10RB", "PA10L",
					"PA8R", "PA8L", "PA6R", "PA6LA", "PA6LB", "PA6LC", "PA4RA", "PA4RB", "PA4L",
					"PA34RA", "PA34RB", "PS34RC", "PA34RD", "PA34LA", "PA34LB", "PA32RA", "PA32RB", "PA32L",
					"PB2R", "PB2L", "PB4R", "PB4L", "PB12R", "PB12L", "PB14R", "PB14L" ]
		toNames = [ "PBSw1", "PBSw3", "PBSw11", "PBSw13",
					"PASw1", "PASw3", "PASw5", "PASw7", "PASw9", "PASw11", "PASw13",
					"PASw15", "PASw17", "PASw19", "PASw21", "PASw23",
					"PASw27", "PASw29", "PASw31", "PASw33", "PASw35", "PASw37"]
		hsNames = [ "PBSw5", "PBSw15a", "PBSw15b" ]
		handswitchNames = [ "PBSw5.hand", "PBSw15a.hand", "PBSw15b.hand" ]
		relayNames = [ "P10.srel", "P11.srel", "P20.srel", "P21.srel",
					"P30.srel", "P31.srel", "P32.srel", "P40.srel", "P41.srel", "P42.srel" ]

		ix = 0
		ix = self.AddOutputs(sigNames, SignalOutput, District.signal, ix)
		ix = self.AddOutputs(toNames, TurnoutOutput, District.turnout, ix)
		ix = self.AddOutputs(handswitchNames, HandSwitchOutput, District.handswitch, ix)
		ix = self.AddOutputs(relayNames, RelayOutput, District.relay, ix)

		for n in toNames:
			self.SetTurnoutPulseLen(n, 2)

		blockNames = [ "P1", "P2", "P3", "P4", "P5", "P6", "P7",
						"P10", "P10.E", "P11.W", "P11", "P11.E", "P20", "P20.E", "P21", "P21.E",
						"P30.W", "P30", "P30.E", "P31.W", "P31", "P31.E", "P32.W", "P32", "P32.E",
						"P40", "P40.E", "P41.W", "P41", "P41.E", "P42.W", "P42", "P42.E", "P50.W", "P50", "P50.E",
						"P60", "P61", "P62", "P63", "P64", "V10", "V11",
						"POSCJ1", "POSCJ2", "POSSJ1", "POSSJ2", "POSPJ1", "POSPJ2",
						"POSSP1", "POSSP2", "POSSP3", "POSSP4", "POSSP5" ]

		ix = 0
		ix = self.AddInputs(blockNames, BlockInput, District.block, ix)
		ix = self.AddInputs(toNames+hsNames, TurnoutInput, District.turnout, ix)

	def OutIn(self):
		pass
		#  PBOS3 = POSCJ2
		#  PBOS4 = POSCJ1
		#  PBOS2 = POSSJ1
		#  PBOS1 = POSSJ2
		#  PJOS1 = POSPJ1
		#  PJOS2 = POSPJ2
