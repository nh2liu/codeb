from rObject import *
import time
import threading
from utility import *
import copy
import math
import random
stop = 1

def main():
    updateThread = threading.Thread(target = statusUpdate)
    updateThread.start()
    time.sleep(1)
    strategyThread = threading.Thread(target = strategy)
    strategyThread.start()
    # while True:
    #     x = input()
    #     if x == "stop":
    #         stop = 0
    #         break
    #     if x == "cal":
    #         utility.calibrateAcc()
    # findAcc()
    while True:
    	# time.sleep(0.5)
    	# utility.bomb()
        c = input()
        if c == "move":
            x = int(input())
            y = int(input())
            # utility.movb((x,y),False)
            movb((x,y),False)
        elif c == "bomb":
            bomb()


def strategy():
    findAcc()
    bounds = moveBoundaries()
    scanPortion(bounds)

def scanPortion(boundsTuple):
    bounds = boundsTuple[0]
    xlen = boundsTuple[1]
    ylen = boundsTuple[2]
    cornerType = 'topleft'
    targCorner = bounds['topleft']
    distanceToCorner = mapDist(r.pos, targCorner)
    for k, v in bounds.items():
        dis = mapDist(v, r.pos)
        if dis < distanceToCorner:
            targCorner = v
            cornerType = k
            distanceToCorner = dis
    print("First target corner " + str(targCorner))

    movb(targCorner, True)
    while(distanceToCorner > r.config['visionradius']):
        distanceToCorner = mapDist(r.pos, targCorner)
        for mine in r.mines:
            if mine[0] != username:
                strayToMine(mine)
        if len(r.mines) > 0:
            movb(targCorner, True)

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
    while i <= horizontalHops and stop:
        targPos = None
        k = None
        if top:
            targPos = (r.pos[0], r.pos[1] + ylen)
            movb(targPos, True)
        else:
            targPos = (r.pos[0], r.pos[1] - ylen)
            movb(targPos, True)

        distanceToTopBottom = mapDist(r.pos, targPos)

        while(distanceToTopBottom > r.config['visionradius']):
            for mine in r.mines:
                if mine[0] != username:
                    strayToMine(mine)
            if len(r.mines) > 0:
                movb(targPos, True)

            distanceToTopBottom = mapDist(r.pos, targPos)

        top = not top

        if left:
            nextX = r.pos[0] + 2*r.config['visionradius']
            if nextX > r.config['mapwidth']:
                nextX = nextX - r.config['mapwidth']
        else:
            nextX = r.pos[0] - 2*r.config['visionradius']
            if nextX < 0:
                nextX = r.config['mapwidth'] + nextX

        print("LEFT " + str(left) + " NEXT X " + str(nextX))
        nextPos = (nextX, r.pos[1])
        k = movb(nextPos, True)
        if k != None and k != False:
            strayToMine(k)
        i += 1
    
    while stop:
        protect()


def protect():
    mines = copy.deepcopy(r.allMines)
    currentPos = r.pos
    greedyPath = []
    while len(mines):
        nxt = min(mines, key = lambda x:mapDist(currentPos, x[1:3]))
        greedyPath.append(nxt)
        currentPos = nxt[1:3]
        mines.remove(nxt)
    for mine in greedyPath:
        strayToMine(mine)

def strayToMine(mine):
    mine = mine[1:3]
    #curPos = copy.deepcopy(r.pos)
    k = movb(mine, False)
    i = 0
    while (k == False and i < 3):
        print('here ' + str(i) + str(k))
        k = movb(mine, False)
        i += 1

    # k = movb(curPos, True)
    '''
    print("before")
    if k:
        strayToMine(k)
    print('after')
    movb(curPos, False)
    '''

#def scanStrat():
#    send()
# def moveToCorner(currentPos, bounds):
#     cornerType = {}

#     def mapDist(p1, p2):
#         return math.sqrt((p1[0] - p2[0])*(p1[0] - p2[0]) + (p1[1] - p2[1])*(p1[1] - p2[1]))
    
#     topleft = bounds[0]
#     cornerType['topleft'] = (mapDist(currentPos, topleft), topleft)
#     topright = (topleft[0] + bounds[1], topleft[1])
#     cornerType['topright'] = (mapDist(currentPos, topright), topright)
#     botleft = (topleft[0], topleft[1] + bounds[2])
#     cornerType['botleft'] = (mapDist(currentPos, botleft), botleft)
#     botright = (topleft[0] + bounds[2], topleft[1] + bounds[2])
#     cornerType['botright'] = (mapDist(currentPos, botright), botright)

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
    xrate = 0.70
    yrate = 0.65
    xlen = 0.25
    ylen = 0.25

    corners = {}
    corners['topleft'] = (xrate*width, yrate*height)
    corners['topright'] = (xrate*width + xlen*width, yrate*height)
    corners['botleft'] = (xrate*width, yrate*height + ylen*height)
    corners['botright'] = (xrate*width + xlen*width, yrate*height + ylen*height)
    return (corners, xlen*width, ylen*height)

def statusUpdate():
    while stop:
        time.sleep(0.02)
        r.update()

if __name__ == "__main__":
    main()
