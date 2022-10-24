import wx
import logging

from districts.hyde import Hyde
from districts.yard import Yard
from districts.latham import Latham
from districts.shore import Shore
from districts.dell import Dell

class Railroad(wx.Notebook):
	def __init__(self, frame, cbEvent, settings):
		wx.Notebook.__init__(self, frame, wx.ID_ANY, style=wx.BK_DEFAULT)
		self.frame = frame
		self.cbEvent = cbEvent
		self.settings = settings

		districtList = [
			[ "Yard", Yard ],
			[ "Latham", Latham ],
			[ "Dell", Dell ],
			[ "Shore", Shore ],
			[ "Hyde", Hyde ],
		]

		self.districts = {}
		self.outputs = {}
		self.inputs = {}
		
		for dname, dclass in districtList:
			logging.debug("Creating district %s" % dname)
			p = dclass(self, dname, self.settings)
			self.AddPage(p, dname)
			self.districts[dname] = p

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

	def SetAspect(self, signame, aspect):
		if signame not in self.outputs:
			logging.warning("No output defined for signal %s" % signame)
			return
		op, district, otype = self.outputs[signame]
		op.SetAspect(aspect)
		district.UpdateSignal(signame)

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

	def SetOutPulse(self, toname, state):
		if toname not in self.outputs:
			logging.warning("no output defined for turnout %s" % toname)
			return
		op, district, otype = self.outputs[toname]
		op.SetOutPulse(state)
		district.RefreshOutput(toname)

	def RefreshOutput(self, toname):
		if toname not in self.outputs:
			logging.warning("no output defined for turnout %s" % toname)
			return
		district = self.outputs[toname][1]
		district.RefreshOutput(toname)

	def RefreshInput(self, iname):
		if iname not in self.inputs:
			logging.warning("No input defined for %s" % iname)
			return
		district, itype = self.inputs[iname][1:3]
		district.RefreshInput(iname, itype)

	def allIO(self):
		for d in self.districts.values():
			d.OutIn()

	def RailroadEvent(self, event):
		self.cbEvent(event)
