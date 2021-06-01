import digitalio
import board
import time
import sys

def main(pin):
    while True:
        print(pin.value)
        time.sleep(0.1)

if __name__ == '__main__':
	try:
        pin = digitalio.DigitalInOut(board.D8)
        main(pin)
	except (KeyboardInterrupt, SystemExit) as exErr:
        pin.deinit()
        print("\nEnding Script")
        sys.exit(0)
