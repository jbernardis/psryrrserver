import wx


class District(wx.Panel):
	signal = 0
	turnout = 1
	indicator = 2
	relay = 3
	typeLabels = [ "Signals", "Turnouts", "Indicators", "Stop Relays" ]

	def __init__(self, parent, name, address):
		wx.Panel.__init__(self, parent, wx.ID_ANY)
		self.name = name
		self.address = address
		self.rr = parent
		self.outputMap = {}

		self.verbose = self.rr.verbose

		self.olist = wx.ListCtrl(self, wx.ID_ANY, pos=(0, 0), size=(250, 300), style=wx.LC_REPORT)
		self.olist.InsertColumn(0, "Output")
		self.olist.SetColumnWidth(0, 100)
		self.olist.InsertColumn(1, "Value", wx.LIST_FORMAT_CENTER)
		self.olist.SetColumnWidth(1, 50)
		self.olist.InsertColumn(2, "Type", wx.LIST_FORMAT_CENTER)
		self.olist.SetColumnWidth(2, 80)
 
		self.ilist = wx.ListCtrl(self, wx.ID_ANY, pos=(320, 0), size=(250, 300), style=wx.LC_REPORT)
		self.ilist.InsertColumn(0, "Input")
		self.ilist.SetColumnWidth(0, 100)
		self.ilist.InsertColumn(1, "Value", wx.LIST_FORMAT_CENTER)
		self.ilist.SetColumnWidth(1, 50)
		self.ilist.InsertColumn(2, "Type", wx.LIST_FORMAT_CENTER)
		self.ilist.SetColumnWidth(2, 80)

	def SetVerbose(self, flag=True):
		self.verbose = flag

	def AddOutputs(self, olist, oclass, otype, ix=0):
		first = True
		for oname in olist:
			oc = oclass(oname)
			self.rr.AddOutput(oc, self)
			self.olist.InsertItem(ix, oname)
			self.olist.SetItem(ix, 1, "0")
			if first:
				first = False
				self.olist.SetItem(ix, 2, District.typeLabels[otype])
			self.outputMap[(oname, otype)] = (ix, oc)
			ix += 1
		return ix

	def SetTurnoutPulseLen(self, to, pl):
		if (to, District.turnout) not in self.outputMap:
			print("Turnout %s not found - unable to change pulse length" % to)
			return False

		oc = self.outputMap[(to, District.turnout)][1]
		oc.SetPulseLen(pl)

	def UpdateSignal(self, signame):
		try:
			ix, oc = self.outputMap[(signame, District.signal)]
		except KeyError:
			print("Output for signal %s in district %s not found" % (signame, self.name))
			return
		
		aspect = oc.GetAspect()
		self.olist.SetItem(ix, 1, "%d" % aspect)

	def UpdateTurnout(self, toname):
		try:
			ix, oc = self.outputMap[(toname, District.turnout)]
		except KeyError:
			print("Output for turnout %s in district %s not found" % (toname, self.name))
			return
		
		pulseval = oc.GetOutPulseValue()
		self.olist.SetItem(ix, 1, "%d" % pulseval)

	def UpdateIndicator(self, indname):
		try:
			ix, oc = self.outputMap[(indname, District.indicator)]
		except KeyError:
			print("Output for indicator %s in district %s not found" % (indname, self.name))
			return
		
		state = oc.GetStatus()
		self.olist.SetItem(ix, 1, "%d" % state)
