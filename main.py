from rObject import *
import time
import threading
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
		r.update()
		#print(r)
		time.sleep(10)

if __name__ == "__main__":
	main()
