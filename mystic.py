import cv2 as cv
import time
from windowcapture import WindowCapture
import keyboard
from settings import settings
from mystic.pve import *
from mystic.pvp import *
from spell import Spell
import utils


DEBUG = True

# initialize the WindowCapture class
wincap = WindowCapture()
settings.binds = ['F24']
# settings.blockers = ['shift+d', 'shift+a']

last_cast = time.time()
shards = 0
spells_init = False
paused = False

def pause_execution(lol):
    global paused
    paused = not paused
    if paused:
        print("Pausing...")
    else:
        print("Resume...")

# keyboard.on_press_key('enter', pause_execution)

while(True):
    if settings.keybind_active() and utils.bdo_selected() and not paused:
        if not spells_init:
            screenshot = wincap.get_skills()
            for spell in Spell.instances:
                spell.ready(screenshot)

            print("Spells Initiated")
            spells_init = True

        if keyboard.is_pressed('F24'):
            new_last_cast = pve(last_cast)
            last_cast = new_last_cast if new_last_cast is not None else last_cast
        elif keyboard.is_pressed('F23'):
            sa_rotation()
        elif keyboard.is_pressed('F22'):
            combo()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')