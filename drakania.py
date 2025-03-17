import cv2 as cv
import numpy as np
import os
import time
from windowcapture import WindowCapture
from spell import Spell, keybind
from vision import Vision
from bind import Bind
from ocr import Ocr
# from bot import AlbionBot, BotState
import keyboard
import mouse

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their 
# own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))


DEBUG = True

# initialize the WindowCapture class
wincap = WindowCapture()
ocr = Ocr()

# Initialize Spells

# Stance
hexblood = Spell('hexblood', None, wincap, 0.99)
dragonblood = Spell('dragonblood', None, wincap, 0.99)

# Blue
aerial_burst = Spell('aerial_burst', Bind('3', None), wincap)
tectonic_blue = Spell('tectonic_slam_blue', Bind('s+e', None, 0.5), wincap)
savage_decree = Spell('savage_decree', Bind('s', 'left', 0.5), wincap)
spiteful_soul_blue = Spell('spiteful_soul_blue', Bind('shift', 'right', 1.2), wincap)
tip_of_the_scale_blue = Spell('tip_of_the_scale_blue', Bind('shift', 'left', 1), wincap)
cloud_strife = Spell('cloud_strife', Bind(None, 'left+right', 0.7), wincap)
obliterate = Spell('obliterate', Bind('shift+e', None, 0.9), wincap)
doombringer = Spell('doombringer', Bind('shift+q', None, 1.2), wincap)
sundering_blue = Spell('sundering_blue', Bind('s+f', None, 1.6), wincap)
storm_piercer_blue = Spell('storm_piercer_blue', Bind('s', 'right', 0.7), wincap)

# Red
tectonic_red = Spell('tectonic_slam_red', Bind('w+e', None), wincap)
sundering_red = Spell('sundering_red', Bind('s+f', None, 0.8), wincap)
crackling_flame = Spell('crackling_flame', Bind('f', None, 0.3), wincap)
extinction = Spell('extinction', Bind('shift+f', None, 0.2), wincap)
concealed_claw = Spell('concealed_claw', Bind(None, 'left+right', 0.3), wincap)
storm_piercer_red = Spell('storm_piercer_red', Bind('s', 'right', 0.7), wincap)
tip_of_the_scale_red = Spell('tip_of_the_scale_red', Bind('shift', 'left', 1), wincap)
tip_of_the_scale_red_cancel = Spell('tip_of_the_scale_red', Bind(None, 'left', 0.4), wincap)
spiteful_soul_red = Spell('spiteful_soul_red', Bind(None, 'right', 0.8), wincap)

# Legacy
legacy = Spell('legacy', Bind('space', None, 0.5), wincap)
fate_beckons = Spell('fate_beckons', Bind('w+f'), wincap)


def infinite(hexblood, state):
    if state == 1:
        if not tectonic_blue.on_cooldown():
            tectonic_blue.cast()
            return 1
        if not hexblood and not savage_decree.on_cooldown():
            savage_decree.cast()
            return 1
        if not hexblood and not storm_piercer_blue.on_cooldown():
            storm_piercer_blue.cast()
            legacy.cast()
            return 1

        if not sundering_blue.on_cooldown():
            return 2
        else:
            return 4
    if state == 2:
        if not aerial_burst.on_cooldown():
            aerial_burst.cast()
            return 2
        if not sundering_blue.on_cooldown():
            sundering_blue.cast()
            return 3
        return 3
    if state == 3:
        if not tectonic_red.on_cooldown():
            tectonic_red.cast()
            return 3
        if not extinction.on_cooldown():
            extinction.cast()
            spiteful_soul_red.cast()
            tip_of_the_scale_red_cancel.cast()
            return 3       
        if hexblood and not sundering_red.on_cooldown() and not crackling_flame.on_cooldown() and not concealed_claw.on_cooldown():
            sundering_red.cast()
            crackling_flame.cast()
            concealed_claw.cast()
            return 3
        if hexblood and not storm_piercer_red.on_cooldown():
            storm_piercer_red.cast()
            return 1
        return 1
    if state == 4:
        if not obliterate.on_cooldown() and not doombringer.on_cooldown():
            obliterate.cast()
            doombringer.cast()
        return 3
    
def gyfin(hexblood, state):
    if state == 1:
        if not aerial_burst.on_cooldown():
            aerial_burst.cast()
            return 1
        if not tectonic_blue.on_cooldown() and not savage_decree.on_cooldown():
            tectonic_blue.cast()
            savage_decree.cast()
            return 1
        if not hexblood and not tip_of_the_scale_blue.on_cooldown():
            tip_of_the_scale_blue.cast()
            return 1
        if not hexblood and not spiteful_soul_blue.on_cooldown() and not cloud_strife.on_cooldown():
            spiteful_soul_blue.cast()
            cloud_strife.cast()
            return 1
        if not obliterate.on_cooldown() and not doombringer.on_cooldown():
            obliterate.cast()
            doombringer.cast()
            return 2
        return 2
    if state == 2:
        if not tectonic_red.on_cooldown():
            tectonic_red.cast()
            return 2
        if not extinction.on_cooldown():
            extinction.cast()
            return 2        
        if hexblood and not sundering_red.on_cooldown() and not crackling_flame.on_cooldown() and not concealed_claw.on_cooldown():
            sundering_red.cast()
            crackling_flame.cast()
            if not concealed_claw.on_cooldown():
                concealed_claw.cast()
            return 2
        if hexblood and not spiteful_soul_red.on_cooldown():
            spiteful_soul_red.cast()
            if not concealed_claw.on_cooldown():
                concealed_claw.cast()
            legacy.cast()
            return 2
        if not hexblood and not sundering_blue.on_cooldown():
            sundering_blue.cast()
            if not storm_piercer_blue.on_cooldown():
                storm_piercer_blue.cast()
            return 1
        if hexblood and not storm_piercer_red.on_cooldown():
            storm_piercer_red.cast()
            legacy.cast()
            return 2
        
        return 1


def main():
    hexblood_state = False
    state = 1
    time_since_first_state = 0

    while(True):
        if keyboard.is_pressed(keybind):
            hexblood_state = False
            screenshot = wincap.get_screenshot()
            hexblood_buff = wincap.get_screenshot('buffs')

            if not hexblood.on_cooldown(hexblood_buff):
                hexblood_state = True
                print("IN HEXBLOOD")

            if state == 1:
                time_since_first_state = time.time()
            
            print(time.time() - time_since_first_state)
            if time.time() - time_since_first_state > 10:
                state = 1
            # state = gyfin(hexblood_state, state)
            state = infinite(hexblood_state, state)

        # # debug the loop rate
        # print('FPS {}'.format(1 / (time.time() - loop_time)))
        # loop_time = time.time()

        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break

    print('Done.')

if __name__ == "__main__":
    main()