from commands import *
import time
import threading
r = MyReponse()
import utility

stop = 1

def main():
	updateThread = threading.Thread(target = statusUpdate)
	updateThread.start()
	while True:
		x = int(input())
		y = int(input())
		utility.movb((x,y))
		if x == "stop":
			stop = 0
			break
		if x == "cal":
			utility.calibrateAcc()

def statusUpdate():
	while stop:
		time.sleep(0.1)
		r.update()
		#print(r)

main()
