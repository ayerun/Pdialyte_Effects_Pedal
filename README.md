# Pdialyte Effects Pedal
### Author: Arun Kumar
* Software and hardware design for a sound effect pedal with user created effects. See this post for more information.

#### Jetson Nano Setup
1. Install Dependencies
```
sudo apt install -y python3 git python3-pip
sudo apt update
sudo apt upgrade
sudo pip3 install --upgrade setuptools
sudo pip3 install adafruit-blinka
sudo pip install sparkfun-qwiic-twist 
sudo apt-get install puredata
```
2. Enable GPIO Pins
```
sudo /opt/nvidia/jetson-io/jetson-io.py
```
3. Set User Permissions
```
sudo groupadd -f -r gpio
sudo usermod -a -G gpio <insert_your_username>
```
4. Copy Udev Rules
```
cd ~
git clone https://github.com/NVIDIA/jetson-gpio.git
sudo cp ~/jetson-gpio/lib/python/Jetson/GPIO/99-gpio.rules /etc/udev/rules.d
```
5. Configure Pure Data DAC/ADC
    1. Plug in your USB audio interface
    2. Open Pure Data
    3. Media -> Audio Settings
    4. Set delay to 8ms
    5. Set input and output device to your audio interface
    6. Save All Settings
    7. Close Pd


#### Wiring
* Encoder
    * 3.3V -> 3.3V
    * GND -> GND
    * SDA -> Jetson Pin 3
    * SCL -> Jetson Pin 5
* Stomp Button
    * Terminal 1 -> 1k Ohm Resistor -> 5V
    * Terminal 1 -> Jetson Pin 24
    * Terminal 2 -> GND
* LCD
    * Vss -> GND
    * Vdd -> 5V
    * V0 -> 10k Ohm Potentiometer Output
    * RS -> Jetson Pin 37
    * RW -> GND
    * E -> Jetson Pin 35
    * D4 -> Jetson Pin 22
    * D5 -> Jetson Pin 18
    * D6 -> Jetson Pin 15
    * D7 -> Jetson Pin 13
    * A -> 5V
    * K -> GND
* Potentiometer
    * Terminal 1 -> 5V
    * Terminal 2 -> V0 (LCD)
    * Terminal 3 -> GND

#### Usage Instructions

1. Plug in Audio Interface
2. Launch effect
```
./<path_to_repo>/Effects_Library/<desire_sound_effect_directory>/start.sh
```

#### Repository Layout
* CAD directory contains 3D models of the pedal
* Effects_Library contains all the sound effects
    * Each effect has its own folder
    * Each folder contains a controls.py, effect.pd, pedal_input~.pd, and start.sh file
        * effect.pd is the Pd patch with the sound effect
        * controls.py is the Python script that controls all pedal peripherals
        * pedal_input~.pd is a subpatch used in effect.pd to turn the sound effect on/off when the stomp button is pressed
            * inputs a 0 or 1
            * both outlets are the audio clean audio signal but only one outlet is on at a time.
        * start.sh is a bash script to start the sound effect

#### Creating New Sound Effects
* Copy NEW_EFFECT_TEMPLATE directory
* Modify <a href="https://github.com/ayerun/Guitar_Pedal/blob/master/Effects_Library/NEW_EFFECT_TEMPLATE/controls_template.py" target="_blank">controls.py</a> with your effect parameters
    * There are detailed instructions in <a href="https://github.com/ayerun/Guitar_Pedal/blob/master/Effects_Library/NEW_EFFECT_TEMPLATE/controls_template.py" target="_blank">controls.py</a>
* Create an effect.pd patch
* See this post for more details
    