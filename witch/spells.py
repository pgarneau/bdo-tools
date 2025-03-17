import os
import time
from windowcapture import WindowCapture
from spell import Spell, NoCooldownSpell
from combo import Combo
from bind import Bind, hold_bind, hold_bind_release_early
from vision import find_nearby_targets

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their 
# own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# initialize the WindowCapture class
wincap = WindowCapture()

def get_cast_speed():
    speed = 1
    buffs = wincap.get_buffs()
    if ap_buff.ready(buffs):
        speed = speed + 0.25
    elif elemental_palace_buff.ready(buffs) or cast_speed_buff.ready(buffs):
        speed = speed + 0.2
    if shai_buff.ready(buffs):
        speed = speed + 0.1
    
    # Generic modifier to press keybinds faster than actual animations
    speed = speed + 0.3
    
    return speed

#buffs
elemental_palace_buff = Spell('elemental_palace_buff', None, threshold=0.98)
cast_speed_buff = Spell('cast_speed', None, threshold=0.98)
shai_buff = Spell('shai_speed', None, threshold=0.98)
ap_addon_buff = Spell('ap_addon', None, threshold=0.98)
ap_buff = Spell('ap', None, threshold=0.98)

#Debuffs
dp_debuff = Spell('magic_dp_debuff', None, threshold=0.98)

# Succession
earth_arrow = Spell('earth_arrow', Bind(None, 'left+right', 0.5), 3, get_cast_speed)
voltaic_pulse = Spell('voltaic_pulse', Bind('w+c', None, 0.6), 6, get_cast_speed)
mma = Spell('mma', Bind('s', 'right', 0.4), 3, get_cast_speed)
frigid_fog_control = Spell('frigid_fog_control', Bind('s+q', None, 0.55), 10, get_cast_speed)
freeze = Spell('freeze', Bind('s+e', None, 0.2), 6, get_cast_speed)
lightning = Spell('lightning', Bind('s+f', None, 0.25), 5, get_cast_speed)
lightning_storm_strike = Spell('lightning_storm_strike', Bind('shift+c', None, 0.8), 9, get_cast_speed)
residual_lightning_high_voltage = Spell('residual_lightning_high_voltage', Bind('f', None, 0.7), 9, get_cast_speed)
meteor_shower_focus = Spell('meteor_shower_focus', Bind('s', 'left+right', 1.3, hold_bind_release_early), 18, get_cast_speed)
voltaic_discharge_focus = Spell('voltaic_discharge_focus', Bind('shift', 'right', 1.4), 30, get_cast_speed)
equilibrium_break = Spell('equilibrium_break', Bind('s+c', None, 0.95), 6, get_cast_speed)
fireball_explosion_spread = Spell('fireball_explosion_spread', Bind('shift', 'left', 0.7), 9, get_cast_speed)
earthquake_destruction = Spell('earthquake_destruction', Bind('shift+f', None, 1.25), 12, get_cast_speed)
blizzard_domain = Spell('blizzard_domain', Bind('shift', 'left+right', 2.4), 20, get_cast_speed)
fireball = Spell('fireball', Bind('s', 'left', 0.45, hold_bind_release_early), 3, get_cast_speed)
earthen_eruption = Spell('earthen_eruption', Bind('f', None, 2.6), 12, get_cast_speed)

elemental_palace = Spell('elemental_palace', Bind('2', None, 1), 180, get_cast_speed)
speed_spell = Spell('speed_spell', Bind('1', None, 1), 50, get_cast_speed)

# Combos
lightning_combo = Combo([lightning_storm_strike, residual_lightning_high_voltage])
freeze_mma = Combo([freeze, mma])
lightning_mma = Combo([lightning, mma])


def cast_speed_active():
    buffs = wincap.get_buffs()
    if elemental_palace_buff.ready(buffs) or cast_speed_active(buffs):
        return True
    return False

def target_dp_debuffed():
    debuffs = wincap.get_debuffs()
    if dp_debuff.ready(debuffs):
        return True
    return False

def ap_buff_active():
    buffs = wincap.get_buffs()
    if ap_addon_buff.ready(buffs):
        return True
    return False

def low_mob_density():
    nearby_hp_bars = wincap.get_nearby_targets()
    num_targets = find_nearby_targets(nearby_hp_bars)
    if num_targets <= 2:
        return True
    return False

def can_speed_spell():
    buffs = wincap.get_buffs()
    if elemental_palace_buff.ready(buffs) or ap_buff.ready(buffs):
        return False
    return True
