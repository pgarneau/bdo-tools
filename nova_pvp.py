import cv2 as cv
import numpy as np
import os
import time
from windowcapture import WindowCapture
from spell import Spell
from vision import find_nearby_targets
from combo import Combo
from bind import Bind, hold_bind
from ocr import Ocr
import settings
# from bot import AlbionBot, BotState
import keyboard
import mouse

from nova.spells import *
from nova.pvp import *
import utils

DEBUG = True

# initialize the WindowCapture class
wincap = WindowCapture()

settings.init(['F23', 'F24', 'r'])




last_cast = time.time()
combo_state = 0
spells_init = False



while(True):
    if not settings.keybind_active():
        combo_state = 0
    # CC engages
    # grab (w+e) (knockdown)
    # swooping ring (w + rmb) (stiffness)
    # lunge (f) (stun)
    # brutal ring (1) (bound)
    # comet (w+f) (knockdown)
    # starfall (shift+rmb) (floating)
    # riposte (s+q) (floating)

    # State 1 -> dmg required
    # State 2 -> HARD OR SOFT CC required
    # 
    if settings.keybind_active() and utils.bdo_selected():
        if not spells_init:
            spells_init = init_spells()
        
        if keyboard.is_pressed('F23'):
            bomb()
        elif keyboard.is_pressed('r'):
            new_last_cast, new_combo_state = combo(last_cast, combo_state) or (None, None)
            last_cast = new_last_cast if new_last_cast is not None else last_cast
            combo_state = new_combo_state if new_combo_state is not None else combo_state
        # if time.time() - last_cc < 2 or cc_counter >= 2:
        #     dps()
        # else:
        #     hard_cc()
        

        # dps(accel_state)
        # gyfin()
        # elvia(accel_state)

    # # debug the loop rate
    # print('FPS {}'.format(1 / (time.time() - loop_time)))
    # loop_time = time.time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')