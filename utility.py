import math
import time
import copy
from rObject import *
import commands
from main import *

aConstant=0

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


def movb(dest):
    print ("dest pos: "+str(dest[0])+", "+str(dest[1]))
    print ("r pos: "+str(r.pos[0])+", "+str(r.pos[1]))
    print("moving to {0}".format(dest))
    while abs(r.vel[0])>0.001 and abs(r.vel[1])>0.001:
       print("breaking")
       run("BRAKE")

    path = dest[0] - r.pos[0], dest[1] - r.pos[1]
    print(path)
    angle = math.atan(path[1]/path[0])
    print(angle)
    print("ACCELERATE " + str(angle) + " 1")
    r.accelerate(angle, 1)

def whenTobrake():
    x = norm


# x = distance to dist, v = initial velocity, a = acceleration

#
# t = v / maxA
# x = v * t - 1/2 * maxA * t ** 2
# v * t +(v + MaxAccel * )*t2+0.5*MaxAccel*t1^2-0.5*MaxDecel*t2^2=X