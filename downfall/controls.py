import time
import digitalio
import RPi.GPIO as GPIO
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

    count = 0           #last encoder count
    clicked = False     #false while in control menu true while in tuning menu

    #constructor
    def __init__(self,controls):
        #Initialize Controls
        self.controls = controls
        self.control_index = 0
        self.control_lim = len(controls)-1

        #Initialize Button
        self.button = digitalio.DigitalInOut(board.D8)
        self.button_status = True

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
        self.twist.set_color(0, 255, 0) #set color to green
        self.twist.set_count(0)

        #Initialize Control Values
        for i in range(len(self.controls)):
            send2Pd(i,self.controls[i].value)
    
    #returns difference from last encoder count
    def getDiff(self):
        diff = self.twist.count-self.count
        self.count = self.twist.count
        if abs(diff) > 60000:
                diff = 0
        return diff

    #change encoder color between red and green
    def changeColor(self):
        red = self.twist.get_red()
        if red > 0:
            for i in range(256):
                self.twist.set_color(255-i,0+i,0)
                time.sleep(0.001)
        else:
            for i in range(256):
                self.twist.set_color(0+i,255-i,0)
                time.sleep(0.001)

    #check button status
    def buttonInterrupt(self):
        
        #check is pedal has been pressed
        if self.button.value == False:
            self.button_status = not self.button_status
            self.changeColor()
            time.sleep(0.4)
        
        #send 1 if pedal is on
        if self.button_status:
            send2Pd(99,1)
        
        #send 0 if pedal is off
        else:
            send2Pd(99,0)

def send2Pd(index, value):
    message = str(index) + ' ' + str(value) + ';'
    os.system("echo '" + message + "' | pdsend 3000")

def main():

    #Make controls
    wet = control(title="Wet", low_lim=0, high_lim=100, unit="%", val=50)
    feedback = control(title="Feedback", low_lim=0, high_lim=95, unit="%", val=50)
    speed = control(title="Speed", low_lim=0, high_lim=1, unit="", val=0.5)
    depth = control(title="Depth", low_lim=0, high_lim=1000, unit="", val=300)
    resolution = control("Resolution",0,0,"",1)
    controls = [wet,feedback,speed,depth,resolution]  #resolution should always be last

    #Resolution
    res_list = [0.01,0.05,0.1,0.5,1,5,10,50,100]
    try:
        res_index = res_list.index(1)
    except:
        res_index = 0

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
        ps.buttonInterrupt()

        #check for encoder button press
        if ps.twist.was_clicked():
            ps.clicked = not ps.clicked

            #display tuning menu
            if ps.clicked:
                ps.lcd.message = ps.controls[ps.control_index].name + "\n" + str(ps.controls[ps.control_index].value) + " " + ps.controls[ps.control_index].unit

                #tuning menu
                while ps.clicked:

                    #resolution tune
                    if ps.control_index == len(ps.controls)-1:

                        #update value and enforce limits
                        diff = ps.getDiff()
                        if ps.twist.has_moved():
                            res_index += diff
                            if res_index > len(res_list)-1:
                                res_index = len(res_list)-1
                            elif res_index < 0:
                                res_index = 0
                            ps.controls[-1].value = res_list[res_index]

                            #update lcd
                            ps.lcd.clear()
                            ps.lcd.message = ps.controls[-1].name + "\n" + str(ps.controls[-1].value)


                    #control tune
                    else:

                        #update value and enforce limits
                        diff = ps.getDiff()
                        if ps.twist.has_moved():
                            ps.controls[ps.control_index].value += diff*ps.controls[-1].value
                            if ps.controls[ps.control_index].value < ps.controls[ps.control_index].low:
                                ps.controls[ps.control_index].value = ps.controls[ps.control_index].low
                            elif ps.controls[ps.control_index].value > ps.controls[ps.control_index].high:
                                ps.controls[ps.control_index].value = ps.controls[ps.control_index].high
                            
                            #update lcd
                            ps.lcd.clear()
                            ps.lcd.message = ps.controls[ps.control_index].name + "\n" + str(round(ps.controls[ps.control_index].value,2)) + " " + ps.controls[ps.control_index].unit

                            #send value to pd
                            send2Pd(ps.control_index, ps.controls[ps.control_index].value)
                    
                    #check for encoder button press
                    if ps.twist.was_clicked():
                        ps.clicked = not ps.clicked
                    
                    time.sleep(0.1)

                #remove value and display control menu
                ps.lcd.clear()
                ps.lcd.message = ps.controls[ps.control_index].name

        time.sleep(0.1)

if __name__ == '__main__':
	try:
		main()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Script")
		sys.exit(0)
