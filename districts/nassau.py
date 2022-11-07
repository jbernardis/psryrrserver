import logging

from district import District, LATHAM
from rrobjects import SignalOutput, TurnoutOutput, NXButtonOutput, RelayOutput, IndicatorOutput, BreakerInput, BlockInput, TurnoutInput
from bus import setBit, getBit

class Nassau(District):
	def __init__(self, parent, name, settings):
		District.__init__(self, parent, name, settings)

		sigNames =  [
			"N20R", "N20L",
			"N18R", "N18LA", "N18LB",
			"N16R", "N16L",
			"N14L", "N14LA", "N14LB", "N14LC", "N14LD",
			"N28R", "N28L",
			"N26RA", "N26RB", "N26RC", "N26L",
			"R24RA", "R24RB", "R24RC", "R24RD", "R24L"
		]
		toONames = ["NSw13", "NSw15", "NSw17"]
		toNames = [ "NSw19", "NSw21", "NSw23", "NSw25", "NSw27", "NSw29", "NSw31", "NSw33", "NSw35",
					"NSw39", "NSw41", "NSw43", "NSw45", "NSw47", "NSw51", "NSw53", "NSw55", "NSw57"]
		relayNames = [ "N21.srel" ]

		self.NXMap = {
			"NNXBtnT12": {
				"NNXBtnW10":  [ ["NSw25", "N"] ]
			},

			"NNXBtnN60": {
				"NNXBtnW10":  [ ["NSw21", "N"], ["NSw23", "R"], ["NSw25", "R"], ["NSw27", "N"] ],
				"NNXBtnN32W": [ ["NSw21", "N"], ["NSw23", "R"], ["NSw25", "N"], ["NSw27", "N"] ],
				"NNXBtnN31W": [ ["NSw21", "N"], ["NSw23", "N"], ["NSw27", "N"] ],
				"NNXBtnN12W": [ ["NSw21", "N"], ["NSw27", "R"], ["NSw29", "N"] ],
				"NNXBtnN22W": [ ["NSw27", "R"], ["NSw29", "R"], ["NSw31", "N"] ],
				"NNXBtnN41W": [ ["NSw27", "R"], ["NSw29", "R"], ["NSw31", "R"], ["NSw33", "R"] ],
				"NNXBtnN42W": [ ["NSw27", "R"], ["NSw29", "R"], ["NSw31", "R"], ["NSw33", "N"], ["NSw35", "R"] ],
				"NNXBtnW20W": [ ["NSw27", "R"], ["NSw29", "R"], ["NSw31", "R"], ["NSw33", "N"], ["NSw35", "N"] ],
			},

			"NNXBtnN11": {
				"NNXBtnW10":  [ ["NSw19", "N"], ["NSw21", "R"], ["NSw23", "R"], ["NSw25", "R"], ["NSw27", "N"], ["NSw29", "N"] ],
				"NNXBtnN32W": [ ["NSw19", "N"], ["NSw21", "R"], ["NSw23", "R"], ["NSw25", "N"], ["NSw27", "N"], ["NSw29", "N"] ],
				"NNXBtnN31W": [ ["NSw19", "N"], ["NSw21", "R"], ["NSw23", "N"], ["NSw27", "N"], ["NSw29", "N"] ],
				"NNXBtnN12W": [ ["NSw19", "N"], ["NSw21", "N"], ["NSw27", "N"], ["NSw29", "N"] ],
				"NNXBtnN22W": [ ["NSw19", "N"], ["NSw27", "N"], ["NSw29", "R"], ["NSw31", "N"] ],
				"NNXBtnN41W": [ ["NSw19", "N"], ["NSw27", "N"], ["NSw29", "R"], ["NSw31", "R"], ["NSw33", "R"] ],
				"NNXBtnN42W": [ ["NSw19", "N"], ["NSw27", "N"], ["NSw29", "R"], ["NSw31", "R"], ["NSw33", "N"], ["NSw35", "R"] ],
				"NNXBtnW20W": [ ["NSw19", "N"], ["NSw27", "N"], ["NSw29", "R"], ["NSw31", "R"], ["NSw33", "N"], ["NSw35", "N"] ],
			},

			"NNXBtnN21": {
				"NNXBtnW10":  [ ["NSw19", "R"], ["NSw21", "R"], ["NSw23", "R"], ["NSw25", "R"], ["NSw27", "N"], ["NSw29", "N"] ],
				"NNXBtnN32W": [ ["NSw19", "R"], ["NSw21", "R"], ["NSw23", "R"], ["NSw25", "N"], ["NSw27", "N"], ["NSw29", "N"] ],
				"NNXBtnN31W": [ ["NSw19", "R"], ["NSw21", "R"], ["NSw23", "N"], ["NSw27", "N"], ["NSw29", "N"] ],
				"NNXBtnN12W": [ ["NSw19", "R"], ["NSw21", "N"], ["NSw27", "N"], ["NSw29", "N"] ],
				"NNXBtnN22W": [ ["NSw19", "N"], ["NSw29", "N"], ["NSw31", "N"] ],
				"NNXBtnN41W": [ ["NSw19", "N"], ["NSw29", "N"], ["NSw31", "R"], ["NSw33", "R"] ],
				"NNXBtnN42W": [ ["NSw19", "N"], ["NSw29", "N"], ["NSw31", "R"], ["NSw33", "N"], ["NSw35", "R"] ],
				"NNXBtnW20W": [ ["NSw19", "N"], ["NSw29", "N"], ["NSw31", "R"], ["NSw33", "N"], ["NSw35", "N"] ],
			},
						"NNXBtnR10": {
				"NNXBtnW11":  [ ["NSw47", "N"], ["NSw55", "N"] ],
				"NNXBtnN32E": [ ["NSw51", "N"], ["NSw53", "R"], ["NSw55", "N"], ["NSw45", "N"], ["NSw47", "R"] ],
				"NNXBtnN31E": [ ["NSw51", "R"], ["NSw53", "R"], ["NSw55", "N"], ["NSw45", "N"], ["NSw47", "R"] ],
				"NNXBtnN12E": [ ["NSw53", "N"], ["NSw55", "N"], ["NSw45", "N"], ["NSw47", "R"] ],
				"NNXBtnN22E": [ ["NSw43", "N"], ["NSw45", "R"], ["NSw47", "R"] ],
				"NNXBtnN41E": [ ["NSw41", "R"], ["NSw43", "R"], ["NSw45", "R"], ["NSw47", "R"] ],
				"NNXBtnN42E": [ ["NSw39", "R"], ["NSw41", "N"], ["NSw43", "R"], ["NSw45", "R"], ["NSw47", "R"] ],
				"NNXBtnW20E": [ ["NSw39", "N"], ["NSw41", "N"], ["NSw43", "R"], ["NSw45", "R"], ["NSw47", "R"] ]
			}, 
			
			"NNXBtnB10": {
				"NNXBtnW11":  [ ["NSw55", "R"], ["NSw45", "N"], ["NSw47", "N"], ["NSw57", "N"] ],
				"NNXBtnN32E": [ ["NSw51", "N"], ["NSw53", "R"], ["NSw55", "N"], ["NSw45", "N"], ["NSw47", "N"], ["NSw57", "N"] ],
				"NNXBtnN31E": [ ["NSw51", "R"], ["NSw53", "R"], ["NSw55", "N"], ["NSw45", "N"], ["NSw47", "N"], ["NSw57", "N"] ],
				"NNXBtnN12E": [ ["NSw53", "N"], ["NSw55", "N"], ["NSw45", "N"], ["NSw47", "N"], ["NSw57", "N"] ],
				"NNXBtnN22E": [ ["NSw43", "N"], ["NSw45", "R"], ["NSw47", "N"], ["NSw57", "N"] ],
				"NNXBtnN41E": [ ["NSw41", "R"], ["NSw43", "R"], ["NSw45", "R"], ["NSw47", "N"], ["NSw57", "N"]],
				"NNXBtnN42E": [ ["NSw39", "R"], ["NSw41", "N"], ["NSw43", "R"], ["NSw45", "R"], ["NSw47", "N"], ["NSw57", "N"] ],
				"NNXBtnW20E": [ ["NSw39", "N"], ["NSw41", "N"], ["NSw43", "R"], ["NSw45", "R"], ["NSw47", "N"], ["NSw57", "N"] ]
			}, 
			
			"NNXBtnB20": {
				"NNXBtnW11":  [ ["NSw55", "R"], ["NSw45", "N"], ["NSw47", "N"], ["NSw57", "R"] ],
				"NNXBtnN32E": [ ["NSw51", "N"], ["NSw53", "R"], ["NSw55", "N"], ["NSw45", "N"], ["NSw47", "N"], ["NSw57", "R"]],
				"NNXBtnN31E": [ ["NSw51", "R"], ["NSw53", "R"], ["NSw55", "N"], ["NSw45", "N"], ["NSw47", "N"], ["NSw57", "R"]],
				"NNXBtnN12E": [ ["NSw53", "N"], ["NSw55", "N"], ["NSw45", "N"], ["NSw47", "N"], ["NSw57", "R"] ],
				"NNXBtnN22E": [ ["NSw43", "N"], ["NSw45", "N"], ["NSw57", "N"] ],
				"NNXBtnN41E": [ ["NSw41", "R"], ["NSw43", "R"], ["NSw45", "N"], ["NSw57", "N"] ],
				"NNXBtnN42E": [ ["NSw39", "R"], ["NSw41", "N"], ["NSw43", "R"], ["NSw45", "N"], ["NSw57", "N"] ],
				"NNXBtnW20E": [ ["NSw39", "N"], ["NSw41", "N"], ["NSw43", "R"], ["NSw45", "N"], ["NSw57", "N"] ]
			}

		}
		ix = 0
		nxButtons = [
			"NNXBtnT12", "NNXBtnN60", "NNXBtnN11", "NNXBtnN21",
			"NNXBtnW10", "NNXBtnN32W",	"NNXBtnN31W", "NNXBtnN12W", "NNXBtnN22W", "NNXBtnN41W", "NNXBtnN42W", "NNXBtnW20W",
			"NNXBtnR10", "NNXBtnB10", "NNXBtnB20",
			"NNXBtnW11", "NNXBtnN32E", "NNXBtnN31E", "NNXBtnN12E", "NNXBtnN22E", "NNXBtnN41E", "NNXBtnN42E", "NNXBtnW20E"
		]
		ix = self.AddOutputs(nxButtons, NXButtonOutput, District.nxbutton, ix)
		ix = self.AddOutputs(toONames, TurnoutOutput, District.turnout, ix)
		ix = self.AddOutputs(sigNames, SignalOutput, District.signal, ix)
		ix = self.AddOutputs(relayNames, RelayOutput, District.relay, ix)

		for n in nxButtons:
			self.SetNXButtonPulseLen(n, 2)

		brkrNames = [ "CBKrulish", "CBNassauW", "CBNassauE", "CBSptJct", "CBWilson", "CBThomas" ]
		blockNames = [ "N21.W", "N21", "N21.E", "NWOSTY", "NWOSCY", "NWOSW", "NWOSE",
						"N31", "N32", "N12", "N22", "N41", "N42",
						"N60", "T12", "W10", "W20", "R10" ]

		ix = 0
		ix = self.AddInputs(blockNames, BlockInput, District.block, ix)
		ix = self.AddInputs(toNames+toONames, TurnoutInput, District.turnout, ix)
		ix = self.AddInputs(brkrNames, BreakerInput, District.breaker, ix)

	def EvaluateNXButtons(self, bEntry, bExit):
		if bEntry not in self.NXMap:
			print("entry button not found")
			return

		if bExit not in self.NXMap[bEntry]:
			print("exit button not found")
			return

		tolist = self.NXMap[bEntry][bExit]

		for toName, status in tolist:
			print("to: (%s)" % toName)
			self.rr.GetInput(toName).SetState(status)
			print("turnout: name: %s, state: %s" % (toName, status))

	def OutIn(self):
		#Latham
		outb = [0 for i in range(5)]

# 	NWOut[0].bit.b0 = N14LC.Aspect[0];	//Interlocking Signals
# 	NWOut[0].bit.b1 = N14LB.Aspect[0];
# 	NWOut[0].bit.b2 = N20R.Aspect[0];
#     NWOut[0].bit.b3 = N20L.Aspect[0];
#     NWOut[0].bit.b4 = N14LA.Aspect[0];
#     NWOut[0].bit.b5 = N14LA.Aspect[1];
# 	NWOut[0].bit.b6 = N16L.Aspect[0];
# 	NWOut[0].bit.b7 = N16L.Aspect[1];

# 	NWOut[1].bit.b0 = N18LB.Aspect[0];
#     NWOut[1].bit.b1 = N18LB.Aspect[1];
# 	NWOut[1].bit.b2 = N18LA.Aspect[0];
# 	NWOut[1].bit.b3 = N18LA.Aspect[1];
# 	NWOut[1].bit.b4 = N16R.Aspect[0];
# 	NWOut[1].bit.b5 = N16R.Aspect[1];
# 	NWOut[1].bit.b6 = N14R.Aspect[0];
# 	NWOut[1].bit.b7 = N14R.Aspect[1];    //Bad output?

# 	NWOut[2].bit.b0 = N18R.Aspect[0];
#     NWOut[2].bit.b1 = N11W.Aspect[0];  	//Block signals
#     NWOut[2].bit.b2 = N11W.Aspect[1];
#     NWOut[2].bit.b3	= N11W.Aspect[2];
#     NWOut[2].bit.b4 = N21W.Aspect[0];
#     NWOut[2].bit.b5 = N21W.Aspect[1];
#     NWOut[2].bit.b6 = N21W.Aspect[2];
# 	NWOut[2].bit.b7 = S11.Blk;			//Shore approach indicator

#    	NWOut[3].bit.b0 = R10.M || R10.W;  	//Rocky Hill approach indicator
#    	NWOut[3].bit.b1 = B20.Blk;       	//Bank approach indicator
# 	NWOut[3].bit.b2 = !NFltL12.R;		//Fleet indicator
# 	NWOut[3].bit.b3 = NFltL12.R;
# 	NWOut[3].bit.b4 = NSigL14.LI;      	//Signal indicators
# 	NWOut[3].bit.b5 = NSigL14.NI;
# 	NWOut[3].bit.b6 = NSigL14.RI;
#     NWOut[3].bit.b7 = NSigL16.LI;

# 	NWOut[4].bit.b0 = NSigL16.NI;
#     NWOut[4].bit.b1 = NSigL16.RI;
#     NWOut[4].bit.b2 = NSigL18.LI;
# 	NWOut[4].bit.b3 = NSigL18.NI;
# 	NWOut[4].bit.b4 = NSigL18.RI;
# 	NWOut[4].bit.b5 = NSigL20.LI;
# 	NWOut[4].bit.b6 = NSigL20.NI;
#     NWOut[4].bit.b7 = NSigL20.RI;

# 	NWOut[5].bit.b0 = KSw1.NO;			//Krulish switch outputs
# 	NWOut[5].bit.b1 = KSw1.RO;
# 	NWOut[5].bit.b2 = KSw3.NO;
#     NWOut[5].bit.b3 = KSw3.RO;
#     NWOut[5].bit.b4 = KSw5.NO;
#     NWOut[5].bit.b5 = KSw5.RO;
#     NWOut[5].bit.b6 = KSw7.NO;
#     NWOut[5].bit.b7 = KSw7.RO;

# 	NWOut[6].bit.b0 = CBKrulish;      	//DCC Circuit Breakers
# 	NWOut[6].bit.b1 = CBNassauW;
# 	NWOut[6].bit.b2 = CBNassauE;
# 	NWOut[6].bit.b3 = CBSptJct;
# 	NWOut[6].bit.b4 = CBWilson;
#     NWOut[6].bit.b5 = CBThomas;
# 	NWOut[6].bit.b6 = NWSL1;			//Switch locks
# 	NWOut[6].bit.b7 = NWSL2;

#     NWOut[7].bit.b0 = NWSL3;
# 	NWOut[7].bit.b1 = NWSL4;
#    	NWOut[7].bit.b2 = N21.Srel;			//Stop relay
# 	NWOut[7].bit.b3 = N14R.Aspect[1];   //transferred bit
# 	NWOut[7].bit.b4 = N14LD.Aspect[0];  //Dwarf signals for W20
# 	NWOut[7].bit.b5 = N24RD.Aspect[0];

# 	SendPacket(NASSAUW, &NassauWAborts, &NWIn[0], &NWOld[0], &NWOut[0], 8, true);
# 		NWText = "NassauW\t" + OutText;

# 	if(Match)
# 	{
# 		NSw19.NI = NWIn[0].bit.b0;	//Switch positions
# 		NSw19.RI = NWIn[0].bit.b1;
# 		NSw21.NI = NWIn[0].bit.b2;
# 		NSw21.RI = NWIn[0].bit.b3;
# 		NSw23.NI = NWIn[0].bit.b4;
# 		NSw23.RI = NWIn[0].bit.b5;
# 		NSw25.NI = NWIn[0].bit.b6;
# 		NSw25.RI = NWIn[0].bit.b7;

# 		NSw27.NI = NWIn[1].bit.b0;
# 		NSw27.RI = NWIn[1].bit.b1;
# 		NSw29.NI = NWIn[1].bit.b2;
# 	   	NSw29.RI = NWIn[1].bit.b3;
# 	   	NSw31.NI = NWIn[1].bit.b4;
# 	   	NSw31.RI = NWIn[1].bit.b5;
# 	   	NSw33.NI = NWIn[1].bit.b6;
# 	   	NSw33.RI = NWIn[1].bit.b7;

# 		N21.W = NWIn[2].bit.b0;   //Detection
# 		N21.M = NWIn[2].bit.b1;
# 		N21.E = NWIn[2].bit.b2;
# 	   	NWOSTY  NWOS1 = NWIn[2].bit.b3;
# 	   NWOSCY   NWOS2 = NWIn[2].bit.b4;
# 	   	NWOSW   NWOS3 = NWIn[2].bit.b5;
# 	   	NWOSE   NWOS4 = NWIn[2].bit.b6;
# 	   	N32.M = NWIn[2].bit.b7;

# 		N31.M 			= NWIn[3].bit.b0;
# 	  	N12.M 			= NWIn[3].bit.b1;
# 		NRelease 		= NWIn[3].bit.b2; 	//Switch release
# 		if(RBNassau->Checked)
# 		{
# 			NFltL12.R 		= NWIn[3].bit.b3;	//Fleet lever
# 			NSigL14.R		= NWIn[3].bit.b4;	//Signal levers
# 			NSigL14.Callon	= NWIn[3].bit.b5;
# 			NSigL14.L		= NWIn[3].bit.b6;
# 			NSigL16.R 		= NWIn[3].bit.b7;
# 			NSigL16.Callon	= NWIn[4].bit.b0;
# 			NSigL16.L		= NWIn[4].bit.b1;
# 			NSigL18.R		= NWIn[4].bit.b2;
# 			NSigL18.Callon	= NWIn[4].bit.b3;
# 			NSigL18.L		= NWIn[4].bit.b4;
# 			NSigL24.R		= NWIn[5].bit.b0;
# 			NSigL24.Callon	= NWIn[5].bit.b1;
# 			NSigL24.L	 	= NWIn[5].bit.b2;
# 			NSigL26.R 		= NWIn[5].bit.b3;
# 			NSigL26.Callon 	= NWIn[5].bit.b4;
# 			NSigL26.L 		= NWIn[5].bit.b5;
# 		}

# 		if(!RBNDispatcherAll->Checked)
# 		{
# 			NSigL20.R		= NWIn[4].bit.b5;
# 			NSigL20.Callon	= NWIn[4].bit.b6;
# 			NSigL20.L		= NWIn[4].bit.b7;
# 			NSigL28.R	 	= NWIn[5].bit.b6;
# 			NSigL28.Callon	= NWIn[5].bit.b7;
# 			NSigL28.L   	= NWIn[6].bit.b0;
# 		}

#       	CktBkr[19]		= !NWIn[6].bit.b1;	//Krulish Yard circuit breaker
# 	   	CktBkr[20]		= !NWIn[6].bit.b2;	//Thomas Yard
# 		CktBkr[21]		= !NWIn[6].bit.b3;	//Wilson City
# 		CktBkr[22]		= !NWIn[6].bit.b4; 	//Krulish
# 		CktBkr[23] 		= !NWIn[6].bit.b5; 	//Nassau West
# 	 	CktBkr[24]		= !NWIn[6].bit.b6; 	//Nassau East
# 		CktBkr[25]		= !NWIn[6].bit.b7; 	//Foss

# 		CktBkr[26]		= !NWIn[7].bit.b0; 	//Dell
# 		NSw60A          = NWIn[7].bit.b1;   //Switches in coach yard
# 		NSw60B          = NWIn[7].bit.b2;
# 		NSw60C          = NWIn[7].bit.b3;
# 		NSw60D          = NWIn[7].bit.b4;
# 		NSw35.NI        = NWIn[7].bit.b5;   //additional switch in Nassau West NX
# 		NSw35.RI        = NWIn[7].bit.b6;
# 	}

# 	NFltL12.N = !NFltL12.R;
# 	NSigL14.N = !(NSigL14.R || NSigL14.L);
# 	NSigL16.N = !(NSigL16.R || NSigL16.L);
# 	NSigL18.N = !(NSigL18.R || NSigL18.L);
# 	NSigL20.N = !(NSigL20.R || NSigL20.L);
# 	NSigL24.N = !(NSigL24.R || NSigL24.L);
# 	NSigL26.N = !(NSigL26.R || NSigL26.L);
# 	NSigL28.N = !(NSigL28.R || NSigL28.L);

# 	if(NSw60A)
# 	{
# 		NSw13.RI = NSw15.RI = NSw17.RI = true;
# 		NSw13.NI = NSw15.NI = NSw17.NI = false;
# 	}
# 	else if(NSw60B)
# 	{
# 		NSw13.NI = NSw15.NI = NSw17.RI = true;
# 		NSw13.RI = NSw15.RI = NSw17.NI = false;
# 	}
# 	else if(NSw60C)
# 	{
# 		NSw13.RI = NSw15.RI = NSw17.NI = true;
# 		NSw13.NI = NSw15.NI = NSw17.RI = false;
# 	}
# 	else if(NSw60D)
# 	{
# 		NSw13.NI = NSw15.NI = NSw17.NI = true;
# 		NSw13.RI = NSw15.RI = NSw17.RI = false;
# 	}


# //NassauE-----------------------------------------------------------------------

# 	NEOut[0].bit.b0 = N24RB.Aspect[0];		//Signals
# 	NEOut[0].bit.b1 = N24RB.Aspect[1];
# 	NEOut[0].bit.b2 = N24RC.Aspect[0];
# 	NEOut[0].bit.b3 = N24RC.Aspect[1];
# 	NEOut[0].bit.b4 = N26RC.Aspect[0];
# 	NEOut[0].bit.b5 = N26RC.Aspect[1];
# 	NEOut[0].bit.b6 = N24RA.Aspect[0];
#     NEOut[0].bit.b7 = N24RA.Aspect[1];

#     NEOut[1].bit.b0 = N26RA.Aspect[0];
#     NEOut[1].bit.b1 = N26RB.Aspect[0];
# 	NEOut[1].bit.b2 = N28R.Aspect[0];
#     NEOut[1].bit.b3 = B20E.Aspect[0];       //Block signal
#     NEOut[1].bit.b4 = B20E.Aspect[1];
#    	NEOut[1].bit.b5 = B20E.Aspect[2];
# 	NEOut[1].bit.b6 = N24L.Aspect[0];
# 	NEOut[1].bit.b7 = N26L.Aspect[0];

#    	NEOut[2].bit.b0 = N26L.Aspect[1];
#     NEOut[2].bit.b1 = N28L.Aspect[0];
#     NEOut[2].bit.b2 = N28L.Aspect[1];
#    	NEOut[2].bit.b3 = NESL1;                //Switch locks
#     NEOut[2].bit.b4 = NESL2;
#    	NEOut[2].bit.b5 = NESL3;
#     NEOut[2].bit.b6 = B10.Srel;           	//Stop relay
#     NEOut[2].bit.b7 = NSigL24.LI;           //Signal indicators

#   	NEOut[3].bit.b0 = NSigL24.NI;
#     NEOut[3].bit.b1 = NSigL24.RI;
# 	NEOut[3].bit.b2 = NSigL26.LI;
#     NEOut[3].bit.b3 = NSigL26.NI;
#    	NEOut[3].bit.b4 = NSigL26.RI;
#    	NEOut[3].bit.b5 = NSigL28.LI;
#    	NEOut[3].bit.b6 = NSigL28.NI;
#     NEOut[3].bit.b7 = NSigL28.RI;

# 	SendPacket(NASSAUE, &NassauEAborts, &NEIn[0], &NEOld[0], &NEOut[0], 4, true);
# 		NEText = "NassauE\t" + OutText;

# 	if(Match)
#    	{
#       	NSw41.NI = NEIn[0].bit.b0;    //Switch positions
# 	   	NSw41.RI = NEIn[0].bit.b1;
# 	   	NSw43.NI = NEIn[0].bit.b2;
# 	   	NSw43.RI = NEIn[0].bit.b3;
# 		NSw45.NI = NEIn[0].bit.b4;
# 	   	NSw45.RI = NEIn[0].bit.b5;
# 	   	NSw47.NI = NEIn[0].bit.b6;
# 	   	NSw47.RI = NEIn[0].bit.b7;

# 	   	NSw51.NI = NEIn[1].bit.b0;
# 	   	NSw51.RI = NEIn[1].bit.b1;
#       	NSw53.NI = NEIn[1].bit.b2;
# 	   	NSw53.RI = NEIn[1].bit.b3;
# 	   	NSw55.NI = NEIn[1].bit.b4;
# 	   	NSw55.RI = NEIn[1].bit.b5;
# 	   	NSw57.NI = NEIn[1].bit.b6;
# 	   	NSw57.RI = NEIn[1].bit.b7;

# 	   	N22.M 	= NEIn[2].bit.b0;	//Detection
# 	   	N41.M	= NEIn[2].bit.b1;
# 	  	N42.M 	= NEIn[2].bit.b2;
# 	   	NEOS1 	= NEIn[2].bit.b3;
# 		NEOS2 	= NEIn[2].bit.b4;
# 	   	NEOS3 	= NEIn[2].bit.b5;
# 	   	B10.W	= NEIn[2].bit.b6;
# 		B10.M 	= NEIn[2].bit.b7;

# 		NSw39.NI = NEIn[3].bit.b0;  //Additional switch in Nassau East NX
# 		NSw39.RI = NEIn[3].bit.b1;
# 	}

# 	//NASSAUNX Output only

		op = self.rr.GetOutput("NNXBtnT12").GetOutPulse()
		op = self.rr.GetOutput("NNXBtnN60").GetOutPulse()
		op = self.rr.GetOutput("NNXBtnN11").GetOutPulse()
		op = self.rr.GetOutput("NNXBtnN21").GetOutPulse()

		op = self.rr.GetOutput("NNXBtnW10").GetOutPulse()
		op = self.rr.GetOutput("NNXBtnN32W").GetOutPulse()
		op = self.rr.GetOutput("NNXBtnN31W").GetOutPulse()
		op = self.rr.GetOutput("NNXBtnN12W").GetOutPulse()
		op = self.rr.GetOutput("NNXBtnN22W").GetOutPulse()
		op = self.rr.GetOutput("NNXBtnN41W").GetOutPulse()
		op = self.rr.GetOutput("NNXBtnN42W").GetOutPulse()
		op = self.rr.GetOutput("NNXBtnW20W").GetOutPulse()

		op = self.rr.GetOutput("NNXBtnR10").GetOutPulse()
		op = self.rr.GetOutput("NNXBtnB10").GetOutPulse()
		op = self.rr.GetOutput("NNXBtnB20").GetOutPulse()

		op = self.rr.GetOutput("NNXBtnW11").GetOutPulse()
		op = self.rr.GetOutput("NNXBtnN32E").GetOutPulse()
		op = self.rr.GetOutput("NNXBtnN31E").GetOutPulse()
		op = self.rr.GetOutput("NNXBtnN12E").GetOutPulse()
		op = self.rr.GetOutput("NNXBtnN22E").GetOutPulse()
		op = self.rr.GetOutput("NNXBtnN41E").GetOutPulse()
		op = self.rr.GetOutput("NNXBtnN42E").GetOutPulse()
		op = self.rr.GetOutput("NNXBtnW20E").GetOutPulse()


# 	NXOut[0].bit.b0 = NXBtnT12;       	//Nassau West
# 	NXOut[0].bit.b1 = NXBtnN60;
# 	NXOut[0].bit.b2 = NXBtnN11;
# 	NXOut[0].bit.b3 = NXBtnN21;
# 	NXOut[0].bit.b4 = NXBtnW10;
# 	NXOut[0].bit.b5 = NXBtnN32W;
# 	NXOut[0].bit.b6 = NXBtnN31W;
# 	NXOut[0].bit.b7 = NXBtnN12W;

# 	NXOut[1].bit.b0 = NXBtnN22W;
# 	NXOut[1].bit.b1 = NXBtnN41W;
# 	NXOut[1].bit.b2 = NXBtnN42W;
# 	NXOut[1].bit.b3 = NXBtnW20W;
# 	NXOut[1].bit.b4 = NXBtnW11;
# 	NXOut[1].bit.b5 = NXBtnN32E;        //Nassau East
# 	NXOut[1].bit.b6 = NXBtnN31E;
# 	NXOut[1].bit.b7 = NXBtnN12E;

# 	NXOut[2].bit.b0 = NXBtnN22E;
# 	NXOut[2].bit.b1 = NXBtnN41E;
# 	NXOut[2].bit.b2 = NXBtnN42E;
# 	NXOut[2].bit.b3 = NXBtnW20E;
# 	NXOut[2].bit.b4 = NXBtnR10;
# 	NXOut[2].bit.b5 = NXBtnB10;
# 	NXOut[2].bit.b6 = NXBtnB20;
# // 	NXOut[2].bit.b7 =

# 	SendPacket(NASSAUNX, &NassauNXAborts, &NXIn[0], &NXOld[0], &NXOut[0], 3, true);
# 		NXText = "NassauNX" + OutText;
# }
# //---------------------------------------------------------------------------

