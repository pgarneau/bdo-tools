import os
import time
from common.windowcapture import wincap
from common.spell import Spell, NoCooldownSpell, link_spells, Iframe
from common.combo import Combo
from common.bind import Bind, hold_bind, hold_bind_release_early
from common.vision import Vision

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# buffs
crit_buff = Spell(Vision('crit', 0.98), None)
ap_buff = Spell(Vision('ap', 0.98), None)
shai_buff = Spell(Vision('shai_speed', 0.98), None)

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
    speed = speed + 0.1
    
    return speed

# Pre-awak

# Awakening
glorious_advance_1h = Spell(Vision('glorious_advance'), Bind('s', 'left'), 0.75, 5, get_attack_speed)
cleansing_flame = Spell(Vision('cleansing_flame'), Bind('shift+f', None), 1.1, 6, get_attack_speed)
flow_to_ashes = Spell(Vision('flow_to_ashes'), Bind(None, 'left'), 0.6, 7, get_attack_speed)
scalding_thorn = Spell(Vision('scalding_thorn'), Bind('f', None), 0.45, 5, get_attack_speed)
dragons_maw = Spell(Vision('dragons_maw'), Bind('shift', 'left'), 0.2, 10, get_attack_speed)
dragons_maw_cheat = NoCooldownSpell('dragons_maw', Bind(None, 'left', hold_bind), 2.0, get_attack_speed)
searing_fang = Spell(Vision('searing_fang'), Bind('shift', 'right', hold_bind), 1.35, 8, get_attack_speed)
scornful_slash = Spell(Vision('scornful_slash'), Bind('s', 'right', hold_bind), 0.75, 5, get_attack_speed)
scornful_slash_cheat = NoCooldownSpell('scornful_slash', Bind('s', 'right', hold_bind), 1.35, get_attack_speed)
god_incinerator = Spell(Vision('god_incinerator'), Bind('shift+q', None), 1.8, 8, get_attack_speed)
fireborne_rupture = Spell(Vision('fireborne_rupture'), Bind('1', None, hotbar=True), 0.5, 4, get_attack_speed)
fireborne_rupture_flow = Spell(Vision('fireborne_rupture'), Bind('q', None), 0.5, 4, get_attack_speed)
e_buff = Spell(Vision('e_buff'), Bind('shift+e', None), 0.5, 4, get_attack_speed)

# Combos
cleansing_flame_combo = Combo([cleansing_flame, flow_to_ashes, scalding_thorn])
football_field_combo = Combo([dragons_maw, dragons_maw_cheat])
god_incinerator_combo = Combo([god_incinerator, fireborne_rupture_flow])
scornful_slash_combo = Combo([scornful_slash, scornful_slash_cheat])

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
    #if e_buff.ready():
    #    e_buff.cast(context)
    if glorious_advance_1h.ready() and time.time() - glorious_advance_1h.shared_data.last_cast >= 17:
        glorious_advance_1h.cast(context)
    elif fireborne_rupture.ready() and time.time() - fireborne_rupture.shared_data.last_cast >= 10:
        fireborne_rupture.cast(context)
    elif football_field_combo.ready():
        football_field_combo.cast(context)
    elif searing_fang.ready():
        searing_fang.cast(context)
    elif god_incinerator_combo.ready():
        god_incinerator_combo.cast(context)
    elif cleansing_flame_combo.ready():
        cleansing_flame_combo.cast(context)
    elif scornful_slash.ready():
        scornful_slash.cast(context)
            