import wx

import pprint

from districts.hyde import Hyde
from districts.yard import Yard
from districts.latham import Latham

# tower addresses


class Railroad(wx.Notebook):
	def __init__(self, frame, cbEvent):
		wx.Notebook.__init__(self, frame, wx.ID_ANY, style=wx.BK_DEFAULT)
		self.frame = frame
		self.cbEvent = cbEvent
		self.verbose = False

		districtList = [
			[ "yard", Yard ],
			[ "latham", Latham ],
			[ "hyde", Hyde ],
		]

		self.districts = {}
		self.outputs = {}
		self.inputs = {}
		
		for dname, dclass in districtList:
			p = dclass(self, dname)
			self.AddPage(p, dname)
			self.districts[dname] = p

	def AddOutput(self, output, district):
		output.SetRailRoad(self)
		oname = output.GetName()
		if oname in self.outputs:
			print("Output (%s) duplicate definition" % oname)
			return

		self.outputs[oname] = [output, district]

	def AddInput(self, input, district):
		input.SetRailRoad(self)
		iname = input.GetName()
		if iname in self.inputs:
			print("Input (%s) duplicate definitionb" % iname)
			return

		self.inputs[iname] = [input, district]

	def GetOutput(self, oname):
		try:
			return self.outputs[oname][0]
		except KeyError:
			print("No output found for name \"%s\"" % oname)
			return None

	def GetInput(self, iname):
		try:
			return self.inputs[iname][0]
		except KeyError:
			print("No input found for name \"%s\"" % iname)
			return None

	def SetAspect(self, signame, aspect):
		if signame not in self.outputs:
			print("No output defined for signal %s" % signame)
			return
		op, district = self.outputs[signame]
		op.SetAspect(aspect)
		district.UpdateSignal(signame)

	def SetIndicator(self, indname, state):
		if indname not in self.outputs:
			print("no output defined for indicator %s" % indname)
			return
		op, district = self.outputs[indname]
		op.SetStatus(state!=0)
		district.UpdateIndicator(indname)

	def SetHandSwitch(self, hsname, state):
		if hsname not in self.outputs:
			print("no output defined for handswitch %s" % hsname)
			return
		op, district = self.outputs[hsname]
		op.SetStatus(state!=0)
		district.UpdateHandSwitch(hsname)

	def SetSwitchLock(self, toname, state):
		if toname not in self.outputs:
			print("no output defined for turnout %s" % toname)
			return
		op, district = self.outputs[toname]
		print("setting lock on switch %s to %d" % (toname, state))
		op.SetLock(state)
		district.UpdateTurnout(toname)

	def SetOutPulse(self, toname, state):
		if toname not in self.outputs:
			print("no output defined for turnout %s" % toname)
			return
		op, district = self.outputs[toname]
		op.SetOutPulse(state)
		district.UpdateTurnout(toname)

	def RefreshTurnout(self, toname):
		if toname not in self.outputs:
			print("no output defined for turnout %s" % toname)
			return
		district = self.outputs[toname][1]
		print("callint updateturnout for turnout %s" % toname)
		district.UpdateTurnout(toname)

	def SetVerbose(self, flag=True):
		self.verbose = flag
		for d in self.districts.values():
			d.SetVerbose(flag)

	def allIO(self):
		for d in self.districts.values():
			d.OutIn()

	def RailroadEvent(self, event):
		self.cbEvent(event)



# 	# def setBlockIndicator(self, blknm, flag=True):
# 	# 	try:
# 	# 		blk = self.blocks[blknm]
# 	# 	except KeyError:
# 	# 		print("SetBlockIndicator: No definition for block %s" % blknm)
# 	# 		return False

# 	# 	return blk.setIndicator(flag)

# 	# def setStoppingRelay(self, srnm, flag=True):
# 	# 	try:
# 	# 		sr = self.relays[srnm]
# 	# 	except KeyError:
# 	# 		print("SetStoppingRelay: No definition for stopping relay %s" % srnm)
# 	# 		return False

# 	# 	return sr.setStatus(flag)




	# # these next methoda are for obtaining information from inbound messages
	# def setSwitchPosition(self, swnm, ibyte, maskn, maskr):
	# 	try:
	# 		sw = self.switches[swnm]
	# 	except KeyError:
	# 		print("setSwitchPosition: no switch definition for %s" % swnm)
	# 		return

	# 	spn = 1 if (ibyte & maskn) != 0 else 0		
	# 	spr = 1 if (ibyte & maskr) != 0 else 0
	# 	if spn == 1:
	# 		sp = 1
	# 	elif spr == 1:
	# 		sp = -1
	# 	else:
	# 		sp = 0
	# 	sw.setPosition(sp)

	