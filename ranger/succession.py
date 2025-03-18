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
e_buff_icon = Spell(Vision('e_buff_icon', 0.98), None)

def get_attack_speed():
    speed = 1
    buffs = wincap.get_buffs()
    if ap_buff.ready(buffs):
        speed = speed + 0.15
    if e_buff_icon.ready(buffs):
        speed = speed + 0.2
    # elif cast_speed_buff.ready(buffs):
    #     speed = speed + 0.1
    if shai_buff.ready(buffs):
        speed = speed + 0.15
    
    # Generic modifier to press keybinds faster than actual animations
    speed = speed + 0.1
    
    return speed

# Pre-awak
magnus = Spell(Vision('magnus'), Bind('s+f', None), 0.48, 9, get_attack_speed)
squall_shot = Spell(Vision('squall_shot'), Bind('shift+x', None), 0.9, 8, get_attack_speed)
flow_bypassing_wind = Spell(Vision('flow_bypassing_wind'), Bind('shift','right'), 0.43, 6, get_attack_speed)

# Succession
prime_regeneration = Spell(Vision('prime_regeneration'), Bind('s+c', None), 0.75, 7, get_attack_speed)
prime_natures_tremble = Spell(Vision('prime_natures_tremble'), Bind('w+c', None), 0.75, 7, get_attack_speed)
prime_penetrating_wind = Spell(Vision('prime_penetrating_wind'), Bind('shift', 'right'), 0.09, 7, get_attack_speed)
prime_razor_wind = Spell(Vision('prime_razor_wind'), Bind('e', 'left', hold_bind), 2.3, 8, get_attack_speed)
prime_tearing_arrow = Spell(Vision('prime_tearing_arrow'), Bind('s+e', None), 0.1, 7, get_attack_speed)
prime_tearing_arrow_cheat = NoCooldownSpell('prime_tearing_arrow', Bind(None, 'left', hold_bind), 1.25, get_attack_speed)
prime_ultimate_blasting_gust = Spell(Vision('prime_ultimate_blasting_gust'), Bind(None, 'left', hold_bind), 1.9, 8, get_attack_speed)
prime_shotgun = Spell(Vision('prime_shotgun'), Bind('space', None), 0.3, 3, get_attack_speed)
wotw = Spell(Vision('wotw'), Bind('shift+q', None), 0.4, get_attack_speed)
e_buff = Spell(Vision('e_buff'), Bind('shift+e', None), 0.9, 180, get_attack_speed)
prime_hop = NoCooldownSpell('prime_hop', Bind('w', 'right'), 0.7, get_attack_speed)

# Combos
combo_part_1 = Combo([prime_razor_wind, prime_penetrating_wind, flow_bypassing_wind, prime_shotgun, magnus])
combo_part_2 = Combo([prime_regeneration, prime_tearing_arrow, prime_tearing_arrow_cheat, prime_hop])
combo_part_3 = Combo([squall_shot, prime_ultimate_blasting_gust])


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
    if e_buff.ready():
        e_buff.cast(context)
    elif wotw.ready():
        wotw.cast(context)
    elif prime_natures_tremble.ready() and time.time() - prime_natures_tremble.shared_data.last_cast >= 10:
        prime_natures_tremble.cast(context)
    elif combo_part_1.ready():
        combo_part_1.cast(context)
    elif combo_part_2.ready():
        combo_part_2.cast(context)
    elif combo_part_3.ready():
        combo_part_3.cast(context)
            