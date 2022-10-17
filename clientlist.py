import wx

class ClientList(wx.ListCtrl):
	def __init__(self, parent):
		wx.ListCtrl.__init__(self, parent, wx.ID_ANY, size=(200, 330), style=wx.LC_REPORT)
		self.InsertColumn(0, "IP")
		self.SetColumnWidth(0, 100)
		self.InsertColumn(1, "Port")
		self.SetColumnWidth(1, 100)
		self.clientList = []

	def AddClient(self, addr):
		if addr in self.clientList:
			return

		index = len(self.clientList)
		self.clientList.append(addr)
		self.InsertItem(index, addr[0])
		self.SetItem(index, 1, "%d" % addr[1])

	def DelClient(self, addr):
		try:
			index = self.clientList.index(addr)
		except ValueError:
			print("not in list")
			return

		print("Found as item %d in our list")
		self.DeleteItem(index)
		del(self.clientList[index])
