import os
import time
from windowcapture import WindowCapture
from spell import Spell
from combo import Combo
from bind import Bind, hold_bind
from collections import OrderedDict
import cv2 as cv
import time
from windowcapture import WindowCapture
import settings
import keyboard
from spell import Spell
import utils
import json

from sorc.spells import *


spell_dict = {spell.name: spell for spell in Spell.instances}
print(spell_dict)


recent_cooldowns = []
current_cooldowns = {}

results = {}
previous_results = {}
global pretty_results

def record():
    global results
    for k, v in spell_dict.items():
        off_cd = v.ready()
        if off_cd and k in current_cooldowns.keys():
            current_cooldowns.pop(k)
            print(f"removing {k} from current cooldowns")
        elif not off_cd and k not in current_cooldowns.keys():
            current_cooldowns[k] = True
            recent_cooldowns.append((k, time.time()))
            print(k)
            if len(recent_cooldowns) >= 2:
                last_two_spells = recent_cooldowns[-2:]
                spell_a, time_a = last_two_spells[0]
                spell_b, time_b = last_two_spells[1]

                time_diff = abs(time_a - time_b)
                print(time_diff)
                if time_diff < 2:
                    name = f"{spell_a}->{spell_b}"
                    if name not in results.keys():
                        results[name] = time_diff
                        previous_results[name] = [time_diff]
                    else:
                        previous_results[name].append(time_diff)
                        average_time = sum(previous_results[name])/len(previous_results[name])
                        results[name] = average_time

                    print(json.dumps(results, sort_keys=True, indent=4))
        else:
            continue
    



DEBUG = True

# initialize the WindowCapture class
wincap = WindowCapture()
settings.init(['F24', 'r'])

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

keyboard.on_press_key('enter', pause_execution)

while(True):
    if settings.keybind_active() and utils.bdo_selected() and not paused:
        if not spells_init:
            screenshot = wincap.get_skills()
            for spell in Spell.instances:
                spell.ready(screenshot)

            print("Spells Initiated")
            spells_init = True

        if settings.keybind_active():
            record()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')