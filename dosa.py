import cv2 as cv
import time
from windowcapture import WindowCapture
import settings
import keyboard
from dosa.spells import *
from dosa.pve import *
from spell import Spell
import utils


DEBUG = True

# initialize the WindowCapture class
wincap = WindowCapture()
settings.init(['F24', 'r'])

state = 0
last_cast = 0
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
            
            q_block.ready()

            print("Spells Initiated")
            spells_init = True

        if keyboard.is_pressed('F24'):
            state = pve(state, last_cast)
            last_cast = time.time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')