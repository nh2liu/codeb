import math
import time
from main import *

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
    run("ACCEKERATE 0 1")
    acceleration = []
    for i in range(5):
        time.sleep(0.2)
        # calculation
        print()
    result = sum(acceleration) / 10
    print(result)
    return result


def movb(dest):
    while r.vel != (0, 0):
        run("BRAKE")
    path = dest[0] - r.pos[0], dest[1] - r.pos[1]
    angle = math.asin(path[1]/path[0])
    run("ACCELERATE " + str(angle) + " 1")
    while ()

def brake()


# x = distance to dist, v = initial velocity, a = acceleration

#
# t = v / maxA
# x = v * t - 1/2 * maxA * t ** 2
# v * t +(v + MaxAccel * )*t2+0.5*MaxAccel*t1^2-0.5*MaxDecel*t2^2=X

