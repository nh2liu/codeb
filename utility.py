import math
import time
import copy
from rObject import *
import commands
from main import *

epison = 0.005
# MAPWIDTH = 10000
# HEIGHT = 10000
# r.config['friction']
def mapDist(t1, dest):
    position = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            position.append(sub(dest, (r.config['mapwidth'] * i, r.config['mapheight'] * j)))
    minDist = min(position, key=lambda x: distance(x, t1))
    return distance(minDist, t1)

# def closestPath(t1, dest):
#     position = []
#     for i in range(-1, 2):
#         for j in range(-1, 2):
#             position.append(sub(dest, (MAPWIDTH * i, MAPWIDTH * j)))
#     minDist = min(position, key=lambda x: distance(x, t1))
#     return sub(minDist, t1)

def trueDest(t1, dest):
    position = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            position.append(sub(dest, (r.config['mapwidth'] * i, r.config['mapheight'] * j)))
    return min(position, key=lambda x: distance(x, t1))

def closeEnough(t1, t2, e = epison):
    return distance(t1,t2) <= e

def mulC(a,c):
    return a[0]*c, a[1]*c

def sub(a,b):
    return a[0] - b[0], a[1] - b[1]

def distance(t1, t2):
    return norm(sub(t1,t2))

def norm(t):
    return math.sqrt(t[0] ** 2 + t[1] ** 2)

def normalize(t):
    n = norm(t)
    return t[0] / n, t[1] / n

# basic move
def mov(cur, velocity, dest):
    path = dest[0] - cur[0], dest[1] - cur[1]
    path_n = normalize(path)
    v_n = normalize(velocity)


# basic move: stop, acceleration, deacceleration, one call
def calibrateAcc():
    pos = r.pos
    run("ACCELERATE 0 1")
    acceleration = []
    for i in range(5):
        v = r.vel
        time.sleep(0.2)
        a = distance(v, r.vel)/0.2
        print(r)
        acceleration.append(a)
    result = sum(acceleration) / 10
    print(result)
    return result

def findAcc():
    # print (str(r.pos[1]))
    friction=0.99
    v1 = r.vel
    r.accelerate(0, 1)
    time.sleep(1)
    v2 = r.vel
    aConstant=norm(mulC(sub(v2,mulC(v1,friction)),1/friction))
    print("Acceleration is: "+str(aConstant))


def movb(dest,interrupt):
    print ("dest pos: "+str(dest[0])+", "+str(dest[1]))
    print ("r pos: "+str(r.pos[0])+", "+str(r.pos[1]))
    print(r.pos)
    while closeEnough((0,0), r.vel)==False:
        run("BRAKE")
    print(dest)
    origDest=dest
    dest=trueDest(r.pos,dest)
    print(dest)
    path = abs(dest[0] - r.pos[0]), abs(dest[1] - r.pos[1])
    print(path)
    # q1
    if dest[0]==r.pos[0]:
        if dest[1]<r.pos[1]:
            r.accelerate(3*math.pi/2, 1)
        else:
            r.accelerate(math.pi/2, 1)
    else:
        angle = math.atan(path[1]/path[0])
        if dest[0]>=r.pos[0] and dest[1]<=r.pos[1]:
            print("q1")
            r.accelerate(-angle, 1)
        # q2
        elif dest[0]<=r.pos[0] and dest[1]<=r.pos[1]:
            print("q2")
            r.accelerate(math.pi+angle, 1)
        # q3
        elif dest[0]<=r.pos[0] and dest[1]>=r.pos[1]:
            print("q3")
            r.accelerate(math.pi-angle, 1)
        # q4
        else:
            print("q4")
            r.accelerate(angle, 1)

    while True:
        time.sleep(0.1)
        if interrupt:
            mines=r.mines
            mines=[x for x in mines if x[0]!="goose"]
            if (mines!=[]):
                print ("found")
                return min(mines, key=lambda x: mapDist(r.pos, (x[1],x[2])))
        # print(distance(dest,r.pos))
        if closeEnough(origDest, r.pos, 5):
            print("Desstination Reached")
            break

def whenTobrake():
    x = norm


# x = distance to dist, v = initial velocity, a = acceleration

#
# t = v / maxA
# x = v * t - 1/2 * maxA * t ** 2
# v * t +(v + MaxAccel * )*t2+0.5*MaxAccel*t1^2-0.5*MaxDecel*t2^2=X