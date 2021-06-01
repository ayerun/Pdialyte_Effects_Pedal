import digitalio
import board
import time

def main():
    pin = digitalio.DigitalInOut(D8)
    while True:
        print(pin.value)
        time.sleep(0.1)

if __name__ == '__main__':
	try:
		main()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Script")
		sys.exit(0)