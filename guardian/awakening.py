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
ap_buff = Spell(Vision('ap', 0.98), None)
shai_buff = Spell(Vision('shai_speed', 0.98), None)
e_buff_buff = Spell(Vision('e_buff_buff', 0.98), None)

def get_attack_speed():
    speed = 1
    buffs = wincap.get_buffs()
    #if ap_buff.ready(buffs): guardian has an ap prebuff showing this icon so this doesnt work
    #    speed = speed + 0.05
    # elif cast_speed_buff.ready(buffs):
    #     speed = speed + 0.1
    if shai_buff.ready(buffs):
        speed = speed + 0.15
    
    # Generic modifier to press keybinds faster than actual animations
    speed = speed + 0.1
    
    return speed

def get_ap_buff():
    buffs = wincap.get_buffs()
    if ap_buff.ready(buffs):
        return True
    return False
    
def get_bsr_buff():
    buffs = wincap.get_buffs()
    x, y = crit_buff.ready(buffs, count=True)
    if x and y >= 2:
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
    if e_buff_buff.ready(buffs):
        return False
    return True

# Pre-awak

# Awakening
glorious_advance_1h = Spell(Vision('glorious_advance'), Bind('s', 'left'), 0.75, 5, get_attack_speed)
cleansing_flame = Spell(Vision('cleansing_flame'), Bind('shift+f', None), 0.9, 6, get_attack_speed)
flow_to_ashes = Spell(Vision('flow_to_ashes'), Bind(None, 'left'), 0.6, 7, get_attack_speed)
scalding_thorn = Spell(Vision('scalding_thorn'), Bind('f', None), 0.45, 5, get_attack_speed)
dragons_maw = Spell(Vision('dragons_maw'), Bind('shift', 'left'), 0.2, 10, get_attack_speed)
dragons_maw_cheat = NoCooldownSpell('dragons_maw', Bind(None, 'left', hold_bind), 2.0, get_attack_speed)
searing_fang = Spell(Vision('searing_fang'), Bind('shift', 'right', hold_bind), 1.35, 8, get_attack_speed)
scornful_slash = Spell(Vision('scornful_slash'), Bind('s', 'right', hold_bind), 0.75, 5, get_attack_speed)
scornful_slash_cheat = NoCooldownSpell('scornful_slash', Bind('s', 'right', hold_bind), 1.35, get_attack_speed)
god_incinerator_accel = Spell(Vision('god_incinerator'), Bind('shift+q', None), 1.3, 8, get_attack_speed)
god_incinerator = Spell(Vision('god_incinerator'), Bind('shift+q', None), 1.8, 8, get_attack_speed)
fireborne_rupture = Spell(Vision('fireborne_rupture'), Bind('q', None), 0.5, 4, get_attack_speed)
fireborne_rupture_qs = Spell(Vision('fireborne_rupture'), Bind('1', None, hotbar=True), 0.5, 4, get_attack_speed)
e_buff = Spell(Vision('e_buff'), Bind('shift+e', None), 0.5, 4, get_attack_speed)
bsr_buff = Spell(Vision('bsr_100'), Bind('z', None), 1.0, 60, get_attack_speed)

# Combos
cleansing_flame_combo = Combo([cleansing_flame, flow_to_ashes, scalding_thorn])
football_field_combo = Combo([dragons_maw, dragons_maw_cheat])
god_incinerator_combo = Combo([god_incinerator, fireborne_rupture])
scornful_slash_combo = Combo([scornful_slash, scornful_slash_cheat])
glorgodcombo = Combo([glorious_advance_1h, god_incinerator_accel, fireborne_rupture])

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
    if fireborne_rupture_qs.ready() and ebuff_inactive() and time.time() - fireborne_rupture.shared_data.last_cast >= 7:
        fireborne_rupture_qs.cast(context)
    elif e_buff.ready():
        e_buff.cast(context)
    elif bsr_buff.ready() and ebuff_inactive():
        bsr_buff.cast(context)
    elif glorious_advance_1h.ready() and god_incinerator_accel.ready():
        glorgodcombo.cast(context)
    elif god_incinerator_combo.ready():
        god_incinerator_combo.cast(context)
    elif football_field_combo.ready():
        football_field_combo.cast(context)
    elif searing_fang.ready():
        searing_fang.cast(context)
    elif cleansing_flame_combo.ready():
        cleansing_flame_combo.cast(context)
    elif scornful_slash.ready():
        scornful_slash.cast(context)
            