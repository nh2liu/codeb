from rObject import *
import time
import threading
import utility
import copy
import math

stop = 1

def main():
    updateThread = threading.Thread(target = statusUpdate)
    updateThread.start()
    # x = int(input())
    # y = int(input())
    # utility.movb((x,y),False)
    utility.findAcc()
    while True:
    	# time.sleep(0.5)
    	# utility.bomb()
        c = input()
        if c == "move":
            x = int(input())
            y = int(input())
            utility.movb((x,y),False)
        elif c == "bomb":
            utility.bomb()


def statusUpdate():
	while stop:
		r.update()
		print(r)
		time.sleep(5)

def protect():
	mines = copy.deepcopy(r.allMines)
	currentPos = r.pos
	greedyPath = []
	while len(mines):
		nxt = min(mines, key = lambda x:distance(currentPos, x[1:3]))
		greedyPath.append(nxt)
		currentPos = nxt
		mines.remove(nxt)
	for mine in greedyPath:
		currentPos = r.pos
		while distance(mine, r.pos) > 10:
			k = moveb(mine, True)
			if k:
				moveb(mine, False)
				continue

def distance(c1, c2):
	return (c1[0] - c2[0])**2 + (c1[1] - c2[1])**2

def strayToMine(mine):
	curPos = copy.deepcopy(r.pos)
	moveb(mine, False)
	k = moveb(curPos, True)
	if k:
		strayToMine(k[1:3])
	moveb(curPos, False)

def strategy():
    r.update()
    bounds = moveBoundaries()
    scanPortion(boundsTuple)

def scanPortion(boundsTuple):
    bounds = boundsTuple[0]
    xlen = boundsTuple[1]
    ylen = boundsTuple[2]
    cornerType = 'topleft'
    targCorner = bounds['topleft']
    distanceToCorner = pointDistance(r.pos, targCorner)
    for k, v in bounds.items():
        dis = pointDistance(v, r.pos)
        if dis < distanceToCorner:
            targCorner = v
            cornerType = k
            distanceToCorner = dis

    movb(targCorner, True)
    while(distanceToCorner > r.config['visionradius']):
        distanceToCorner = pointDistance(r.pos, targCorner)
        for mine in r.mines:
            if mine[0] != "goose":
                strayToMine(mine)
        if len(r.mines) > 0:
            movb(targPos, True)

    top, left = False, False
    if cornerType[0:3] == 'top':
        top = True
    else:
        top = False

    horizontalHops = None
    if cornerType[3:] == "left":
        left = True
        horizontalHops = (bounds['topright'][0] - targCorner[0])/(r.config['visionradius']*2)
    else:
        horizontalHops = (targCorner[0] - bounds['topleft'][0]) /(r.config['visionradius']*2)
        left = False

    
    i = 0
    while i < horizontalHops:
        targPos = None
        if top:
            targPos = (r.pos[0], r.pos[0] - ylen)
            movb(targPos, True)
        else:
            targPos = (r.pos[0], r.pos[0] + ylen)
            movb(targPos, True)

        distanceToTopBottom = pointDistance(r.pos, targPos)

        while(distanceToTopBottom > r.config['captureradius']):
            for mine in r.mines:
                if mine[0] != "goose":
                    strayToMine(mine)
            if len(r.mines) > 0:
                movb(targPos, True)

        if left:
            nextPos = (r.pos[0] + 2*r.config['visionradius'], r.pos[1])
            movb(nextPos, False)
        else:
            nextPos = (r.pos[0] - 2*r.config['visionradius'], r.pos[1])
            movb(nextPos, False)

        i += 1

    protect()


def pointDistance(p1, p2):
    return math.sqrt((p1[0] - p2[0])*(p1[0] - p2[0]) + (p1[1] - p2[1])*(p1[1] - p2[1]))


# def moveToCorner(currentPos, bounds):
#     cornerType = {}

#     def pointDistance(p1, p2):
#         return math.sqrt((p1[0] - p2[0])*(p1[0] - p2[0]) + (p1[1] - p2[1])*(p1[1] - p2[1]))
    
#     topleft = bounds[0]
#     cornerType['topleft'] = (pointDistance(currentPos, topleft), topleft)
#     topright = (topleft[0] + bounds[1], topleft[1])
#     cornerType['topright'] = (pointDistance(currentPos, topright), topright)
#     botleft = (topleft[0], topleft[1] + bounds[2])
#     cornerType['botleft'] = (pointDistance(currentPos, botleft), botleft)
#     botright = (topleft[0] + bounds[2], topleft[1] + bounds[2])
#     cornerType['botright'] = (pointDistance(currentPos, botright), botright)

#     minCornerType = 'topleft'
#     minDist = cornerType['topleft'][0]
#     for k, v in cornerType.items():
#         if v[0] < minDist:
#             minCornerType = k

#     #movb(cornerType[minCornerType][1])
#     return minCornerType


def moveBoundaries():
    width = r.config['mapwidth']
    height = r.config['mapheight']
    xrate = 0
    yrate = 0.5
    xlen = 0.5
    ylen = 0.5

    corners = {}
    corners['topleft'] = (xrate*width, yrate*height)
    corners['topright'] = (xrate*width + xlen*width, yrate*height)
    corners['botleft'] = (xrate*width, yrate*height + ylen*height)
    corners['botright'] = (xrate*width + xlen*width, yrate*height + ylen*height)
    return (corners, xlen*width, ylen*height)

def statusUpdate():
    while True:
        time.sleep(0.05)
        r.update()
        # print(r)

if __name__ == "__main__":
	main()
