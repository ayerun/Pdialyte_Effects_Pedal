import time
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import board
import qwiic_twist
import sys
import os

class control:

    def __init__(self,title,low_lim,high_lim,unit,val=0):
        self.name = title
        self.unit = unit
        self.low = low_lim
        self.high = high_lim
        self.value = val

class controller:

    #Encoder Resolution
    resolution = 1
    res_list = [0.01,0.05,0.1,0.5,1,5,10,50,100]

    #Last encoder count
    count = 0

    #false while in control menu true while in tuning menu
    clicked = False

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

        #Initialize Encoder
        self.twist = qwiic_twist.QwiicTwist()
        if self.twist.connected == False:
            print("The Qwiic twist device isn't connected to the system. Please check your connection", file=sys.stderr)
            sys.exit(0)
        self.twist.begin()
        self.twist.set_color(255, 0, 0) #set color to red
        self.twist.set_count(0)
    
    #returns difference from last encoder count
    def getDiff(self):
        diff = self.twist.count-self.count
        self.count = self.twist.count
        return diff

def send2Pd(message=''):
	os.system("echo '" + message + "' | pdsend 3000")

def main():
    #Make controls
    transposition = control("Transposition", -24, 24, "1/2 steps", 0)
    window = control("Window", 0, 2000, "ms", 0)
    delay = control("Delay", 0, 5000, "ms", 0)
    controls = [transposition,window,delay]

    #Start controller
    ps = controller(controls)

    #Loop
    while True:

        #check for encoder ticks
        diff = ps.getDiff()
        if ps.twist.has_moved():

            #update control index and enforce limits
            ps.control_index += diff
            if ps.control_index < 0:
                ps.control_index = 0
            elif ps.control_index > ps.control_lim:
                ps.control_index = ps.control_lim
            
            #update lcd
            ps.lcd.clear()
            ps.lcd.message = ps.controls[ps.control_index].name

        #check for button press
        if ps.twist.was_clicked():
            ps.clicked = not ps.clicked

            #tuning menu
            if ps.clicked:
                #display value
                ps.lcd.message = ps.controls[ps.control_index].name + "\n" + str(ps.controls[ps.control_index].value) + " " + ps.controls[ps.control_index].unit

            else:
                #remove value and display control menu
                ps.lcd.clear()
                ps.lcd.message = ps.controls[ps.control_index].name

        time.sleep(.1)

if __name__ == '__main__':
	try:
		main()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Script")
		sys.exit(0)
