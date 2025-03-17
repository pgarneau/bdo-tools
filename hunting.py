import cv2 as cv
import time
from windowcapture import WindowCapture
import settings
import keyboard
from hunting.hunting import *
from spell import Spell
from bind import Bind
import utils


DEBUG = True

# initialize the WindowCapture class
wincap = WindowCapture()
settings.init(['F24', 'F23', 'F22'])

last_cast = time.time()
last_element = None
state = 0
paused = False
was_pressed = False

while(True):
    if settings.keybind_active() and utils.bdo_selected() and not paused:

        if keyboard.is_pressed('F24'):
            was_pressed = True
            state = hunt()

    elif was_pressed and mouse.is_pressed('left'):
        print('releasing left click')
        mouse.release('left')
        was_pressed = False
    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')