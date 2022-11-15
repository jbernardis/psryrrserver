import logging

from district import District, LATHAM
from rrobjects import SignalOutput, TurnoutOutput, NXButtonOutput, HandSwitchOutput, IndicatorOutput, BreakerInput, BlockInput, TurnoutInput
from bus import setBit, getBit

class Cliff(District):
	def __init__(self, parent, name, settings):
		District.__init__(self, parent, name, settings)

		sigNames =  [
			"C4R", "C4LA", "C4LB", "C4LC", "C4LD",
		]
		toNames = [ "CSw37", "CSw39", "CSw41" ]
		hsNames = [ "CSw3" ]
		handswitchNames = [ "CSw3.hand" ]

		self.NXMap = {
			"CG21W":  [ ["CSw41", "R"] ],
			"CC10W":  [ ["CSw41", "N"], ["CSw39", "N"] ],
			"CC30W":  [ ["CSw41", "N"], ["CSw39", "R"], ["CSw37", "R"] ],
			"CC31W":  [ ["CSw41", "N"], ["CSw39", "R"], ["CSw37", "N"] ],
		}
		ix = 0
		nxButtons = [ "CG21W", "CC10W", "CC30W", "CC31W" ]

		ix = self.AddOutputs(sigNames, SignalOutput, District.signal, ix)
		ix = self.AddOutputs(nxButtons, NXButtonOutput, District.nxbutton, ix)
		ix = self.AddOutputs(handswitchNames, HandSwitchOutput, District.handswitch, ix)

		for n in nxButtons:
			self.SetNXButtonPulseLen(n, 2)

		blockNames = [ "G21", "C10", "C30", "C31", "COSGMW" ]

		ix = 0
		ix = self.AddInputs(blockNames, BlockInput, District.block, ix)
		ix = self.AddInputs(toNames+hsNames, TurnoutInput, District.turnout, ix)

	def EvaluateNXButton(self, btn):
		if btn not in self.NXMap:
			return

		tolist = self.NXMap[btn]

		for toName, status in tolist:
			print("%s: %s" % (toName, status))
			self.rr.GetInput(toName).SetState(status)

	def OutIn(self):
		#Cliff GM West
		outb = [0 for i in range(8)]

		for bn in self.NXMap.keys():
			self.rr.GetOutput(bn).GetOutPulse()

