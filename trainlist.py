import json

class TrainList:
	def __init__(self, frame):
		self.frame = frame
		self.trains = {}
		self.count = 0

	def Update(self, train, loco, block):
		if block is None:
			return

		if train is None:
			# search for and remove the block from the table
			dellist = []
			for tr in self.trains:
				if block in self.trains[tr]["blocks"]:
					self.trains[tr]["blocks"].remove(block)
					if len(self.trains[tr]["blocks"]) == 0:
						dellist.append(tr)

			for tr in dellist:
				del(self.trains[tr])
		else:
			if train in self.trains:
				if block not in self.trains[train]["blocks"]:
					self.trains[train]["blocks"].append(block)
				if loco:
					self.trains[train]["loco"] = loco
			else:
				self.trains[train] = {"blocks": [block], "loco": loco}

	def FindTrainInBlock(self, block):
		for tr, trinfo in self.trains.items():
			if block in trinfo["blocks"]:
				return tr, trinfo["loco"]

		return None, None

	def RenameTrain(self, oname, nname, oloco, nloco):
		if oname == nname and oloco == nloco:
			return False
			
		if oname != nname:
			if oname not in self.trains:
				# we can't do anything if we can't find the original record
				return False

			if nname in self.trains:
				# in this case, we retain the old information, but merge the block lists
				for b in self.trains[oname]["blocks"]:
					if b not in self.trains[nname]["blocks"]:
						self.trains[nname]["blocks"].append(b)
			else:
				self.trains[nname] = self.trains[oname]

			del(self.trains[oname])

		if nloco is not None:
			self.trains[nname]["loco"] = nloco

		return True

	def GetSetTrainCmds(self, train=None):
		for tr, trinfo in self.trains.items():
			if train is None or train == tr:
				loco = trinfo["loco"]
				blocks = trinfo["blocks"]
				clist = []
				for b in blocks:
					clist.append({"block": b, "name": tr, "loco": loco})
				yield({"settrain": clist})
