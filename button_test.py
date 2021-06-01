import digitalio
import board
import time
import sys

def main():
    pin = digitalio.DigitalInOut(board.D8)
    pin.switch_to_input()
    while True:
        print(pin.value)
        time.sleep(0.1)

if __name__ == '__main__':
	try:
		main()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Script")
		sys.exit(0)
