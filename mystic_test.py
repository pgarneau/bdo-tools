import cv2 as cv
import time
from windowcapture import WindowCapture
import settings
import keyboard
from mystic.spells import init_spells
from mystic.pve import *
import utils


DEBUG = True

# initialize the WindowCapture class
wincap = WindowCapture()
settings.init(['x', 'F23', 'F24', 'r'])

last_cast = time.time()
last_debuff = time.time()
start_time = time.time()
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

keyboard.on_press_key('enter', pause_execution)

while(True):
    if settings.keybind_active() and utils.bdo_selected() and not paused:
        if not spells_init:
            spells_init = init_spells()

        some_func()


    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')