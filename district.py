import wx

# district node addresses
YARD      = 0x11;
KALE      = 0x12;
EASTJCT   = 0x13;
CORNELL   = 0x14;
YARDSW    = 0x15;
PARSONS   = 0x21;
PORTA     = 0x22;
PORTB     = 0x23;
LATHAM    = 0x31;
CARLTON   = 0x32;
DELL      = 0x41;
FOSS      = 0x42;
HYDEJCT   = 0x51;
HYDE      = 0x52;
SHORE     = 0x61;
KRULISH   = 0x71;
NASSAUW   = 0x72;
NASSAUE   = 0x73;
NASSAUNX  = 0x74;
BANK      = 0x81;
CLIVEDEN  = 0x91;
GREENMTN  = 0x92;
CLIFF     = 0x93;
SHEFFIELD = 0x95;

class District(wx.Panel):
	signal = 0
	turnout = 1
	indicator = 2
	relay = 3
	handswitch = 4
	route = 5
	block = 6
	typeLabels = [ "Signals", "Turnouts", "Indicators", "Stop Relays", "Handswitches", "Routes", "Blocks" ]

	def __init__(self, parent, name):
		wx.Panel.__init__(self, parent, wx.ID_ANY)
		self.name = name
		self.rr = parent
		self.outputMap = {}
		self.inputMap = {}
		self.inputTypes = {}

		self.verbose = self.rr.verbose

		self.olist = wx.ListCtrl(self, wx.ID_ANY, pos=(0, 0), size=(260, 300), style=wx.LC_REPORT)
		self.olist.InsertColumn(0, "Output")
		self.olist.SetColumnWidth(0, 100)
		self.olist.InsertColumn(1, "Value", wx.LIST_FORMAT_CENTER)
		self.olist.SetColumnWidth(1, 50)
		self.olist.InsertColumn(2, "Type", wx.LIST_FORMAT_CENTER)
		self.olist.SetColumnWidth(2, 90)
 
		self.ilist = wx.ListCtrl(self, wx.ID_ANY, pos=(330, 0), size=(260, 300), style=wx.LC_REPORT)
		self.ilist.InsertColumn(0, "Input")
		self.ilist.SetColumnWidth(0, 100)
		self.ilist.InsertColumn(1, "Value", wx.LIST_FORMAT_CENTER)
		self.ilist.SetColumnWidth(1, 50)
		self.ilist.InsertColumn(2, "Type", wx.LIST_FORMAT_CENTER)
		self.ilist.SetColumnWidth(2, 90)

		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.inputDClick, self.ilist)

	def inputDClick(self, evt):
		# TODO - only allow this in simulation mode
		index = evt.Index
		print("Double click item %d" % index)
		if index == wx.NOT_FOUND:
			print("Not found - returning")
			return

		iname = self.ilist.GetItemText(index, 0)
		itype = self.inputTypes[index]
		cval = int(self.ilist.GetItemText(index, 1))
		nval = 1 - cval
		self.ilist.SetItem(index, 1, "%d" % nval)

		print("send rr event: %s %s %d" % (District.typeLabels[itype], iname, nval))
		if itype == District.route:
			if nval != 0:
				rrevt = self.MapRouteToTurnouts(iname)
				if rrevt is None:
					print("Unable to map route name %s to turnouts")
				else:
					self.RailroadEvent(rrevt)

		elif itype == District.block:
			self.RailroadEvent({"block": [{"name": iname, "state": nval}]})
		else:
			print("No handling of input type %s(%s)" % (District.typeLabels[itype], itype))

	def SetVerbose(self, flag=True):
		self.verbose = flag

	def AddOutputs(self, olist, oclass, otype, ix=0):
		first = True
		for oname in olist:
			oc = oclass(oname)
			self.rr.AddOutput(oc, self)
			self.olist.InsertItem(ix, oname)
			if otype == District.turnout:
				self.olist.SetItem(ix, 1, "0,U")
			else:
				self.olist.SetItem(ix, 1, "0")
			if first:
				first = False
				self.olist.SetItem(ix, 2, District.typeLabels[otype])
			self.outputMap[(oname, otype)] = (ix, oc)
			ix += 1
		return ix

	def AddInputs(self, ilist, iclass, itype, ix=0):
		first = True
		for iname in ilist:
			ic = iclass(iname)
			self.rr.AddInput(ic, self)
			self.ilist.InsertItem(ix, iname)
			self.ilist.SetItem(ix, 1, "0")
			if first:
				first = False
				self.ilist.SetItem(ix, 2, District.typeLabels[itype])
			self.inputMap[(iname, itype)] = (ix, ic)
			self.inputTypes[ix] = itype
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
		state = oc.GetLock()
		self.olist.SetItem(ix, 1, "%d,%s" % (pulseval, "L" if state != 0 else "U"))

	def DetermineSignalLever(self, lsigs, rsigs):
		lval = 0
		for sig in lsigs:
			try:
				_, oc = self.outputMap[(sig, District.signal)]
			except KeyError:
				print("Output for signal %s not found" % sig)
				oc = None
			if oc:
				lval += oc.GetAspect()

		rval = 0
		for sig in rsigs:
			try:
				_, oc = self.outputMap[(sig, District.signal)]
			except KeyError:
				print("Output for signal %s not found" % sig)
				oc = None
			if oc:
				rval += oc.GetAspect()

		if rval == 0 and lval == 0:
			return 'N'

		if rval == 0:
			return "L"

		if lval == 0:
			return 'R'

		# both non-zero - shouldn't happen, bue set to N
		return 'N'

	def UpdateIndicator(self, indname):
		try:
			ix, oc = self.outputMap[(indname, District.indicator)]
		except KeyError:
			print("Output for indicator %s in district %s not found" % (indname, self.name))
			return
		
		state = oc.GetStatus()
		self.olist.SetItem(ix, 1, "%d" % state)

	def UpdateHandSwitch(self, hsname):
		try:
			ix, oc = self.outputMap[(hsname, District.handswitch)]
		except KeyError:
			print("Output for handswitch %s in district %s not found" % (hsname, self.name))
			return
		
		state = oc.GetStatus()
		self.olist.SetItem(ix, 1, "%d" % state)

	def RailroadEvent(self, cmd):
		self.rr.RailroadEvent(cmd)
