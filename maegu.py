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

# Active Keybinds
settings.init(['x', 'F23', 'F24'])

# Initialize Spells

# Spells
heavenward_dance = Spell('maegu/heavenward_dance', Bind('w', 'right', 1), wincap)
spirited_away = Spell('maegu/spirited_away', Bind('s', 'left', 1.2), wincap)
petal_play = Spell('maegu/petal_play', Bind('shift', 'left', 0.7), wincap)
heavenly_return = Spell('maegu/heavenly_return', Bind('2', None, 0.5), wincap)
foxflare = Spell('maegu/foxflare', Bind('shift+q', None, 0.7), wincap)
bristling_sparks = Spell('maegu/bristling_sparks', Bind('shift', 'right', 2.2), wincap)
bared_claws = Spell('maegu/bared_claws', Bind('d', 'left', 0.2), wincap)
foxspirit_tag = Spell('maegu/foxspirit_tag', Bind(None, 'right', 0.3, hold_bind), wincap)
charmed = Spell('maegu/charmed', Bind('space'), wincap)
nukduri_dance = Spell('maegu/nukduri_dance', Bind('shift+c', None, 0.7), wincap)
spirit_swirl = Spell('maegu/spirit_swirl', Bind('shift+f', None, 2), wincap)
flower_shroud = Spell('maegu/flower_shroud', Bind('w+e', None, 1), wincap)

spirit_swirl_combo_1 = Combo([heavenward_dance, spirit_swirl])
spirit_swirl_combo_2 = Combo([flower_shroud, spirit_swirl])
nukduri_dance_combo_1 = Combo([heavenward_dance, nukduri_dance])
nukduri_dance_combo_2 = Combo([flower_shroud, nukduri_dance])
foxspirit_tag_combo = Combo([bared_claws, foxspirit_tag])
petal_play_combo = Combo([spirited_away, petal_play])

last_cast = time.time()

def elvia():
    global last_cast
    ss = wincap.get_screenshot()
    if petal_play_combo.ready():
        if petal_play_combo.cast():
            last_cast = time.time()
        return
    if foxspirit_tag_combo.ready():
        foxspirit_tag_combo.cast()
    if not foxspirit_tag.on_cooldown() and time.time() - last_cast <= 1:
        foxspirit_tag.cast()
        return
    if not heavenward_dance.on_cooldown(ss):
        if heavenward_dance.cast():
            last_cast = time.time()
        return
    if not foxflare.on_cooldown(ss):
        if foxflare.cast():
            last_cast = time.time()
        return
    if not bristling_sparks.on_cooldown(ss):
        if bristling_sparks.cast():
            last_cast = time.time()
        return
    if nukduri_dance_combo_2.ready():
        if nukduri_dance_combo_2.cast():
            last_cast = time.time()
        return
    if spirit_swirl_combo_2.ready():
        if spirit_swirl_combo_2.cast():
            last_cast = time.time()
        return
    if not spirit_swirl.on_cooldown(ss):
        if spirit_swirl.cast():
            last_cast = time.time()
        return
    if not nukduri_dance.on_cooldown(ss):
        if nukduri_dance.cast():
            last_cast = time.time()
        return
    
    
    
def orcs(buffs):
    ap_addon_buff = False
    if ap_addon.is_active(screenshot=buffs):
        print("AP ADDON ON")
        ap_addon_buff = True

    if not ap_addon_buff and not bristling_sparks.on_cooldown():
        bristling_sparks.cast()
        return
    if not ap_addon_buff and not spirit_swirl.on_cooldown():
        if not heavenward_dance.on_cooldown():
            heavenward_dance.cast()
        elif not flower_shroud.on_cooldown():
            flower_shroud.cast()
        spirit_swirl.cast()
        return
    # if not ap_buff and not charmed.on_cooldown():
    #     charmed.cast()
    #     return
    # if not ap_buff and not nukduri_dance.on_cooldown():
    #     nukduri_dance.cast()
    #     return
    
    if not foxspirit_tag.on_cooldown():
        foxspirit_tag.cast()
        return
    
    if not foxflare.on_cooldown():
        foxflare.cast()
        return
    
    if not charmed.on_cooldown():
        charmed.cast()
        return
    
    if not spirited_away.on_cooldown():
        spirited_away.cast()
        if not petal_play.on_cooldown():
            petal_play.cast()
        return
    
    if not bristling_sparks.on_cooldown():
        bristling_sparks.cast()
        return
    
    if not heavenward_dance.on_cooldown():
        heavenward_dance.cast()
        return
    
    if not flower_shroud.on_cooldown():
        flower_shroud.cast()
        return
    
    if not nukduri_dance.on_cooldown():
        nukduri_dance.cast()
        return
    
    if not spirit_swirl.on_cooldown():
        if not heavenward_dance.on_cooldown():
            heavenward_dance.cast()
        elif not flower_shroud.on_cooldown():
            flower_shroud.cast()
        if not nukduri_dance.on_cooldown():
            nukduri_dance.cast()
        spirit_swirl.cast()
        return
    
    if not petal_play.on_cooldown():
        petal_play.cast()
        return
    
    if not heavenly_return.on_cooldown():
        heavenly_return.cast()
        return

def dps(buffs):
    mov_speed = False
    att_speed = False
    ap_buff = False
    ap_addon_buff = False
    if not movement_speed.on_cooldown(buffs):
        mov_speed = True
    if not attack_speed.on_cooldown(buffs):
        att_speed = True
    if not ap.on_cooldown(buffs):
        ap_buff = True
    if not ap_addon.on_cooldown(buffs):
        ap_addon_buff = True

    if not ap_addon_buff and not bristling_sparks.on_cooldown():
        bristling_sparks_short.cast()
        bared_claws.cast()
        return
    if not ap_addon_buff and not spirit_swirl.on_cooldown():
        if not heavenward_dance.on_cooldown():
            heavenward_dance.cast()
        elif not flower_shroud.on_cooldown():
            flower_shroud.cast()
        if not nukduri_dance.on_cooldown():
            nukduri_dance.cast()
        spirit_swirl.cast()
        return
    # if not mov_speed and not spirited_away.on_cooldown():
    #     spirited_away.cast()
    #     if not petal_play.on_cooldown():
    #         petal_play.cast()
    #     return
    # if not mov_speed and not flower_shroud.on_cooldown():
    #     flower_shroud.cast()
    #     return
    
    if not foxspirit_tag.on_cooldown():
        foxspirit_tag.cast()
        return
    
    if not spirited_away.on_cooldown():
        spirited_away.cast()
        if not petal_play.on_cooldown():
            petal_play.cast()
        return
    
    if not spirit_swirl.on_cooldown():
        if not heavenward_dance.on_cooldown():
            heavenward_dance.cast()
        elif not flower_shroud.on_cooldown():
            flower_shroud.cast()
        if not nukduri_dance.on_cooldown():
            nukduri_dance.cast()
        spirit_swirl.cast()
        return
    
    if not heavenward_dance.on_cooldown():
        heavenward_dance.cast()
        return
    
    if not foxflare.on_cooldown():
        foxflare.cast()
        return
    
    if not charmed.on_cooldown():
        charmed.cast()
        return

    if not bristling_sparks.on_cooldown():
        bristling_sparks.cast()
        return
    
    if not bared_claws.on_cooldown():
        bared_claws.cast()
        return
    
    if not petal_play.on_cooldown():
        petal_play.cast()
        return
    
    if not flower_shroud.on_cooldown():
        flower_shroud.cast()
        return
    
    if not heavenly_return.on_cooldown():
        heavenly_return.cast()
        return
    
    return



def main():
    while(True):
        if keyboard.is_pressed('x') or keyboard.is_pressed('F23'):
            elvia()

        # # debug the loop rate
        # print('FPS {}'.format(1 / (time.time() - loop_time)))
        # loop_time = time.time()

        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break

    print('Done.')

if __name__ == "__main__":
    main()