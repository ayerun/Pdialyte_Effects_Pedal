import qwiic_twist
import time
import sys
import os

def send2Pd(message=''):
	os.system("echo '" + message + "' | pdsend 3000")

def runExample():

	print("\nSparkFun qwiic Twist   Example 1\n")
	myTwist = qwiic_twist.QwiicTwist()

	if myTwist.connected == False:
		print("The Qwiic twist device isn't connected to the system. Please check your connection", file=sys.stderr)
		return

	myTwist.begin()

	# Set the knob color to pink
	myTwist.set_color(100, 10, 50)

	while True:

		print("Count: %d, Pressed: %s" % (myTwist.count, "YES" if myTwist.pressed else "NO",))
		send2Pd(str(myTwist.count) + ';')
		time.sleep(.1)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)
