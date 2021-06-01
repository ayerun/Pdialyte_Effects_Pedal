import RPi.GPIO as GPIO
import time

button = 8

def button_back(channel):
    print("Button Pressed!")



def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button, GPIO.IN)
    GPIO.add_event_detect(button, GPIO.FALLING, callback=button_back, bouncetime=10)

    try:
        while True:
            print("nothing happening")
            time.sleep(0.1)
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
    GPIO.cleanup()