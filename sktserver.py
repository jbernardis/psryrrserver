import threading
import socket
import select
import json

class SktServer (threading.Thread):
	def __init__(self, ip, port, cbEvent):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.isRunning = False
		self.endOfLife = False
		self.cbEvent = cbEvent
		self.socketLock = threading.Lock()
		self.sockets = []
		print("Starting socket server at address: %s:%d" % (ip, port))

	def getSockets(self):
		return [x for x in self.sockets]

	def kill(self):
		self.isRunning = False
		self.join()

	def isKilled(self):
		return self.endOfLife

	def sendToAll(self, msg):
		with self.socketLock:
			tl = [x for x in self.sockets]
		for skt, addr in tl:
			self.sendToOne(skt, addr, msg)
			
	def sendToOne(self, skt, addr, msg):
			try:
				m = json.dumps(msg).encode()
			except:
				try:
					m = msg.encode()
				except:
					m = msg
			try:
				nbytes = len(m).to_bytes(2, "little")
				skt.send(nbytes)
				skt.send(m)
			except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
				self.deleteSocket(addr)

	def deleteSocket(self, addr):
		with self.socketLock:
			for i in range(len(self.sockets)):
				if self.sockets[i][1] == addr:
					del(self.sockets[i])
					print("Disconnecting socket client at %s" % str(addr))
					return

	def run(self):
		self.isRunning = True
		addr = (self.ip, self.port)
		s = socket.create_server(addr)
		s.listen()
		slist = [s]

		while self.isRunning:
			readable, _, _ = select.select(slist, [], [], 1)
			if s in readable:
				skt, addr = s.accept()
				print("Subscription from address %s" % str(addr))
				with self.socketLock:
					self.sockets.append((skt, addr))
					self.cbEvent({"newclient": {"socket": skt, "addr": addr}})

		for skt in self.sockets:
			skt[0].close()

		self.endOfLife = True
