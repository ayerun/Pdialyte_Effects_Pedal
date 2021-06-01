import RPi.gpio as GPIO
import time

button = 8

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button, GPIO.IN)

    try:
        while True:
            GPIO.wait_for_edge(button, GPIO.FALLING)
            print("Button Pressed!")
            time.sleep(0.1)
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()