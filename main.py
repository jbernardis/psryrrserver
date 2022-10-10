import wx
import wx.lib.newevent

from settings import Settings
from bus import RailroadMonitor
from railroad import Railroad
from httpserver import HTTPServer
from sktserver import SktServer

import pprint

(HTTPMessageEvent, EVT_HTTPMESSAGE) = wx.lib.newevent.NewEvent()  
(RailroadEvent, EVT_RAILROAD) = wx.lib.newevent.NewEvent()  



class MainFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, size=(900, 800), style=wx.DEFAULT_FRAME_STYLE)
		self.Bind(wx.EVT_CLOSE, self.onClose)

		self.settings = Settings()

		print("Creating railroad object")
		self.rr = Railroad(self, self.rrEventReceipt) #, self.rrbus, self.rrEventReceipt, self.settings.busInterval)

		print("Opening a railroad monitoring thread on device %s" % self.settings.tty)
		self.rrMonitor = RailroadMonitor(self.settings.tty, self.rr)
		if not self.rrMonitor.initialized:
			print("Failed to open railroad bus on device %s.  Exiting..." % self.settings.tty)
			exit(1)
		self.rrMonitor.start()

		self.dispServer = HTTPServer(self.settings.ip, self.settings.serverport, self.dispCommandReceipt)
		self.Bind(EVT_HTTPMESSAGE, self.onHTTPMessageEvent)
		self.Bind(EVT_RAILROAD, self.onRailroadEvent)

		print("Starting Socket server at address: %s:%d" % (self.settings.ip, self.settings.socketport))
		self.socketServer = SktServer(self.settings.ip, self.settings.socketport, self.socketEventReceipt)
		self.socketServer.start()

		vsz = wx.BoxSizer(wx.VERTICAL)
		hsz = wx.BoxSizer(wx.HORIZONTAL)

		vsz.AddSpacer(20)
		vsz.Add(self.rr)
		vsz.AddSpacer(20)

		hsz.AddSpacer(20)
		hsz.Add(vsz)
		hsz.AddSpacer(20)

		self.SetSizer(hsz)
		self.Layout()
		self.Fit()

	def socketEventReceipt(self, cmd):
		print("socket event")
		pprint.pprint(cmd)

	def rrEventReceipt(self, cmd):
		#print("Main Frame Received railroad event")
		#pprint.pprint(cmd)
		evt = RailroadEvent(data=cmd)
		wx.QueueEvent(self, evt)

	def onRailroadEvent(self, evt):
		print("Railroad event handler")
		pprint.pprint(evt.data)
		cmd = evt.data["cmd"]
		if cmd == "refreshturnout":
			toname = evt.data["name"]
			self.rr.RefreshTurnout(toname)

	def dispCommandReceipt(self, cmd):
		print("Received display command")
		pprint.pprint(cmd)
		evt = HTTPMessageEvent(data=cmd)
		wx.QueueEvent(self, evt)

	def onHTTPMessageEvent(self, evt):
		print("HTTP message event handler: ")
		pprint.pprint(evt.data)
		verb = evt.data["cmd"][0]

		if verb == "signal":
			signame = evt.data["name"][0]
			aspect = int(evt.data["aspect"][0])
			resp = {"signal": [{"name": signame, "aspect": aspect}]}
			# signal changes are echoed back to all listeners
			self.socketServer.sendToAll(resp)
			self.rr.SetAspect(signame, aspect)

		elif verb == "settrain":
			try:
				trn = evt.data["name"][0]
			except:
				trn = None
			try:
				loco = evt["loco"][0]
			except:
				loco = None
			block = evt.data["block"][0]
			# train information is echoed back to all listeners
			resp = {"settrain": [{"name": trn, "loco": loco, "block": block}]}
			self.socketServer.sendToAll(resp)

		elif verb == "lock":
			lkname = evt.data["name"][0]
			stat = int(evt.data["status"][0])
			resp = {"lock": [{"name": lkname, "state": stat}]}

			if self.settings.echoLock:
				self.socketServer.sendToAll(resp)
			self.rr.SetIndicator(lkname, stat)

		elif verb == "turnout":
			swname = evt.data["name"][0]
			status = evt.data["status"][0]

			self.rr.SetOutPulse(swname, status)

			if self.settings.echoTurnout:
				resp = {"turnout": [{ "name": swname, "state": status}]}
				self.socketServer.sendToAll(resp)

		elif verb == "quit":
			print("HTTP 'quit' command received - terminating")
			self.Shutdown()

	def onClose(self, _):
		self.Shutdown()

	def Shutdown(self):
		print("Killing socket server...")
		self.socketServer.kill()

		print("killing HTTP server...")
		self.dispServer.close()

		print("closing bus to railroad...")
		try:
			self.rr.kill()
		except:
			pass
		try:
			self.rrbus.close()
		except:
			pass

		print("exiting...")
		self.Destroy()

class App(wx.App):
	def OnInit(self):
		self.frame = MainFrame()
		self.frame.Show()
		return True

app = App(False)
app.MainLoop()

