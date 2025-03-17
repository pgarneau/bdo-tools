import cv2 as cv
import numpy as np
import os
import time
from windowcapture import WindowCapture
from spell import Spell
from vision import Vision
from combo import Combo
from bind import Bind, hold_bind
import settings
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

# Active Keybinds
settings.init(['x', 'F23', 'F24'])

def left_click_casts(bind):
    bind.release()
    if bind.hold_time > 0 :
        start_time = time.time()
        while(settings.keybind_active() and time.time() - start_time < bind.hold_time):
            mouse.click()
            time.sleep(0.1)

# Initialize Spells
# Succession
aqua_jail = Spell('witch/aqua_jail', Bind('s+c', None, 0.4), wincap)
bolide = Spell('witch/bolide', Bind('w+c', None, 0.9), wincap)
earthquake_evade = Spell('witch/earthquake_evade', Bind('shift+f', None, 1.4), wincap)
fireball_explosion = Spell('witch/fireball_explosion', Bind('shift', 'left', 0.4), wincap)
frigid_disrupt = Spell('witch/frigid_disrupt', Bind('s+q', None, 0.2), wincap)
lightning_storm_hv = Spell('witch/lightning_storm_high_voltage', Bind('shift+c', None, 0.8, left_click_casts), wincap)
meteor_shower = Spell('witch/meteor_shower', Bind('s', 'left+right', 2.7), wincap)
residual_lightning_combo = Spell('witch/residual_lightning_combo', Bind(None, 'right', 0.9, hold_bind), wincap)
earth_response = Spell('witch/earth_response', Bind('d', 'left'), wincap)
mana_absorption = Spell('witch/mana_absorption', Bind('space', None, 1), wincap)
meteor = Spell('witch/meteor', Bind('s', 'left+right', 0.8, left_click_casts), wincap)
blizzard = Spell('witch/blizzard', Bind('shift', 'left+right', 1), wincap)
earth_arrow = Spell('witch/earth_arrow', Bind(None, 'left+right', 0.2), wincap)
earthen_eruption = Spell('witch/earthen_eruption', Bind('f', None, 1.8), wincap)
mma = Spell('witch/mma', Bind('s', 'right', 0.3), wincap)
lightning = Spell('witch/lightning', Bind('s+f', None, 0.1), wincap)
fireball = Spell('witch/fireball', Bind('s', 'left', 0.2, left_click_casts), wincap)

# Combos
bolide_combo = Combo([frigid_disrupt, fireball, fireball_explosion, earth_arrow, lightning_storm_hv, residual_lightning_combo, mma])
lightning_combo_part1 = Combo([residual_lightning_combo, fireball, fireball_explosion, lightning_storm_hv])
lightning_combo_part2 = Combo([bolide, frigid_disrupt, mma])
pvp_dps_combo = Combo([earth_arrow, bolide, frigid_disrupt, fireball, fireball_explosion, mma, lightning, residual_lightning_combo, lightning_storm_hv])
pvp_protected_combo = Combo([earth_arrow, mma, bolide, frigid_disrupt, lightning_storm_hv, residual_lightning_combo])
fire_combo = Combo([fireball, fireball_explosion, mma])
small_lightning_combo = Combo([lightning_storm_hv, residual_lightning_combo])


last_debuff = time.time()
last_cast = time.time()
last_lightning_storm = time.time()
last_frigid = time.time()

def bolide_catch():
    if bolide_combo.ready():
        bolide_combo.cast()
        return

def lightning_catch():
    if lightning_combo_part1.ready():
        if lightning_combo_part1.cast():
            if lightning_combo_part2.ready():
                if lightning_combo_part2.cast():
                    if not meteor_shower.on_cooldown():
                        meteor_shower.cast()
        return

def protected_dps():
    if pvp_protected_combo.ready():
        if pvp_protected_combo.cast():
            if not meteor.on_cooldown():
                if meteor.cast():
                    if not bolide.on_cooldown():
                        bolide.cast()
                return
            if not bolide.on_cooldown():
                bolide.cast()
        return

def ranged_dps():
    global last_debuff
    if pvp_dps_combo.ready():
        if pvp_dps_combo.cast():
            if not meteor.on_cooldown():
                meteor.cast()
        return
    if not earth_arrow.on_cooldown() and time.time() - last_debuff > 5:
        if earth_arrow.cast():
            last_debuff = time.time()
        return
    if not meteor.on_cooldown():
        meteor.cast()
        return
    if not bolide.on_cooldown():
        bolide.cast()
        return
    if not frigid_disrupt.on_cooldown():
        frigid_disrupt.cast()
        return
    if fire_combo.ready():
        fire_combo.cast()
        return
    if small_lightning_combo.ready():
        small_lightning_combo.cast()
        return
    if not fireball.on_cooldown():
        fireball.cast()
        return
    if not lightning.on_cooldown():
        lightning.cast()
        return
    

def sa_rotation():
    ss = wincap.get_screenshot()
    if not earth_response.on_cooldown(ss):
        if earth_response.cast():
            # Max SA timing
            # time.sleep(2.8)
            # Without Mana Absorption
            # time.sleep(1.75)
            time.sleep(1.5)
        return
    if not bolide.on_cooldown(ss):
        bolide.cast()
        return
    if not earthquake_evade.on_cooldown(ss):
        earthquake_evade.cast()
        return
    if not aqua_jail.on_cooldown(ss):
        if aqua_jail.cast():
            time.sleep(0.6)
        return
    if not earthen_eruption.on_cooldown(ss):
        earthen_eruption.cast()
        return
    if not mana_absorption.on_cooldown(ss):
        mana_absorption.cast(hotbar=True)
        return


while(True):
    if keyboard.is_pressed('x'):
        sa_rotation()
    if keyboard.is_pressed('F23'):
        ranged_dps()
    if keyboard.is_pressed('F24'):
        protected_dps()
        # protected_dps()
        # ranged_dps()

    # # debug the loop rate
    # print('FPS {}'.format(1 / (time.time() - loop_time)))
    # loop_time = time.time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')