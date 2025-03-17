import cv2 as cv
import time
from windowcapture import WindowCapture
import settings
import keyboard
from nova.spells import accel, swooping_accel, accel_buff, init_spells
from nova.non_accel import *
from nova.endgame import *
import utils


DEBUG = True

# initialize the WindowCapture class
wincap = WindowCapture()
settings.init(['x', 'F23', 'F24', 'r'])

last_cast = time.time()
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

        if keyboard.is_pressed('F23') or keyboard.is_pressed('x') or keyboard.is_pressed('r'):
            buffs = wincap.get_buffs()
            if accel_buff.ready(buffs):
                print("ACCEL")
                # new_last_cast = dehkia(last_cast)
                # new_last_cast = endgame_with_opener(last_cast)
                new_last_cast = endgame_no_opener(last_cast)
                # new_last_cast = midgame(last_cast)
                last_cast = new_last_cast if new_last_cast is not None else last_cast
            else:
                if accel.ready(wincap.get_accel()):
                    if swooping_accel.ready():
                        if swooping_accel.cast():
                            last_cast = time.time()
                    else:
                        accel.cast()
                else:
                    new_last_cast = non_accel(last_cast)
                    last_cast = new_last_cast if new_last_cast is not None else last_cast
        
        if keyboard.is_pressed('F24'):
            if fleche_lunge_combo.ready():
                fleche_lunge_combo.cast()


    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')