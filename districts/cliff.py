import logging

from district import District
from rrobjects import SignalOutput, NXButtonOutput, HandSwitchOutput, BlockInput, TurnoutInput, RouteInput
from bus import setBit, getBit

class Cliff(District):
	def __init__(self, parent, name, settings):
		District.__init__(self, parent, name, settings)

		sigNames =  [
			"C2RA", "C2RB", "C2RC", "C2RD", "C2L",
			"C4R", "C4LA", "C4LB", "C4LC", "C4LD",
			"C6RA", "C6RB", "C6RC", "C6RD", "C6RE", "C6RF", "C6RG", "C6RH", "C6GJ", "C6RK", "C6RL", "C6L",
			"C8R", "C8LA", "C8LB", "C8LC", "C8LD", "C8LE", "C8LF", "C8LG", "C8LH", "C8LJ", "C8LK", "C8LL",
		]
		toNames = [ "CSw31", "CSw33", "CSw35", "CSw37", "CSw39",
					"CSw41", "CSw43", "CSw45", "CSw47", "CSw49",
					"CSw51", "CSw53", "CSw55", "CSw57", "CSw59",
					"CSw61", "CSw63", "CSw65", "CSw67", "CSw69",
					"CSw71", "CSw73", "CSw75", "CSw77", "CSw79",
					"CSw81"]
		hsNames = [ "CSw3" ]
		handswitchNames = [ "CSw3.hand" ]

		self.routeMap = {
			"CG21W":  [ ["CSw41", "R"] ],
			"CC10W":  [ ["CSw41", "N"], ["CSw39", "N"] ],
			"CC30W":  [ ["CSw41", "N"], ["CSw39", "R"], ["CSw37", "R"] ],
			"CC31W":  [ ["CSw41", "N"], ["CSw39", "R"], ["CSw37", "N"] ],

			"CG12E":  [ ["CSw31", "R"], ["CSw35", "N"] ],
			"CG10E":  [ ["CSw31", "R"], ["CSw35", "R"] ],
			"CC10E":  [ ["CSw31", "N"], ["CSw33", "N"] ],
			"CC30E":  [ ["CSw31", "N"], ["CSw33", "R"] ],

			"CC44E":  [ ["CSw43", "N"], ["CSw49", "N"] ],
			"CC43E":  [ ["CSw43", "N"], ["CSw49", "R"] ],
			"CC42E":  [ ["CSw43", "R"], ["CSw45", "R"], ["CSw51", "N"] ],
			"CC41E":  [ ["CSw43", "R"], ["CSw45", "R"], ["CSw51", "R"] ],
			"CC40E":  [ ["CSw43", "R"], ["CSw45", "N"], ["CSw47", "R"] ],
			"CC21E":  [ ["CSw43", "R"], ["CSw45", "N"], ["CSw47", "N"], ["CSw63", "R"] ],
			"CC50E":  [ ["CSw43", "R"], ["CSw45", "N"], ["CSw47", "N"], ["CSw63", "N"], ["CSw65", "R"] ],
			"CC51E":  [ ["CSw43", "R"], ["CSw45", "N"], ["CSw47", "N"], ["CSw63", "N"], ["CSw65", "N"], ["CSw67", "R"], ["CSw69", "N"] ],
			"CC52E":  [ ["CSw43", "R"], ["CSw45", "N"], ["CSw47", "N"], ["CSw63", "N"], ["CSw65", "N"], ["CSw67", "R"], ["CSw69", "R"] ],
			"CC53E":  [ ["CSw43", "R"], ["CSw45", "N"], ["CSw47", "N"], ["CSw63", "N"], ["CSw65", "N"], ["CSw67", "N"], ["CSw71", "R"] ],
			"CC54E":  [ ["CSw43", "R"], ["CSw45", "N"], ["CSw47", "N"], ["CSw63", "N"], ["CSw65", "N"], ["CSw67", "N"], ["CSw71", "N"] ],

			"CC44W":  [ ["CSw57", "N"], ["CSw59", "N"], ["CSw61", "R"] ],
			"CC43W":  [ ["CSw57", "R"], ["CSw59", "N"], ["CSw61", "R"] ],
			"CC42W":  [ ["CSw53", "R"], ["CSw59", "R"], ["CSw61", "R"] ],
			"CC41W":  [ ["CSw53", "N"], ["CSw59", "R"], ["CSw61", "R"] ],
			"CC40W":  [ ["CSw55", "R"], ["CSw61", "N"] ],
			"CC21W":  [ ["CSw55", "N"], ["CSw61", "N"], ["CSw73", "N"] ],
			"CC50W":  [ ["CSw55", "N"], ["CSw61", "N"], ["CSw73", "R"], ["CSw75", "R"] ],

			"CC51W":  [ ["CSw55", "N"], ["CSw61", "N"], ["CSw73", "R"], ["CSw75", "N"], ["CSw77", "R"], ["CSw79", "N"] ],
			"CC52W":  [ ["CSw55", "N"], ["CSw61", "N"], ["CSw73", "R"], ["CSw75", "N"], ["CSw77", "R"], ["CSw79", "R"] ],
			"CC53W":  [ ["CSw55", "N"], ["CSw61", "N"], ["CSw73", "R"], ["CSw75", "N"], ["CSw77", "N"], ["CSw81", "R"] ],
			"CC54W":  [ ["CSw55", "N"], ["CSw61", "N"], ["CSw73", "R"], ["CSw75", "N"], ["CSw77", "N"], ["CSw81", "N"] ],
		}
		ix = 0
		nxButtons = [
			"CG21W", "CC10W", "CC30W", "CC31W",
			"CG12E", "CG10E", "CC10E", "CC30E",
			"CC44E", "CC43E", "CC42E", "CC41E", "CC40E", "CC21E", "CC50E", "CC51E", "CC52E", "CC53E", "CC54E",
			"CC44W", "CC43W", "CC42W", "CC41W", "CC40W", "CC21W", "CC50W", "CC51W", "CC52W", "CC53W", "CC54W",
		]

		ix = self.AddOutputs(sigNames, SignalOutput, District.signal, ix)
		ix = self.AddOutputs(nxButtons, NXButtonOutput, District.nxbutton, ix)
		ix = self.AddOutputs(handswitchNames, HandSwitchOutput, District.handswitch, ix)

		for n in nxButtons:
			self.SetNXButtonPulseLen(n, 2)

		blockNames = [ "G21", "C10", "C30", "C31", "COSGMW", "G10", "G12", "C20", "COSGME",
					"C44", "C43", "C42", "C41", "C40", "C21", "C50", "C51", "C52", "C53", "C54", "COSSHE", "COSSHW"]

		ix = 0
		# each NX button corresponds to a route
		ix = self.AddInputs(nxButtons, RouteInput, District.route, ix)
		ix = self.AddInputs(blockNames, BlockInput, District.block, ix)
		ix = self.AddInputs(toNames+hsNames, TurnoutInput, District.turnout, ix)

	def EvaluateNXButton(self, btn):
		if btn not in self.routeMap:
			return

		tolist = self.routeMap[btn]

		for toName, status in tolist:
			print("%s: %s" % (toName, status))
			self.rr.GetInput(toName).SetState(status)

	def DetermineSignalLevers(self):
		self.sigLever["C2"] = self.DetermineSignalLever(["C2L"], ["C2RA", "C2RB", "C2RC", "C2RD"])  # signal indicators
		self.sigLever["C4"] = self.DetermineSignalLever(["C4LA", "C4LB", "C4LC", "C4LD"], ["C4R"])
		self.sigLever["C6"] = self.DetermineSignalLever(["C6L"], ["C6RA", "C6RB", "C6RC", "C6RD", "C6RE", "C6RF", "C6RG", "C6RH", "C6GJ", "C6RK", "C6RL"])
		self.sigLever["C8"] = self.DetermineSignalLever(["C8LA", "C8LB", "C8LC", "C8LD", "C8LE", "C8LF", "C8LG", "C8LH", "C8LJ", "C8LK", "C8LL"], ["C8R"])
		self.sigLever["C10"] = self.DetermineSignalLever(["C10L"], ["C10R"])
		self.sigLever["C12"] = self.DetermineSignalLever(["C12L"], ["C12R"])
		self.sigLever["C14"] = self.DetermineSignalLever(["C14LA", "C14LB"], ["C14R"])
		self.sigLever["C18"] = self.DetermineSignalLever(["C18L"], ["C18RA", "C18RB"])
		self.sigLever["C22"] = self.DetermineSignalLever(["C22L"], ["C22R"])
		self.sigLever["C24"] = self.DetermineSignalLever(["C24L"], ["C24R"])

	def OutIn(self):
		# Green Mountain
		outb = [0 for i in range(3)]
		asp = self.rr.GetOutput("C2RB").GetAspect()
		outb[0] = setBit(outb[0], 0, 1 if asp in [1, 3, 5, 7] else 0)  # east end signals
		outb[0] = setBit(outb[0], 1, 1 if asp in [2, 3, 6, 7] else 0)
		outb[0] = setBit(outb[0], 2, 1 if asp in [4, 5, 6, 7] else 0)
		asp = self.rr.GetOutput("C2RD").GetAspect()
		outb[0] = setBit(outb[0], 3, 1 if asp != 0 else 0)
		asp = self.rr.GetOutput("C2L").GetAspect()
		outb[0] = setBit(outb[0], 4, 1 if asp in [1, 3, 5, 7] else 0)
		outb[0] = setBit(outb[0], 5, 1 if asp in [2, 3, 6, 7] else 0)
		outb[0] = setBit(outb[0], 6, 1 if asp in [4, 5, 6, 7] else 0)
		asp = self.rr.GetOutput("C2RA").GetAspect()
		outb[0] = setBit(outb[0], 7, 1 if asp in [1, 3] else 0)

		outb[1] = setBit(outb[1], 0, 1 if asp in [2, 3] else 0)
		asp = self.rr.GetOutput("C2RC").GetAspect()
		outb[1] = setBit(outb[1], 1, 1 if asp != 0 else 0)
		asp = self.rr.GetOutput("C4LA").GetAspect()
		outb[1] = setBit(outb[1], 2, 1 if asp in [1, 3] else 0)	  # west end signals
		outb[1] = setBit(outb[1], 3, 1 if asp in [2, 3] else 0)
		asp = self.rr.GetOutput("C4LB").GetAspect()
		outb[1] = setBit(outb[1], 4, 1 if asp in [1, 3] else 0)
		outb[1] = setBit(outb[1], 5, 1 if asp in [2, 3] else 0)
		asp = self.rr.GetOutput("C4LC").GetAspect()
		outb[1] = setBit(outb[1], 6, 1 if asp in [1, 3, 5, 7] else 0)
		outb[1] = setBit(outb[1], 7, 1 if asp in [2, 3, 6, 7] else 0)

		outb[2] = setBit(outb[2], 0, 1 if asp in [4, 5, 6, 7] else 0)
		asp = self.rr.GetOutput("C4LD").GetAspect()
		outb[2] = setBit(outb[2], 1, 1 if asp != 0 else 0)
		asp = self.rr.GetOutput("C4R").GetAspect()
		outb[2] = setBit(outb[2], 2, 1 if asp in [1, 3, 5, 7] else 0)
		outb[2] = setBit(outb[2], 3, 1 if asp in [2, 3, 6, 7] else 0)
		outb[2] = setBit(outb[2], 4, 1 if asp in [4, 5, 6, 7] else 0)
		outb[2] = setBit(outb[2], 5, 0 if self.rr.GetOutput("CSw3.hand").GetStatus() != 0 else 1)  # hand switch 3

		inb = [0, 0, 0, 0]
		otext = "{0:08b}  {1:08b}  {2:08b}".format(outb[0], outb[1], outb[2])
		itext = "{0:08b}  {1:08b}  {2:08b}".format(inb[0], inb[1], inb[2])
		logging.debug("Cliff:GM: Output bytes: %s" % otext)
		if self.sendIO:
			self.rr.ShowText(otext, itext, 0, 4)

		inb = []
		inbc = 0
		if inbc == 3:
			self.rr.GetInput("CC30E").SetValue(getBit(inb[0], 0))   # Routes
			self.rr.GetInput("CC10E").SetValue(getBit(inb[0], 1))
			self.rr.GetInput("CG10E").SetValue(getBit(inb[0], 2))
			self.rr.GetInput("CG12E").SetValue(getBit(inb[0], 3))
			self.rr.GetInput("CC31W").SetValue(getBit(inb[0], 4))
			self.rr.GetInput("CC30W").SetValue(getBit(inb[0], 5))
			self.rr.GetInput("CC10W").SetValue(getBit(inb[0], 6))
			self.rr.GetInput("CG21W").SetValue(getBit(inb[0], 7))

			nb = getBit(inb[1], 0)  # Switch positions
			rb = getBit(inb[1], 1)
			self.rr.GetInput("CSw3").SetState(nb, rb)
			self.rr.GetInput("C11").SetValue(getBit(inb[1], 2))  # Detection
			self.rr.GetInput("COSGMW").SetValue(getBit(inb[1], 3))  # COS1
			self.rr.GetInput("C10").SetValue(getBit(inb[1], 4))
			self.rr.GetInput("C30").SetValue(getBit(inb[1], 5))
			self.rr.GetInput("C31").SetValue(getBit(inb[1], 6))
			self.rr.GetInput("COSGME").SetValue(getBit(inb[1], 7))  # COS2

			self.rr.GetInput("C20").SetValue(getBit(inb[2], 0))

		# Cliff
		outb = [0 for i in range(8)]
		sigl = self.sigLever["C2"]  # signal indicators
		outb[0] = setBit(outb[0], 0, 1 if sigl == "L" else 0)
		outb[0] = setBit(outb[0], 1, 1 if sigl == "N" else 0)
		outb[0] = setBit(outb[0], 2, 1 if sigl == "R" else 0)
		sigl = self.sigLever["C4"]
		outb[0] = setBit(outb[0], 3, 1 if sigl == "L" else 0)
		outb[0] = setBit(outb[0], 4, 1 if sigl == "N" else 0)
		outb[0] = setBit(outb[0], 5, 1 if sigl == "R" else 0)
		sigl = self.sigLever["C6"]
		outb[0] = setBit(outb[0], 6, 1 if sigl == "L" else 0)
		outb[0] = setBit(outb[0], 7, 1 if sigl == "N" else 0)

		outb[1] = setBit(outb[1], 0, 1 if sigl == "R" else 0)
		sigl = self.sigLever["C8"]
		outb[1] = setBit(outb[1], 1, 1 if sigl == "L" else 0)
		outb[1] = setBit(outb[1], 2, 1 if sigl == "N" else 0)
		outb[1] = setBit(outb[1], 3, 1 if sigl == "R" else 0)
		sigl = self.sigLever["C10"]
		outb[1] = setBit(outb[1], 4, 1 if sigl == "L" else 0)
		outb[1] = setBit(outb[1], 5, 1 if sigl == "N" else 0)
		outb[1] = setBit(outb[1], 6, 1 if sigl == "R" else 0)
		sigl = self.sigLever["C12"]
		outb[1] = setBit(outb[1], 7, 1 if sigl == "L" else 0)

		outb[2] = setBit(outb[2], 0, 1 if sigl == "N" else 0)
		outb[2] = setBit(outb[2], 1, 1 if sigl == "R" else 0)
		sigl = self.sigLever["C14"]
		outb[2] = setBit(outb[2], 2, 1 if sigl == "L" else 0)
		outb[2] = setBit(outb[2], 3, 1 if sigl == "N" else 0)
		outb[2] = setBit(outb[2], 4, 1 if sigl == "R" else 0)
# 	CFOut[2].bit.b5 = !CFltL16.R;	//Fleet indicator
# 	CFOut[2].bit.b6 = CFltL16.R;
		sigl = self.sigLever["C18"]
		outb[2] = setBit(outb[2], 7, 1 if sigl == "L" else 0)

		outb[3] = setBit(outb[3], 0, 1 if sigl == "N" else 0)
		outb[3] = setBit(outb[3], 1, 1 if sigl == "R" else 0)
		sigl = self.sigLever["C22"]
		outb[3] = setBit(outb[3], 2, 1 if sigl == "L" else 0)
		outb[3] = setBit(outb[3], 3, 1 if sigl == "N" else 0)
		outb[3] = setBit(outb[3], 4, 1 if sigl == "R" else 0)
		sigl = self.sigLever["C24"]
		outb[3] = setBit(outb[3], 5, 1 if sigl == "L" else 0)
		outb[3] = setBit(outb[3], 6, 1 if sigl == "N" else 0)
		outb[3] = setBit(outb[3], 7, 1 if sigl == "R" else 0)

		locked = self.rr.GetOutput("CSw3.hand").GetStatus() != 0  # Hand switch unlock indicators
		outb[4] = setBit(outb[4], 0, 0 if locked else 1)
		outb[4] = setBit(outb[4], 1, 1 if locked else 0)
		locked = self.rr.GetOutput("CSw11.hand").GetStatus() != 0
		outb[4] = setBit(outb[4], 2, 0 if locked else 1)
		outb[4] = setBit(outb[4], 3, 1 if locked else 0)
		locked = self.rr.GetOutput("CSw15.hand").GetStatus() != 0
		outb[4] = setBit(outb[4], 4, 0 if locked else 1)
		outb[4] = setBit(outb[4], 5, 1 if locked else 0)
		locked = self.rr.GetOutput("CSw19.hand").GetStatus() != 0
		outb[4] = setBit(outb[4], 6, 0 if locked else 1)
		outb[4] = setBit(outb[4], 7, 1 if locked else 0)

		lockeda = self.rr.GetOutput("CSw21a.hand").GetStatus() != 0
		lockedb = self.rr.GetOutput("CSw21b.hand").GetStatus() != 0
		locked = lockeda or lockedb
		outb[5] = setBit(outb[5], 0, 0 if locked else 1)
		outb[5] = setBit(outb[5], 1, 1 if locked else 0)
		outb[5] = setBit(outb[5], 2, self.rr.GetInput("B10").GetValue())    # block indicators
		# outb[5] = setBit(outb[5], 3, self.rr.GetInput("CBGreenMountain").GetValue())    #Circuit breakers
		# outb[5] = setBit(outb[5], 4, self.rr.GetInput("CBSheffield").GetValue())
		# outb[5] = setBit(outb[5], 5, self.rr.GetInput("CBClivedon").GetValue())
		# outb[5] = setBit(outb[5], 6, self.rr.GetInput("CBReverser").GetValue())
		# outb[5] = setBit(outb[5], 6, self.rr.GetInput("CBBank").GetValue())
#
# 	CFOut[6].bit.b0 = CSw31.L;		//Switch locks
# 	CFOut[6].bit.b1 = CSw41.L;
# 	CFOut[6].bit.b2 = CSw43.L;
# 	CFOut[6].bit.b3 = CSw61.L;
# 	CFOut[6].bit.b4 = CSw9.L;
# 	CFOut[6].bit.b5 = CSw13.L;
# 	CFOut[6].bit.b6 = CSw17.L;
# 	CFOut[6].bit.b7 = CSw23.L;
#
		outb[7] - setBit(outb[7], 0, 1 if self.rr.GetInput("CSw21a").GetValue() == "R" else 0)  # remote hand switch indications
		outb[7] - setBit(outb[7], 1, 1 if self.rr.GetInput("CSw21b").GetValue() == "R" else 0)  # remote hand switch indications
		outb[7] - setBit(outb[7], 2, 1 if self.rr.GetInput("CSw19").GetValue() == "R" else 0)  # remote hand switch indications
		outb[7] - setBit(outb[7], 3, 1 if self.rr.GetInput("CSw15").GetValue() == "R" else 0)  # remote hand switch indications
		outb[7] - setBit(outb[7], 4, 1 if self.rr.GetInput("CSw11").GetValue() == "R" else 0)  # remote hand switch indications

		inb = [0, 0, 0, 0, 0, 0, 0, 0]
		otext = "{0:08b}  {1:08b}  {2:08b}  {3:08b}  {4:08b}  {5:08b}  {6:08b}  {7:08b}".format(outb[0], outb[1], outb[2], outb[3], outb[4], outb[5], outb[6], outb[7])
		itext = "{0:08b}  {1:08b}  {2:08b}  {3:08b}  {4:08b}  {5:08b}  {6:08b}  {7:08b}".format(inb[0], inb[1], inb[2], inb[3], inb[4], inb[5], inb[6], inb[7])
		logging.debug("Cliff: Output bytes: %s" % otext)
		if self.sendIO:
			self.rr.ShowText(otext, itext, 1, 4)

		inb = []
		inbc = 0
		if inbc == 3:
			pass
# 		C21W = CFIn[0].bit.b0;    //Routes
# 		C40W = CFIn[0].bit.b1;
# 		C44W = CFIn[0].bit.b2;
# 		C43W = CFIn[0].bit.b3;
# 		C42W = CFIn[0].bit.b4;
# 		C41W = CFIn[0].bit.b5;
# 		C41E = CFIn[0].bit.b6;
# 		C42E = CFIn[0].bit.b7;
#
			# "CC44E", "CC43E", "CC42E", "CC41E", "CC40E", "CC21E", "CC50E", "CC51E", "CC52E", "CC53E", "CC54E",
			# "CC44W", "CC43W", "CC42W", "CC41W", "CC40W", "CC21W", "CC50W", "CC51W", "CC52W", "CC53W", "CC54W",
## 		C21E = CFIn[1].bit.b0;
# 		C40E = CFIn[1].bit.b1;
# 		C44E = CFIn[1].bit.b2;
# 		C43E = CFIn[1].bit.b3;
# 		COS3 = CFIn[1].bit.b4;   COSSHE     //Detection
# 		C21.M = CFIn[1].bit.b5;
# 		C40.M = CFIn[1].bit.b6;
# 		C41.M = CFIn[1].bit.b7;
#
# 		C42.M = CFIn[2].bit.b0;
# 		C43.M = CFIn[2].bit.b1;
# 		C44.M = CFIn[2].bit.b2;
# 		COS4 = CFIn[2].bit.b3;  #COSSHW
#
# 		if(!RBDispatcherAll->Checked)
# 		{
# 			CSigL2.L = CFIn[2].bit.b4;			//Signal levers
# 			CSigL2.Callon = CFIn[2].bit.b5;
# 			CSigL2.R = CFIn[2].bit.b6;
# 			CSigL4.L = CFIn[2].bit.b7;
#
# 			CSigL4.Callon = CFIn[3].bit.b0;
# 			CSigL4.R = CFIn[3].bit.b1;
# 			CSigL6.L = CFIn[3].bit.b2;
# 			CSigL6.Callon = CFIn[3].bit.b3;
# 			CSigL6.R = CFIn[3].bit.b4;
# 			CSigL8.L = CFIn[3].bit.b5;
# 			CSigL8.Callon = CFIn[3].bit.b6;
# 			CSigL8.R = CFIn[3].bit.b7;
# 		}
#
# 		if(RBCliff->Checked)
#         {
#
# 			CSigL10.L = CFIn[4].bit.b0;
# 			CSigL10.Callon = CFIn[4].bit.b1;
# 			CSigL10.R = CFIn[4].bit.b2;
# 			CSigL12.L = CFIn[4].bit.b3;
# 			CSigL12.Callon = CFIn[4].bit.b4;
# 			CSigL12.R = CFIn[4].bit.b5;
# 			CSigL14.L = CFIn[4].bit.b6;
# 			CSigL14.Callon = CFIn[4].bit.b7;
#
# 			CSigL14.R = CFIn[5].bit.b0;
# 			CFltL16.R = CFIn[5].bit.b1;				//Fleet
# 			CSigL18.L = CFIn[5].bit.b2;
# 			CSigL18.Callon = CFIn[5].bit.b3;
# 			CSigL18.R = CFIn[5].bit.b4;
# 			CSigL22.L = CFIn[5].bit.b5;
# 			CSigL22.Callon = CFIn[5].bit.b6;
# 			CSigL22.R = CFIn[5].bit.b7;
#
# 			CSigL24.L = CFIn[6].bit.b0;
# 			CSigL24.Callon = CFIn[6].bit.b1;
# 			CSigL24.R = CFIn[6].bit.b2;
# 		}
#
# 		CRelease = CFIn[6].bit.b3;
#
# 		CSigL2.N = !CSigL2.L && !CSigL2.R;
# 		CSigL4.N = !CSigL4.L && !CSigL4.R;
# 		CSigL6.N = !CSigL6.L && !CSigL6.R;
# 		CSigL8.N = !CSigL8.L && !CSigL8.R;
#
# 		if(RBCliff->Checked)
# 		{
# 			CSw3.UnlockReq = CFIn[6].bit.b4;
# 			CSw11.UnlockReq = CFIn[6].bit.b5;
# 			CSw15.UnlockReq = CFIn[6].bit.b6;
# 			CSw19.UnlockReq = CFIn[6].bit.b7;
# 			CSw21.UnlockReq = CFIn[7].bit.b0;
#
# 			CSw3.N = !CSw3.R;
# 			CSw11.N = !CSw11.R;
# 			CSw15.N = !CSw15.R;
# 			CSw19.N = !CSw19.R;
# 			CSw21.N = !CSw21.R;
# 		}
# 	}
#
# //Sheffield
#
# 	SHOut[0].bit.b0 = SBC54E;  //Switch outputs Sheffield
# 	SHOut[0].bit.b1 = SBC53E;
# 	SHOut[0].bit.b2 = SBC52E;
# 	SHOut[0].bit.b3 = SBC51E;
# 	SHOut[0].bit.b4 = SBC50E;
# 	SHOut[0].bit.b5 = SBC21E;
# 	SHOut[0].bit.b6 = SBC40E;
# 	SHOut[0].bit.b7 = SBC41E;
#
# 	SHOut[1].bit.b0 = SBC42E;
# 	SHOut[1].bit.b1 = SBC43E;
# 	SHOut[1].bit.b2 = SBC44E;
# 	SHOut[1].bit.b3 = SBC54W;
# 	SHOut[1].bit.b4 = SBC53W;
# 	SHOut[1].bit.b5 = SBC52W;
# 	SHOut[1].bit.b6 = SBC51W;
# 	SHOut[1].bit.b7 = SBC50W;
#
# 	SHOut[2].bit.b0 = SBC21W;
# 	SHOut[2].bit.b1 = SBC40W;
# 	SHOut[2].bit.b2 = SBC41W;
# 	SHOut[2].bit.b3 = SBC42W;
# 	SHOut[2].bit.b4 = SBC43W;
# 	SHOut[2].bit.b5 = SBC44W;
# 	SHOut[2].bit.b6 = SBC30E;  //Switch outputs Green Mtn.
# 	SHOut[2].bit.b7 = SBC10E;
#
# 	SHOut[3].bit.b0 = SBG10E;
# 	SHOut[3].bit.b1 = SBG12E;
# 	SHOut[3].bit.b2 = SBC30W;
# 	SHOut[3].bit.b3 = SBC31W;
# 	SHOut[3].bit.b4 = SBC10W;
# 	SHOut[3].bit.b5 = SBG21W;
# 	SHOut[3].bit.b6 = 0;
# 	SHOut[3].bit.b7 = 0;
#
# 	SendPacket(SHEFFIELD, &SHAborts, &SHIn[0], &SHOld[0], &SHOut[0], 4, true);
# 			SFText = "Sheffield " + OutText;
#
# 	if(Match)
# 	{
# 		C50W = SHIn[0].bit.b0;   //Routes
# 		C51W = SHIn[0].bit.b1;
# 		C52W = SHIn[0].bit.b2;
# 		C53W = SHIn[0].bit.b3;
# 		C54W = SHIn[0].bit.b4;
# 		C50E = SHIn[0].bit.b5;
# 		C51E = SHIn[0].bit.b6;
# 		C52E = SHIn[0].bit.b7;

			# "CC44E", "CC43E", "CC42E", "CC41E", "CC40E", "CC21E", "CC50E", "CC51E", "CC52E", "CC53E", "CC54E",
			# "CC44W", "CC43W", "CC42W", "CC41W", "CC40W", "CC21W", "CC50W", "CC51W", "CC52W", "CC53W", "CC54W",
#
# 		C53E = SHIn[1].bit.b0;
# 		C54E = SHIn[1].bit.b1;
# 		C50.M = SHIn[1].bit.b2;        //Detection
# 		C51.M = SHIn[1].bit.b3;
# 		C52.M = SHIn[1].bit.b4;
# 		C53.M = SHIn[1].bit.b5;
# 		C54.M = SHIn[1].bit.b6;
# 	}
# }
