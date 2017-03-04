from commands import *
import time
import threading
r = MyReponse()

def main():
	updateThread = threading.Thread(target = statusUpdate)
	updateThread.start()


def statusUpdate():
	while True:
		time.sleep(0.1)
		r.update()
		print(r)

main()