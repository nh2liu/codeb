from rObject import *
import time
import threading
import utility
import math

stop = 1

def main():
    updateThread = threading.Thread(target = statusUpdate)
    updateThread.start()
    while True:
        x = int(input())
        y = int(input())
        utility.movb((x,y),True)
        if x == "stop":
            stop = 0
            break
        if x == "cal":
            utility.calibrateAcc()


def strategy():
    bounds = moveBoundaries()
    r.update()
    moveType = moveToCorner(r.pos, bounds)
    print(moveType)

    scanPortion(moveType)

def scanPortion(moveType):
    print(1)


def moveToCorner(currentPos, bounds):
    cornerType = {}

    def pointDistance(p1, p2):
        return math.sqrt((p1[0] - p2[0])*(p1[0] - p2[0]) + (p1[1] - p2[1])*(p1[1] - p2[1]))
    
    topleft = bounds[0]
    cornerType['topleft'] = (pointDistance(currentPos, topleft), topleft)
    topright = (topleft[0] + bounds[1], topleft[1])
    cornerType['topright'] = (pointDistance(currentPos, topright), topright)
    botleft = (topleft[0], topleft[1] + bounds[2])
    cornerType['botleft'] = (pointDistance(currentPos, botleft), botleft)
    botright = (topleft[0] + bounds[2], topleft[1] + bounds[2])
    cornerType['botright'] = (pointDistance(currentPos, botright), botright)

    minCornerType = 'topleft'
    minDist = cornerType['topleft'][0]
    for k, v in cornerType.items():
        if v[0] < minDist:
            minCornerType = k

    #movb(cornerType[minCornerType][1])
    return minCornerType


def moveBoundaries():
    width = r.config['mapwidth']
    height = r.config['mapheight']
    xrate = 0
    yrate = 0.5
    xlen = 0.5
    ylen = 0.5

    return ((xrate * width, yrate*height), xlen * width, ylen*height)

def statusUpdate():
    while True:
        time.sleep(0.1)
        r.update()
        # print(r)


if __name__ == "__main__":
	main()
