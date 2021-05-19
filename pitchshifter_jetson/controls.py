import time
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import board
import qwiic_twist
import sys
import os

class controller:

    #controls
    transposition = 0
    window = 0
    delay = 0
    resolution = 1

    #limits
    t_lim = [-24,24]
    w_lim = [0,2000]
    delay_lim = [0,10000]
    res_list = [0.01,0.05,0.1,0.5,1,5,10,50,100]

    #constructor
    def __init__(self):

        #LCD Setup
        lcd_columns = 16
        lcd_rows = 2

        #GPIO Setup
        lcd_rs = digitalio.DigitalInOut(board.D26)
        lcd_en = digitalio.DigitalInOut(board.D19)
        lcd_d7 = digitalio.DigitalInOut(board.D27)
        lcd_d6 = digitalio.DigitalInOut(board.D22)
        lcd_d5 = digitalio.DigitalInOut(board.D24)
        lcd_d4 = digitalio.DigitalInOut(board.D25)
        lcd_backlight = digitalio.DigitalInOut(board.D4)

        #Initialize LCD
        self.lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
        self.lcd.backlight = True
        self.lcd.message = "Transposition\nWindow"

        #Initialize Encoder
        self.twist = qwiic_twist.QwiicTwist()
        if self.twist.connected == False:
            print("The Qwiic twist device isn't connected to the system. Please check your connection", file=sys.stderr)
            sys.exit(0)
        self.twist.begin()
        self.twist.set_color(255, 0, 0) #set color to red


def send2Pd(message=''):
	os.system("echo '" + message + "' | pdsend 3000")

def main():

    #Start controller
    ps = controller()

    #Loop
    while True:
        print("Count: %d, Pressed: %s" % (ps.twist.count, "YES" if ps.twist.pressed else "NO",))
        send2Pd(str(ps.twist.count) + ';')
        time.sleep(.1)

if __name__ == '__main__':
	try:
		main()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Script")
		sys.exit(0)
