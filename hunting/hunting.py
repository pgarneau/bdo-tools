
import os
import time
from windowcapture import WindowCapture
from spell import Spell, NoCooldownSpell
from combo import Combo
from bind import Bind, hold_bind, hold_bind_release_early
from vision import find_nearby_targets
import keyboard
import mouse

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their 
# own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# initialize the WindowCapture class
wincap = WindowCapture()

# Hunting
aiming = Spell('aiming', None, 0.99)
# crosshair = Spell('crosshair', None, threshold=0.9)
crosshair = Spell('crosshair_dezoom', None, threshold=0.9)
reload_deep_left = Spell('reload_deep_left', None, threshold=0.94)
reload_left = Spell('reload_left', None, threshold=0.94)
reload_center = Spell('reload_center', None, threshold=0.94)
# reload_right = Spell('reload_right', None, threshold=0.96)

# States
# 0 = aiming
# 1 = shooting
# 2 = Reloading
def hunt():
    if aiming.ready(wincap.get_hunting_crosshair()):
        if mouse.is_pressed('left'):
            if crosshair.ready(wincap.get_hunting_crosshair(), debug='rectangles'):
                mouse.release('left')
                time.sleep(1)
                keyboard.press_and_release('space')
                return
        else:
            mouse.press('left')
            return

    # reload_ss = wincap.get_reloader()

    # if reload_deep_left.ready(wincap.get_reloader(), debug='rectangles'):
    #     keyboard.press_and_release('space')
    
    # if reload_deep_left.ready(wincap.get_reloader(), debug='rectangles') or reload_left.ready(wincap.get_reloader(), debug='rectangles') or reload_center.ready(wincap.get_reloader(), debug='rectangles'):
    #     keyboard.press_and_release('space')
    # print('not aiming')

