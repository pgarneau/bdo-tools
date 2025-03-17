import os
import time
from windowcapture import WindowCapture
from spell import Spell, NoCooldownSpell
from .q_block import QBlock
from combo import Combo
from bind import Bind, hold_bind, hold_bind_release_early

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their 
# own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# initialize the WindowCapture class
wincap = WindowCapture()

#buffs
cast_speed_buff = Spell('cast_speed', None, threshold=0.98)
ele_invocation_buff = Spell('elemental_invocation_buff', None, threshold=0.98)
shai_buff = Spell('shai_speed', None, threshold=0.98)


def get_attack_speed():
    speed = 1
    buffs = wincap.get_buffs()
    if cast_speed_buff.ready(buffs):
        speed = speed + 0.25
    if shai_buff.ready(buffs):
        speed = speed + 0.1
    
    # Generic modifier to press keybinds faster than actual animations
    speed = speed + 0.3
    
    return speed

# Awak
elemental_invocation = Spell('elemental_invocation', Bind('1', None, 2, hotbar=True), 180, get_attack_speed)
earth_reap = Spell('earth_reap', Bind('s+q', None, 1.85), 10, get_attack_speed)
earth_till = Spell('earth_till', Bind('shift+q', None, 1.7), 12, get_attack_speed)
fire_blaze = Spell('fire_blaze', Bind('shift', 'right', 0.85), 12, get_attack_speed)
fire_blaze_flow = Spell('fire_blaze', Bind('shift', 'right', 1.7, hold_bind), 12, get_attack_speed)
fire_spread = Spell('fire_spread', Bind('s', 'right', 0.33), 6, get_attack_speed)
metal_pour = Spell('metal_pour', Bind('s', 'left', 1), 10, get_attack_speed)
metal_temper = Spell('metal_temper', Bind('shift', 'left', 0.2, hold_bind), 12, get_attack_speed)
metal_temper_flow = Spell('metal_temper', Bind('shift', 'left', 1.25, hold_bind), 12, get_attack_speed)
water_weave = Spell('water_weave', Bind('shift+e', None, 0.3), 12, get_attack_speed)
water_weave_flow = Spell('water_weave', Bind('shift+e', None, 1.25, hold_bind), 12, get_attack_speed)
wood_bend = Spell('wood_bend', Bind('shift+f', None, 1.9), 12, get_attack_speed)
wood_stake = Spell('wood_stake', Bind('f', None, 2.65, hold_bind), 6, get_attack_speed)
sundering_sweep = Spell('sundering_sweep', Bind(None, 'right', 1.3, hold_bind_release_early), 7, get_attack_speed)
sundering_sweep_1hit = Spell('sundering_sweep', Bind(None, 'right', 0.6, hold_bind_release_early), 7, get_attack_speed)
enlightened_haze = Spell('enlightened_haze', Bind('w+f', None, 1), 5, get_attack_speed)

# Pre-awak
taeguk = Spell('taeguk', Bind('shift+q', None, 1.2), 20, get_attack_speed)
rabam = Spell('reverse_blade_waltz', Bind('shift+z', None, 0.8), 6, get_attack_speed)
q_block = QBlock('q_block', Bind('q', None, 0.2), get_attack_speed)


# Combos
part_1 = Combo([water_weave, metal_pour, earth_reap, metal_temper])
part_1_speed = Combo([water_weave_flow, metal_pour, earth_reap, metal_temper_flow])
part_2 = Combo([earth_till, fire_blaze, wood_bend, q_block, fire_spread, wood_stake])
part_2_speed = Combo([earth_till, fire_blaze_flow, wood_bend, q_block, fire_spread, wood_stake])

metal_earth_metal = Combo([metal_pour, earth_reap, metal_temper])
metal_earth_metal_speed = Combo([metal_pour, earth_reap, metal_temper_flow])
earth_metal = Combo([earth_reap, metal_temper])
earth_metal_speed = Combo([earth_reap, metal_temper_flow])

fire_wood_fire_wood = Combo([fire_blaze, wood_bend, fire_spread, wood_stake])
fire_wood_fire_wood_speed = Combo([fire_blaze_flow, wood_bend, fire_spread, wood_stake])
wood_fire_wood = Combo([wood_bend, fire_spread, wood_stake])
fire_wood = Combo([fire_spread, wood_stake])

# experiment = Combo([wood_stake, q_block, sundering_sweep, water_weave])
pre_awak_combo = Combo([rabam, taeguk, enlightened_haze])



def init_spells():
    screenshot = wincap.get_skills()
    elemental_invocation.ready(screenshot)
    earth_reap.ready(screenshot)
    earth_till.ready(screenshot)
    fire_blaze.ready(screenshot)
    fire_blaze_flow.ready(screenshot)
    fire_spread.ready(screenshot)
    metal_pour.ready(screenshot)
    metal_temper.ready(screenshot)
    metal_temper_flow.ready(screenshot)
    water_weave.ready(screenshot)
    water_weave_flow.ready(screenshot)
    wood_bend.ready(screenshot)
    wood_stake.ready(screenshot)
    sundering_sweep.ready(screenshot)
    sundering_sweep_1hit.ready(screenshot)


    return True


def cast_speed_active():
    buffs = wincap.get_buffs()
    if cast_speed_buff.ready(buffs):
        return True
    return False

def shai_buff_active():
    buffs = wincap.get_buffs()
    if shai_buff.ready(buffs):
        return True
    return False

