import time
import board
import digitalio
import sys

def main():
    button = digitalio.DigitalInOut(board.D8)
    button.direction = digitalio.Direction.INPUT

    while True:
        print(button.value())
        time.sleep(0.1)
    
if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Script")
        sys.exit(0)