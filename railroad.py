import wx
import logging

from districts.hyde import Hyde
from districts.yard import Yard
from districts.latham import Latham
from districts.dell import Dell
from districts.shore import Shore
from districts.krulish import Krulish
from districts.nassau import Nassau
from districts.bank import Bank
from districts.cliveden import Cliveden
from districts.cliff import Cliff


class Railroad(wx.Notebook):
	def __init__(self, frame, cbEvent, settings):
		wx.Notebook.__init__(self, frame, wx.ID_ANY, style=wx.BK_DEFAULT)
		self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.pageChanged)
		self.frame = frame
		self.cbEvent = cbEvent
		self.settings = settings

		self.districtList = [
			[ "Yard", Yard ],
			[ "Latham", Latham ],
			[ "Dell", Dell ],
			[ "Shore", Shore ],
			[ "Krulish", Krulish ],
			[ "Nassau", Nassau ],
			[ "Bank", Bank ],
			[ "Cliveden", Cliveden ],
			[ "Cliff", Cliff ],
			[ "Hyde", Hyde ],
		]

		self.districts = {}
		self.outputs = {}
		self.inputs = {}
		self.osRoutes = {}
		for dname, dclass in self.districtList:
			logging.debug("Creating district %s" % dname)
			p = dclass(self, dname, self.settings)
			self.AddPage(p, dname)
			self.districts[dname] = p

		self.SetPageText(0, "* " + self.districtList[0][0] + " *")

	def Initialize(self):
		for dname, dobj in self.districts.items():
			dobj.SendIO(False)
			dobj.DetermineSignalLevers()

		self.districts["Yard"].SendIO(True)

	def pageChanged(self, evt):
		opx = evt.GetOldSelection()
		if opx != wx.NOT_FOUND:
			self.SetPageText(opx, self.districtList[opx][0])
			odistrict = self.districts[self.districtList[opx][0]]
			odistrict.SendIO(False)
		px = evt.GetSelection()
		if px != wx.NOT_FOUND:
			self.SetPageText(px, "* " + self.districtList[px][0] + " *")
			district = self.districts[self.districtList[px][0]]
			district.SendIO(True)

	def ClearIO(self):
		self.frame.ClearIO()

	def ShowText(self, otext, itext, line, lines):
		self.frame.ShowText(otext, itext, line, lines)

	def AddOutput(self, output, district, otype):
		output.SetRailRoad(self)
		oname = output.GetName()
		if oname in self.outputs:
			logging.warning("Output (%s) duplicate definition" % oname)
			return

		self.outputs[oname] = [output, district, otype]

	def AddInput(self, input, district, itype):
		input.SetRailRoad(self)
		iname = input.GetName()
		if iname in self.inputs:
			logging.warning("Input (%s) duplicate definitionb" % iname)
			return

		self.inputs[iname] = [input, district, itype]

	def GetOutput(self, oname):
		try:
			return self.outputs[oname][0]
		except KeyError:
			logging.warning("No output found for name \"%s\"" % oname)
			return None

	def GetInput(self, iname):
		try:
			return self.inputs[iname][0]
		except KeyError:
			logging.warning("No input found for name \"%s\"" % iname)
			return None

	def GetCurrentValues(self):
		for ip,district,itype in self.inputs.values():
			m = ip.GetEventMessage()
			if m is not None:
				yield m

		for op,district,itype in self.outputs.values():
			m = op.GetEventMessage()
			if m is not None:
				yield m

		print("get current values - about to send routes")
		for osblk, rtinfo in self.osRoutes.items():
			rt = rtinfo[0]
			ends = rtinfo[1]
			print("block: %s %s" % (osblk, rt))
			m = {"setroute": [{ "block": osblk, "route": str(rt)}]}
			if ends is not None:
				m["setroute"][0]["ends"] = ends
			yield m

	def SetOSRoute(self, blknm, rtname, ends, signals):
		self.osRoutes[blknm] = [rtname, ends, signals]

	def PlaceTrain(self, blknm):
		if blknm not in self.inputs:
			logging.warning("No input defined for block %s" % blknm)
			return
		ip, district, itype = self.inputs[blknm]
		district.PlaceTrain(blknm)

	def RemoveTrain(self, blknm):
		print("rr remove train")
		if blknm not in self.inputs:
			logging.warning("No input defined for block %s" % blknm)
			print("block %s not found" % blknm)
			return
		ip, district, itype = self.inputs[blknm]
		district.RemoveTrain(blknm)

	def SetAspect(self, signame, aspect):
		print("set aspect for signal %s" % signame)
		if signame not in self.outputs:
			print("not in outputs")
			logging.warning("No output defined for signal %s" % signame)
			return
		op, district, otype = self.outputs[signame]
		op.SetAspect(aspect)
		district.DetermineSignalLevers()
		district.UpdateSignal(signame)

	def SetBlockDirection(self, block, direction):
		if block not in self.inputs:
			logging.warning("No input defined for block %s" % block)
			return
		ip, district, itype = self.inputs[block]
		ip.SetDirection(direction)

	def SetIndicator(self, indname, state):
		if indname not in self.outputs:
			logging.warning("no output defined for indicator %s" % indname)
			return
		op, district, otype = self.outputs[indname]
		op.SetStatus(state!=0)
		district.UpdateIndicator(indname)

	def SetRelay(self, relayname, state):
		if relayname not in self.outputs:
			logging.warning("no output defined for relay %s" % relayname)
			return
		op, district, otype = self.outputs[relayname]
		op.SetStatus(state!=0)
		district.UpdateRelay(relayname)

	def SetHandSwitch(self, hsname, state):
		if hsname not in self.outputs:
			logging.warning("no output defined for handswitch %s" % hsname)
			return
		op, district, otype = self.outputs[hsname]
		op.SetStatus(state!=0)
		district.UpdateHandSwitch(hsname)

	def SetSwitchLock(self, toname, state):
		if toname not in self.outputs:
			logging.warning("no output defined for turnout %s" % toname)
			return
		op, district, otype = self.outputs[toname]
		op.SetLock(state)
		district.RefreshOutput(toname)

	def SetOutPulseTo(self, oname, state):
		if oname not in self.outputs:
			logging.warning("no pulsed output defined for %s" % oname)
			return
		op, district, otype = self.outputs[oname]
		op.SetOutPulseTo(state)
		district.RefreshOutput(oname)

	def SetOutPulseNXB(self, oname):
		if oname not in self.outputs:
			logging.warning("no pulsed output defined for %s" % oname)
			return
		op, district, otype = self.outputs[oname]
		op.SetOutPulseNXB()
		district.RefreshOutput(oname)

	def RefreshOutput(self, oname):
		if oname not in self.outputs:
			logging.warning("no output defined for %s" % oname)
			return
		district = self.outputs[oname][1]
		district.RefreshOutput(oname)

	def RefreshInput(self, iname):
		if iname not in self.inputs:
			logging.warning("No input defined for %s" % iname)
			return
		district, itype = self.inputs[iname][1:3]
		district.RefreshInput(iname, itype)

	def EvaluateNXButtons(self, bEntry, bExit):
		if bEntry not in self.outputs:
			logging.warning("No output defined for %s" % bEntry)
			return
		district = self.outputs[bEntry][1]
		district.EvaluateNXButtons(bEntry, bExit)

	def EvaluateNXButton(self, btn):
		if btn not in self.outputs:
			logging.warning("No output defined for %s" % btn)
			return
		district = self.outputs[btn][1]
		district.EvaluateNXButton(btn)

	def allIO(self):
		for d in self.districts.values():
			d.OutIn()

	def RailroadEvent(self, event):
		self.cbEvent(event)
