import cv2 as cv
import time
from windowcapture import WindowCapture
import settings
import keyboard
from witch.pve import *
from spell import Spell
from bind import Bind
import utils


DEBUG = True

# initialize the WindowCapture class
wincap = WindowCapture()
settings.init(['F24', 'F23', 'F22'])

last_cast = time.time()
last_element = None
spells_init = False
paused = False

# Pause Keybinds
pause_binds = [
    Bind('d', 'left'),
    Bind('a', 'left'),
    Bind('shift+d', None),
    Bind('shift+a', None),
    Bind('shift+s', None),
]

while(True):
    if settings.keybind_active() and utils.bdo_selected() and not paused:
        if not spells_init:
            screenshot = wincap.get_skills()
            for spell in Spell.instances:
                spell.ready(screenshot)

            print("Spells Initiated")
            spells_init = True

        if keyboard.is_pressed('F24'):
            new_last_cast, last_element = pve(last_cast, last_element)
            last_cast = new_last_cast if new_last_cast is not None else last_cast
        # elif keyboard.is_pressed('F23'):
        #     sa_rotation()
        # elif keyboard.is_pressed('F22'):
        #     combo()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')