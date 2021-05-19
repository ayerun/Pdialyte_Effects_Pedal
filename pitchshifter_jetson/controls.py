import time
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import board
import qwiic_twist
import sys
import os

class control:

    def __init__(self,title,low_lim,high_lim,val=0):
        self.name = title
        self.low = low_lim
        self.high = high_lim
        self.value = val

class controller:

    #Encoder Resolution
    resolution = 1
    res_list = [0.01,0.05,0.1,0.5,1,5,10,50,100]

    #constructor
    def __init__(self,controls):
        #Initialize Controls
        self.controls = controls
        self.control_index = 0
        self.control_lim = len(controls)-1

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
        self.lcd.message = self.controls[0].name
        self.lcd.cursor = True
        self.lcd.blink = True

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
    #Make controls
    transposition = control("Transposition", -24, 24, 0)
    window = control("Window", 0, 2000, 0)
    delay = control("Delay", 0, 5000, 0)
    controls = [transposition,window,delay]

    #Start controller
    ps = controller(controls)

    #Loop
    while True:
        # print("Count: %d, Pressed: %s" % (ps.twist.count, "YES" if ps.twist.pressed else "NO",))
        # send2Pd(str(ps.twist.count) + ';')

        #check for encoder ticks
        diff = ps.twist.get_diff()
        if diff != 0:

            #update control index and enforce limits
            ps.control_index += diff
            if ps.control_index < 0:
                ps.control_index = 0
            elif ps.control_index > ps.control_lim:
                ps.control_index = ps.control_lim
            
            #update lcd
            ps.lcd.clear()
            ps.lcd.message = ps.controls[ps.control_index].name

        time.sleep(.05)

if __name__ == '__main__':
	try:
		main()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Script")
		sys.exit(0)
