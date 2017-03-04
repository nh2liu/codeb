from rObject import *
import time
import threading
import utility
import copy

stop = 1

def main():
	updateThread = threading.Thread(target = statusUpdate)
	updateThread.start()
	'''
	while True:
		x = int(input())
		y = int(input())
		utility.movb((x,y))
		if x == "stop":
			stop = 0
			break
		if x == "cal":
			utility.calibrateAcc()
	'''
def statusUpdate():
	while stop:
		r.update()
		print(r)
		time.sleep(5)


if __name__ == "__main__":
	main()

def protect():
	mines = copy.deepcopy(r.mines)
	currentPos = r.pos
	greedyPath = []
	while len(mines):
		nxt = min(mines, lambda x:distance(currentPos, x))
		greedyPath.append(nxt)
		currentPos = nxt
		mines.remove(nxt)
	for mine in greedyPath:
		moveb(mine)

def distance(c1, c2):
	return (c1[0] - c2[0])**2 + (c1[1] - c2[1])**2