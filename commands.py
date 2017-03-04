from clientpy3 import *
class Player:
	def __init__(self, pos, vel):
		self.pos = pos
		self.vel = vel
	def __repr__(self):
		output = "pos: {} \nvel: {}\n".format(self.pos, self.vel)
		return output
	def __str__(self):
		output = "pos: {} \nvel: {}\n".format(self.pos, self.vel)
		return output

class MyReponse:
	def __init__(self):
		self.pos = (0,0)
		self.vel = (0,0)
		self.mines = []
		self.players = []
		self.bombs = []
	def __repr__(self):
		output = "pos: {}\nvel: {}\nmines: {}\nplayers: {}\nbombs: {}\n".format(\
				 self.pos, self.vel, self.mines, "\n".join([str(p) for p in self.players]),self.bombs)
		return output
	def update(self):
		def findInSet(response, keyword):
			index = response.index(keyword)
			cSet = []
			if response[index + 1] != '0':
				num = int(response[index + 1])
				j = 2
				while j < num + 2:
					if keyword == "PLAYERS":
						x,y,dx,dy = [float(x) for x in response[index + j:index + j + 4]]
						cSet.append(Player((x,y),(dx,dy)))
					else:
						x,y,dx,dy = [float(x) for x in response[index + j * 4 :index + (j+1) * 4]]
						cSet.append((x,y))
					j += 1
			return cSet

		r = run("STATUS").split(" ")
		self.mines = findInSet(r,"MINES")
		self.players = findInSet(r,'PLAYERS')
		self.bombs = findInSet(r,'BOMBS')
		self.pos = [float(x) for x in r[1:3]]
		self.vel = [float(x) for x in r[3:5]]
		print(r)