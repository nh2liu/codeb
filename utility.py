import math
import time
import copy
from rObject import *
import commands
from main import *

epson2 = 50
epsilon = 0.5
epson3 = 0.5
aConstant=0
MAPWIDTH = r.config['mapwidth']
# HEIGHT = 10000
# r.config['friction']


# return the smallest distance btw 2 points, taking account of edge crossing
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

def closeEnough(t1, t2, e = epsilon):
    return distance(t1,t2) <= e

def mulC(a,c):
    return a[0]*c, a[1]*c

def sub(a,b):
    return a[0] - b[0], a[1] - b[1]

def dot(a,b):
    return a[0]*b[0]+a[1]*b[1]

def proj(v,d):
    return mulC(d,dot(v,d)/(norm(d)**2))

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
        acceleration.append(a)
    result = sum(acceleration) / 10
    return result

def findAcc():
    friction=0.99
    v1 = r.vel
    r.accelerate(0, 1)
    time.sleep(0.5)
    v2 = r.vel
    global aConstant
    print(v1)
    print(v2)
    aConstant=norm(mulC(sub(v2,mulC(v1,friction)),1/friction))/20
    print("Acceleration is: "+str(aConstant))

def direction(pos,dest):
    path = abs(dest[0] - pos[0]), abs(dest[1] - pos[1])
    angle=0
    if dest[0]==pos[0]:
        if dest[1]<pos[1]:
            angle=3*math.pi/2
        else:
            angle=math.pi/2
    else:
        angle = math.atan(path[1]/path[0])
        # q1
        if dest[0]>=pos[0] and dest[1]<=pos[1]:
            angle=-angle
        # q2
        elif dest[0]<=pos[0] and dest[1]<=pos[1]:
            angle=-math.pi+angle
        # q3
        elif dest[0]<=pos[0] and dest[1]>=pos[1]:
            angle=-math.pi-angle
        # q4
        else:
            angle=angle
    return angle

def bomb(xc=None,yc=None):
    x=r.pos[0]+10*r.vel[0]
    y=r.pos[1]+10*r.vel[1]

    if xc:
        x = xc
        y = yc
    # print (x)
    # print (y)
    # print (r.pos)
    r.bomb(x,y)
def crossEdge(prev,cur):
    if (abs(prev[0]-cur[0])>0.9*r.config['mapwidth'] or abs(prev[1]-cur[1])>0.9*r.config['mapheight']):
        return True
    else:
        return False
def mova(dest):
    origDest=dest
    while True:
        dest=trueDest(r.pos,dest)
        d = abs(dest[0] - r.pos[0]), abs(dest[1] - r.pos[1])
        aVector=mulC(sub(r.vel,proj(r.vel,d)),-1)
        mag=min(1,norm(aVector)/aConstant)
        arg=direction(r.vel,(r.vel[0]+10*aVector[0],r.vel[1]-10*aVector[1]))
        r.accelerate(arg, mag)
        if closeEnough(origDest, r.pos, 10):
            print("Destination Reached")
            break
# def movb(dest, nul = False):
#     origDest=dest
#     dest = trueDest(r.pos, origDest)
#     print('dest : ' + str(dest))
#     prev=r.pos
#     actualDest=dest
#     while True:
#         if (crossEdge(prev,r.pos)):
#             print("edge cross")
#             actualDest=origDest
#         prev=r.pos
#         if closeEnough(origDest, r.pos, 10):
#             break
#         if nul:
#             mines=r.mines
#             mines=[x for x in mines if x[0]!=username]
#             if (mines!=[]):
#                 print ("found")
#                 return min(mines, key=lambda x: mapDist(r.pos, (x[1],x[2])))
#         else:
#             for player in r.players:
#                 if closeEnough(player.pos, origDest, r.config['bombeffectradius']*2):
#                     bomb(player.pos[0], player.pos[1])

#         d = actualDest[0] - r.pos[0], actualDest[1] - r.pos[1]
#         if (norm(d)==0):
#             break
#         aVector = mulC(sub(r.vel,proj(r.vel, d)), -1)
#         arg=0
#         mag=0
#         if (norm(aVector)<aConstant):
#             arg=direction(r.pos,actualDest)
#             mag=1
#         else:
#             # binary search for best value
#             low = 0
#             if (d[1]):
#                 low= proj(r.vel,d)[1]/d[1]
#             else:
#                 low = proj(r.vel, d)[0] / d[0]
#             high=low + aConstant/norm(d)
#             n=0
#             acc=0,0
#             while(abs(high-low)<0.001):
#                 n=(low+high)/2
#                 acc=sub(mulC(d,n),r.vel)
#                 if (norm(acc)<=aConstant):
#                     low=n+0.001
#                 else:
#                     high=n-0.001
#             arg=direction(r.vel,(r.vel[0]+10*acc[0],r.vel[1]+10*acc[1]))
#             mag=1
#         r.accelerate(arg, mag)
#       #  print("accelerating", origDest, arg, dest)
#     print("Destination Reached")
# '''
def movb(dest,interrupt):
    if interrupt == False:
        epsilon = 0.015
        epson2 = 10
        epson3 = 0.2
    else:
        epsilon = 0.4
        epson3 = 0.2
        epson2 = 100
    print ("dest pos: "+str(dest[0])+", "+str(dest[1]))
    # print ("r pos: "+str(r.pos[0])+", "+str(r.pos[1]))
    # print(r.pos)
    while closeEnough((0,0), r.vel, epson3)==False:
        time.sleep(0.025)
        # print("decelerating")
        # decelerate
        mag=min(1,norm(r.vel)/aConstant)
        arg=direction(r.pos,(r.pos[0]-10*r.vel[0],r.pos[1]-10*r.vel[1]))
        r.accelerate(arg, mag)
    # if interrupt:
    #     r.bomb(r.pos[0],r.pos[1])
    print(dest)
    origDest=dest
    dest=trueDest(r.pos,dest)
    angle=direction(r.pos,dest)
    r.accelerate(angle, 1)
    prev = r.pos
    counter = 1
    while True:
        time.sleep(0.01)
        counter += 1
        if mapDist(prev, origDest) < mapDist(r.pos, origDest) and counter >= 500:
            return False
        prev = r.pos
        if interrupt:
            mines=r.mines
            mines=[x for x in mines if x[0]!=username]
            if (mines!=[]):
                print ("found")
                return min(mines, key=lambda x: mapDist(r.pos, (x[1],x[2])))
        else:
            for player in r.players:
                if closeEnough(player.pos, origDest, r.config['bombeffectradius']*2):
                    bomb(player.pos[0], player.pos[1])

        # print(distance(dest,r.pos))
        if closeEnough(origDest, r.pos, epson2):
            print("Desstination Reached")
            break
# '''
def whenTobrake():
    x = norm


# x = distance to dist, v = initial velocity, a = acceleration

#
# t = v / maxA
# x = v * t - 1/2 * maxA * t ** 2
# v * t +(v + MaxAccel * )*t2+0.5*MaxAccel*t1^2-0.5*MaxDecel*t2^2=X