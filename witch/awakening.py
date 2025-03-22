import os
import time
from common.windowcapture import wincap
from common.spell import Spell, NoCooldownSpell, link_spells, Iframe, BsrConsume
from common.combo import Combo
from common.bind import Bind, hold_bind, hold_bind_release_early
from common.vision import Vision

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# buffs
crit_buff = Spell(Vision('crit', 0.98), None)
speedspell = Spell(Vision('attack_speed', 0.98), None)
ap_buff = Spell(Vision('ap', 0.98), None)
shai_buff = Spell(Vision('shai_speed', 0.98), None)
ebuff_buff = Spell(Vision('ebuff_buff', 0.98), None)

#fissure-anti-movement 
fissurecount = 0

def get_attack_speed():
    speed = 1
    buffs = wincap.get_buffs()
    if ap_buff.ready(buffs):
        speed = speed + 0.05
    # elif cast_speed_buff.ready(buffs):
    #     speed = speed + 0.1
    if shai_buff.ready(buffs):
        speed = speed + 0.15
    
    # Generic modifier to press keybinds faster than actual animations
    speed = speed + 0.2
    
    return speed

def get_ap_buff():
    buffs = wincap.get_buffs()
    if ap_buff.ready(buffs):
        return True
    return False
    
def get_speed_spell():
    buffs = wincap.get_buffs()
    if speedspell.ready(buffs):
        return True
    return False

def get_ap_while_bsr():
    buffs = wincap.get_buffs()
    x, y, z = ap_buff.ready(buffs, count=True)
    if x and y and z>= 3:
        return True
    return False

def ebuff_inactive():
    buffs = wincap.get_buffs()
    if ebuff_buff.ready(buffs):
        return False
    return True

# Pre-awak
speedspellab = Spell(Vision('speed_spell'), Bind('1', None, hotbar=True), 0.6, 50, get_attack_speed)


# Awakening
voltaic_pulse = Spell(Vision('a_voltaic_pulse'), Bind('shift+f', None), 1.0, 6, get_attack_speed)
eggyoke = Spell(Vision('eggyoke'), Bind('shift', 'right', hold_bind), 2.4, 13, get_attack_speed)
fisherwave = Spell(Vision('fissure_wave'), Bind('s', 'left+right', hold_bind), 1.6, 3, get_attack_speed)
equilibrium_break = Spell(Vision('a_equilibrium_break'), Bind('shift', 'left'), 1.6, 6, get_attack_speed)
thunder_storm = Spell(Vision('thunderstorm'), Bind('s+f', None), 1.0, 8, get_attack_speed)
toxic_flood = Spell(Vision('toxic_flood'), Bind('e', None), 0.5, 15, get_attack_speed)
thorns_of_denial = Spell(Vision('deluluthorns'), Bind('shift+q', None), 1.2, 8, get_attack_speed)
magical_evasion_back = Spell(Vision('magical_evasion'), Bind('shift+s', None), 0.5, 8, get_attack_speed)

e_buff = Spell(Vision('e_buff', threshold=0.9), Bind('shift+e', None), 0.5, 180, get_attack_speed)
bsr_buff = Spell(Vision('bsr_100'), Bind('z', None), 1.0, 60, get_attack_speed)

# Combos

def crit_buff_active():
    buffs = wincap.get_buffs()
    x, y = crit_buff.ready(buffs, count=True)
    if x and y >= 2:
        return True
    return False

def shai_buff_active():
    buffs = wincap.get_buffs()
    if shai_buff.ready(buffs):
        return True
    return False

def pve(context):
    global fissurecount
    if e_buff.ready() and not get_speed_spell():
        e_buff.cast(context)
    elif ebuff_inactive and bsr_buff.ready():
        bsr_buff.cast(context)
    elif ebuff_inactive and speedspellab.ready() and not get_ap_buff():
        speedspellab.cast(context)
    elif toxic_flood.ready():
        toxic_flood.cast(context)
    elif fissurecount == 12:
        magical_evasion_back.cast(context)
        fissurecount = 0
    elif equilibrium_break.ready() and time.time() - equilibrium_break.shared_data.last_cast >= 10:
        equilibrium_break.cast(context)
    elif eggyoke.ready():
        eggyoke.cast(context)
    elif fisherwave.ready() and time.time() - fisherwave.shared_data.last_cast >= 6:
        fisherwave.cast(context)
        fissurecount += 1
    elif voltaic_pulse.ready():
        voltaic_pulse.cast(context)
    elif thunder_storm.ready():
        thunder_storm.cast(context)
    elif thorns_of_denial.ready():
        thorns_of_denial.cast(context)
        fissurecount += 1
    elif equilibrium_break.ready():
        equilibrium_break.cast(context)
    elif fisherwave.ready():
        fisherwave.cast(context)
        fissurecount += 1