from clientpy3 import *
class Player:
	def __init__(self, pos, vel):
		self.pos = pos
		self.vel = vel
	def __repr__(self):
		oPos = [round(x, 2) for x in self.pos]
		oVel = [round(x, 2) for x in self.vel]
		output = "pos: {} \nvel: {}\n".format(oPos, oVel)
		return output
	def __str__(self):
		oPos = [round(x, 2) for x in self.pos]
		oVel = [round(x, 2) for x in self.vel]
		output = "pos: {} \nvel: {}\n".format(oPos, oVel)
		return output

class MyReponse:
	def __init__(self):
		self.pos = (0,0)
		self.vel = (0,0)
		self.mines = []
		self.players = []
		self.bombs = []
	def __repr__(self):
		'''output = "pos: {}\nvel: {}\nmines: {}\nplayers:\n{}\nbombs: {}\n".format(\
				 self.pos, self.vel, self.mines, "\n".join([str(p) for p in self.players]),self.bombs)
			'''
		output = "pos: {}\nvel: {}\nmines: {}\nplayers:{}\nbombs: {}\n".format(\
				 self.pos, self.vel, len(self.mines), len(self.players),len(self.bombs))
		return output
	def update(self):
		def findInSet(response, keyword):
			index = response.index(keyword)
			cSet = []
			if response[index + 1] != '0':
				num = int(response[index + 1])
				j = 0
				while j < num:
					if keyword == "PLAYERS":
						x,y,dx,dy = [float(x) for x in response[index + 2+ j * 4:index + 2 + (j + 1)*4]]
						cSet.append(Player((x,y),(dx,dy)))
					else:
						x,y = [float(x) for x in response[index + 2+ j * 2 :index + 2+ (j + 1) * 2]]
						cSet.append((x,y))
					j += 1
			return cSet

		r = run("STATUS").split(" ")
		try:
			self.mines = findInSet(r,"MINES")
			self.players = findInSet(r,'PLAYERS')
			self.bombs = findInSet(r,'BOMBS')
			self.pos = [float(x) for x in r[1:3]]
			self.vel = [float(x) for x in r[3:5]]
		except:
			print("ERROR: {}".format(r))