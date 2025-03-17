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

# Spells
bamboo = Spell('woosa/bamboo', Bind('w+e', None, 0.6), wincap)
orchid = Spell('woosa/orchid', Bind('shift+e'), wincap)
fan_kick = Spell('woosa/fan_kick', Bind('f', None, 0.4), wincap)
cloudcarve = Spell('woosa/cloudcarve', Bind('s+f'), wincap)
thunderstroke = Spell('woosa/thunderstroke', Bind('s+e'), wincap)
plum = Spell('woosa/plum', Bind('s', 'left'), wincap)
kaleidoscope = Spell('woosa/kaleidoscope', Bind('shift', 'left'), wincap)
wingbeat = Spell('woosa/wingbeat', Bind('space'), wincap)
chrysanth = Spell('woosa/chrysanth', Bind('shift+f'), wincap)
cloudrise = Spell('woosa/cloudrise', Bind('shift', 'right', 0.7), wincap)
stormfall = Spell('woosa/stormfall', Bind('shift+q', None, 1), wincap)
stormbolt = Spell('woosa/stormbolt', Bind('shift', 'right'), wincap)

flitting_step = Spell('woosa/flitting_step', Bind('shift+d'), wincap)


def dps(state):
    if state == 1:
        if not fan_kick.on_cooldown():
            fan_kick.cast()
            return 1
        if not cloudcarve.on_cooldown():
            cloudcarve.cast()
            return 2
        return 1
    if state == 2:
        if not bamboo.on_cooldown():
            bamboo.cast()
            if not orchid.on_cooldown():
                orchid.cast()
            if not stormfall.on_cooldown():
                return 3
            else:
                return 4
        return 2
    if state == 3:
        if not thunderstroke.on_cooldown():
            thunderstroke.cast()
            return 3
        if not stormfall.on_cooldown():
            stormfall.cast()
            return 3
        if not wingbeat.on_cooldown():
            wingbeat.cast()
            return 3
        if not chrysanth.on_cooldown():
            chrysanth.cast()
            return 1
        return 3
    if state == 4:
        if not thunderstroke.on_cooldown():
            thunderstroke.cast()
            return 4
        if not cloudrise.on_cooldown():
            cloudrise.cast()
            flitting_step.cast()
            return 4
        if not stormbolt.on_cooldown():
            stormbolt.cast()
            return 4
        if not plum.on_cooldown():
            plum.cast()
            return 4
        if not kaleidoscope.on_cooldown():
            kaleidoscope.cast()
            return 1
        return 4    

def gyfin(state):
    if state == 1:
        if not fan_kick.on_cooldown():
            fan_kick.cast()
            return 1
        if not cloudcarve.on_cooldown():
            cloudcarve.cast()
            return 2
        return 1
    if state == 2:
        if not bamboo.on_cooldown():
            bamboo.cast()
            return 2
        if not orchid.on_cooldown():
            orchid.cast()
            return 3
        return 2
    if state == 3:
        if not thunderstroke.on_cooldown():
            thunderstroke.cast()
            return 3
        if not kaleidoscope.on_cooldown():
            kaleidoscope.cast()
            return 3
        if not wingbeat.on_cooldown():
            wingbeat.cast()
            return 3
        if not chrysanth.on_cooldown():
            chrysanth.cast()
            return 4
        return 3
    if state == 4:
        flitting_step.cast()

        if not stormfall.on_cooldown():
            stormfall.cast()
            return 1
        return 1 


def main():
    state = 1
    time_since_first_state = 0

    while(True):
        if keyboard.is_pressed(keybind):

            if state == 1:
                time_since_first_state = time.time()
            
            if time.time() - time_since_first_state > 7:
                state = 1
            state = gyfin(state)
            
            # if time.time() - time_since_first_state > 10:
            #     state = 1
            # state = dps(state)

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