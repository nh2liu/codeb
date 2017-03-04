from commands import *
import time
import threading
r = MyReponse()

def main():
    updateThread = threading.Thread(target = statusUpdate)
    updateThread.start()


def strategy():
    print(r.config)
    print(moveBoundaries())

    moveType = moveToCorner()


def moveToCorner():
    


def moveBoundaries():
    width = r.config['mapwidth']
    height = r.config['mapheight']
    xrate = 0
    yrate = 0.5
    xlen = 0.5
    ylen = 0.5

    return (xrate * width, yrate*height, xlen * width, ylen*height)




def statusUpdate():
    while True:
        time.sleep(0.1)
        r.update()
        print(r)

strategy()
