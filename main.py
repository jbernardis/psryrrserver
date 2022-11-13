import wx
import wx.lib.newevent

import logging
logging.basicConfig(filename='pydispatch.log', filemode='w', format='%(asctime)s %(message)s', level=logging.INFO)
import json
import socket

from settings import Settings
from bus import RailroadMonitor
from railroad import Railroad
from httpserver import HTTPServer
from sktserver import SktServer

from clientlist import ClientList
from trainlist import TrainList
from iodisplay import IODisplay

(HTTPMessageEvent, EVT_HTTPMESSAGE) = wx.lib.newevent.NewEvent()  
(RailroadEvent, EVT_RAILROAD) = wx.lib.newevent.NewEvent()  
(SocketEvent, EVT_SOCKET) = wx.lib.newevent.NewEvent()  
(IOClearEvent, EVT_CLEARIO) = wx.lib.newevent.NewEvent()  
(IOTextEvent, EVT_TEXTIO) = wx.lib.newevent.NewEvent()  

class MainFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, size=(900, 800), style=wx.DEFAULT_FRAME_STYLE)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		logging.info("pydispatch starting")

		hostname = socket.gethostname()
		self.ip = socket.gethostbyname(hostname)

		self.clients = {}

		self.settings = Settings()
		self.SetTitle("PSRY Railroad Server    IP:  %s   Listening on port:  %d    Broadcasting on port:  %d" % 
				(self.ip, self.settings.serverport, self.settings.socketport))

		logging.info("Creating railroad object")
		self.rr = Railroad(self, self.rrEventReceipt, self.settings) #, self.rrbus, self.rrEventReceipt, self.settings.busInterval)

		self.clientList = ClientList(self)
		self.trainList = TrainList(self)
		self.ioDisplay = IODisplay(self)

		vsz = wx.BoxSizer(wx.VERTICAL)
		hsz = wx.BoxSizer(wx.HORIZONTAL)

		hsz.AddSpacer(20)
		hsz.Add(self.rr)
		hsz.AddSpacer(10)
		vsz2 = wx.BoxSizer(wx.VERTICAL)
		vsz2.Add(self.clientList)
		vsz2.AddSpacer(10)
		vsz2.Add(self.trainList)
		hsz.Add(vsz2)
		hsz.AddSpacer(20)

		vsz.AddSpacer(20)
		vsz.Add(hsz)
		vsz.AddSpacer(20)
		hsz2 = wx.BoxSizer(wx.HORIZONTAL)
		hsz2.AddSpacer(20)
		hsz2.Add(self.ioDisplay)
		hsz2.AddSpacer(20)
		vsz.Add(hsz2)
		vsz.AddSpacer(20)

		self.SetSizer(vsz)
		self.Layout()
		self.Fit()
		
		wx.CallAfter(self.Initialize)

	def Initialize(self):
		self.rr.Initialize()

		logging.info("Opening a railroad monitoring thread on device %s" % self.settings.tty)
		self.rrMonitor = RailroadMonitor(self.settings.tty, self.rr, self.settings)
		if not self.rrMonitor.initialized:
			logging.error("Failed to open railroad bus on device %s.  Exiting..." % self.settings.tty)
			exit(1)
		self.rrMonitor.start()

		self.dispServer = HTTPServer(self.ip, self.settings.serverport, self.dispCommandReceipt)
		self.Bind(EVT_HTTPMESSAGE, self.onHTTPMessageEvent)
		self.Bind(EVT_RAILROAD, self.onRailroadEvent)
		self.Bind(EVT_SOCKET, self.onSocketEvent)
		self.Bind(EVT_CLEARIO, self.onClearIOEvent)
		self.Bind(EVT_TEXTIO, self.onTextIOEvent)

		logging.info("Starting Socket server at address: %s:%d" % (self.ip, self.settings.socketport))
		self.socketServer = SktServer(self.ip, self.settings.socketport, self.socketEventReceipt)
		self.socketServer.start()

	def ClearIO(self):
		evt = IOClearEvent()
		wx.QueueEvent(self, evt)

	def onClearIOEvent(self, evt):
		self.ioDisplay.ClearIO()

	def ShowText(self, otext, itext, line, lines):
		evt = IOTextEvent(otext=otext, itext=itext, line=line, lines=lines)
		wx.QueueEvent(self, evt)

	def onTextIOEvent(self, evt):
		self.ioDisplay.ShowText(evt.otext, evt.itext, evt.line, evt.lines)

	def socketEventReceipt(self, cmd):
		evt = SocketEvent(data=cmd)
		wx.QueueEvent(self, evt)

	def onSocketEvent(self, evt):
		for cmd, parms in evt.data.items():
			if cmd == "newclient":
				addr = parms["addr"]
				skt = parms["socket"]
				sid = parms["SID"]
				logging.info("New Client connecting from address: %s:%d" % (addr))
				self.socketServer.sendToOne(skt, addr, {"sessionID": sid})
				self.clients[addr] = [skt, sid]
				self.refreshClient(addr, skt)
				self.clientList.AddClient(addr, sid)

			elif cmd == "delclient":
				addr = parms["addr"]
				logging.info("Disconnecting Client from address: %s:%d" % (addr))
				try:
					del self.clients[addr]
				except KeyError:
					pass
				self.clientList.DelClient(addr)

	def refreshClient(self, addr, skt):
		for m in self.rr.GetCurrentValues():
			self.socketServer.sendToOne(skt, addr, m)
		for m in self.trainList.GetSetTrainCmds():
			self.socketServer.sendToOne(skt, addr, m)

	def rrEventReceipt(self, cmd, addr=None, skt=None):
		evt = RailroadEvent(data=cmd, addr=addr, skt=skt)
		wx.QueueEvent(self, evt)

	def onRailroadEvent(self, evt):
		logging.info("Railroad event: %s" % json.dumps(evt.data))

		for cmd, parms in evt.data.items():
			if cmd == "refreshoutput":
				for oname in parms:
					self.rr.RefreshOutput(oname)
			elif cmd == "refreshinput":
				for iname in parms:
					self.rr.RefreshInput(iname)
			else:
				self.socketServer.sendToAll(evt.data)

	def dispCommandReceipt(self, cmd):
		evt = HTTPMessageEvent(data=cmd)
		wx.QueueEvent(self, evt)

	def onHTTPMessageEvent(self, evt):
		logging.info("HTTP Request: %s" % json.dumps(evt.data))
		print("HTTP Request: %s" % json.dumps(evt.data))
		verb = evt.data["cmd"][0]

		if verb == "signal":
			signame = evt.data["name"][0]
			aspect = int(evt.data["aspect"][0])
			resp = {"signal": [{"name": signame, "aspect": aspect}]}
			# signal changes are always echoed back to all listeners
			self.socketServer.sendToAll(resp)
			self.rr.SetAspect(signame, aspect)

		elif verb == "settrain":
			try:
				trn = evt.data["name"][0]
			except:
				trn = None
			try:
				loco = evt.data["loco"][0]
			except:
				loco = None
			block = evt.data["block"][0]
			# train information is always echoed back to all listeners

			if trn and trn.startswith("??"):
				# this is an unknown train - see if we have a known train in the same block
				ntrn, nloco = self.trainList.FindTrainInBlock(block)
				if ntrn:
					trn = ntrn
				if nloco:
					loco = nloco

			resp = {"settrain": [{"name": trn, "loco": loco, "block": block}]}
			self.socketServer.sendToAll(resp)

			self.trainList.Update(trn, loco, block)

		elif verb == "renametrain":
			try:
				oname = evt.data["oldname"][0]
			except:
				oname = None
			try:
				oloco = evt.data["oldloco"][0]
			except:
				oloco = None
			try:
				nname = evt.data["newname"][0]
			except:
				nname = None
			try:
				nloco = evt.data["newloco"][0]
			except:
				nloco = None

			if self.trainList.RenameTrain(oname, nname, oloco, nloco):
				for cmd in self.trainList.GetSetTrainCmds(nname):
					self.socketServer.sendToAll(cmd)

		elif verb == "blockdir":
			block = evt.data["block"][0]
			direction = evt.data["dir"][0]
			self.rr.SetBlockDirection(block, direction)

		elif verb == "handswitch":
			hsname = evt.data["name"][0]
			stat = int(evt.data["status"][0])

			self.rr.SetHandSwitch(hsname, stat)
			# handswitch information is always echoed to all listeners
			resp = {"handswitch": [{"name": hsname, "state": stat}]}
			self.socketServer.sendToAll(resp)

		elif verb == "turnout":
			swname = evt.data["name"][0]
			status = evt.data["status"][0]

			self.rr.SetOutPulseTo(swname, status)

			# turnouts are not normally echoed back to listeners.  Instead,
			# the turnout information that the railroad reponds with is sent
			# back to listeners to convey this information
			if self.settings.echoTurnout and self.settings.simulation:
				self.rr.GetInput(swname).SetState(status)

		elif verb == "nxbutton":
			bentry = evt.data["entry"][0]
			bexit = evt.data["exit"][0]
			self.rr.SetOutPulseNXB(bentry)
			self.rr.SetOutPulseNXB(bexit)

			# nxbuttons are not normally echoed back to listeners.  Instead,
			# the turnout information that the railroad reponds with is sent
			# back to listeners to convey this information
			if self.settings.echoTurnout and self.settings.simulation:
				self.rr.EvaluateNXButtons(bentry, bexit)

		elif verb == "turnoutlock":
			swname = evt.data["name"][0]
			status = int(evt.data["status"][0])

			self.rr.SetSwitchLock(swname, status)
			# turnoutlock information is always echoed to all listeners
			resp = {"turnoutlock": [{ "name": swname, "state": status}]}
			self.socketServer.sendToAll(resp)

		elif verb == "indicator":
			indname = evt.data["name"][0]
			value = int(evt.data["value"][0])

			self.rr.SetIndicator(indname, value)
			# indicator information is always echoed to all listeners
			resp = {"indicator": [{ "name": indname, "value": value}]}
			self.socketServer.sendToAll(resp)

		elif verb == "relay":
			relay = evt.data["block"][0]+".srel"
			status = int(evt.data["status"][0])

			self.rr.SetRelay(relay, status)

		elif verb == "refresh":
			sid = int(evt.data["SID"][0])
			for addr, data in self.clients.items():
				if data[1] == sid:
					skt = data[0]
					break
			else:
				logging.info("session %s not found" % sid)
				return
			self.refreshClient(addr, skt)

		elif verb == "placetrain":
			try:
				blknm = evt.data["block"][0]
			except:
				print("block missing")
				return
			self.rr.PlaceTrain(blknm)

		elif verb == "removetrain":
			try:
				blknm = evt.data["block"][0]
			except:
				print("block missing")
				return
			self.rr.RemoveTrain(blknm)

		elif verb == "quit":
			logging.info("HTTP 'quit' command received - terminating")
			self.Shutdown()

	def onClose(self, _):
		self.Shutdown()

	def Shutdown(self):
		logging.info("Killing socket server...")
		self.socketServer.kill()

		logging.info("killing HTTP server...")
		self.dispServer.close()

		logging.info("closing bus to railroad...")
		try:
			self.rrMonitor.kill()
		except:
			pass
		try:
			self.rrbus.close()
		except:
			pass

		logging.info("exiting...")
		self.Destroy()

class App(wx.App):
	def OnInit(self):
		self.frame = MainFrame()
		self.frame.Show()
		return True

app = App(False)
app.MainLoop()

