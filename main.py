import time
import queue
import threading

from bus import Bus
from railroad import Railroad
from httpserver import NodeHTTPServer
from sktserver import SktServer

import pprint

class NodeServerMain:
	def __init__(self, cfgfn):
		tty = "COM4"
		ip = "192.168.1.138"
		port = 9000
		socketport = 9001
		busInterval = 1

		print("node initializing...")

		print("Opening bus to railroad on device %s" % tty)
		self.rrbus = Bus(tty)
		if not self.rrbus.initialized:
			print("Failed to open railroad bus on device %s.  Exiting..." % tty)
			exit(1)

		print("Starting HTTP server at address: %s:%d" % (ip, port))
		self.startHttpServer(ip, port)

		print("Starting Socket server at address: %s:%d" % (ip, socketport))
		self.socketServer = SktServer(ip, socketport)
		self.socketServer.start()

		print("Creating railroad object")
		self.railroadQ = queue.Queue(0)
		self.rr = Railroad(self.rrbus, self.railroadQ, busInterval)
		self.rr.start()

		print("Initialization completed...")

	def startHttpServer(self, ip, port):
		self.HttpCmdQ = queue.Queue(0)
		self.HttpRespQ = queue.Queue(0)
		self.serving = True
		self.nodeserver = NodeHTTPServer(ip, port, self.HttpCmdQ, self.HttpRespQ)

	def stopHttpServer(self):
		self.nodeserver.close()
		self.nodeserver.getThread().join()

	def railroadProcess(self):
		# Deal with all reports from the railroad"
		while not self.railroadQ.empty():
			try:
				cmd = self.railroadQ.get(False)			
			except queue.Empty:
				cmd = None

			if cmd is None:
				return

			print("RRQ=>(%s)" % str(cmd))
			self.socketServer.sendToAll(cmd)

	def process(self):
		self.HTTPProcess()

		self.railroadProcess()

		ns = self.socketServer.getNewSockets()	
		if ns is not None:
			print("send current status of everything to all newly joined listeners")

	def HTTPProcess(self):
		while not self.HttpCmdQ.empty():
			try:
				cmd = self.HttpCmdQ.get(False)			
			except queue.Empty:
				cmd = None

			if cmd is None:
				return

			self.HttpRespQ.put((200, b'command received'))

			print("received HTTP request: ============================================================")
			pprint.pprint(cmd)

			verb = cmd["cmd"][0].lower()

			if verb == "signal":
				signame = cmd["name"][0]
				aspect = int(cmd["state"][0])
				resp = {"signal": [signame, aspect]}
				# signal changes are echoed back to all listeners
				self.socketServer.sendToAll(resp)
				op = self.rr.GetOutput(signame)
				if op is not None: 
					op.SetAspect(aspect)
				else:
					# None happens if there are no physical signals
					# print a message just in case
					print("no output defined for signal %s" % signame)
					return

			elif verb == "turnout":
				swname = cmd["name"][0]
				status = cmd["status"][0]

				op = self.rr.GetOutput(swname)
				if op is not None:
					op.SetOutPulse(status)
				else:
					print("no output defined for turnout %s" % swname)
					return

				# the below logic is unnecessary - it makes testing easier
				resp = {"turnout": { swname : status}}
				self.socketServer.sendToAll(resp)
				if swname == "HSw3":
					resp = {"turnout": { "HSw5" : status}}
					self.socketServer.sendToAll(resp)
				elif swname == "HSw11":
					resp = {"turnout": { "HSw13" : status}}
					self.socketServer.sendToAll(resp)

			elif verb == "quit":
				print("HTTP 'quit' command received - terminating server")
				self.serving = False



	def serve_forever(self, interval):
		ticker = threading.Event()
		try:
			while not ticker.wait(interval) and self.serving:
				if self.serving:
					self.process()

		except KeyboardInterrupt:
			print("Keyboard Interrupt - exiting...")

		ticker = None

		print("Stopping HTTP Server...")
		self.stopHttpServer()

		self.socketServer.kill()

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

server = NodeServerMain("nodecfg.json")
server.serve_forever(0.25)



