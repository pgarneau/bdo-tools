import os
import time
from common.windowcapture import wincap
from common.spell import Spell, NoCooldownSpell, link_spells, Iframe
from common.combo import Combo
from common.bind import Bind, hold_bind, hold_bind_release_early
from common.vision import Vision

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# buffs
cast_speed_buff = Spell(Vision('cast_speed', 0.98), None)
crit_buff = Spell(Vision('crit', 0.98), None)
ap_buff = Spell(Vision('ap', 0.98), None)
shai_buff = Spell(Vision('shai_speed', 0.98), None)
e_buff = Spell(Vision('e_buff', 0.98), None)
dp_debuff = Spell(Vision('magic_dp_debuff', 0.98), None)

def get_attack_speed():
    speed = 1
    buffs = wincap.get_buffs()
    if ap_buff.ready(buffs):
        speed = speed + 0.25
    # elif cast_speed_buff.ready(buffs):
    #     speed = speed + 0.1
    if shai_buff.ready(buffs):
        speed = speed + 0.1
    
    # Generic modifier to press keybinds faster than actual animations
    speed = speed + 0.1
    
    return speed

# Awak
blade_of_darkness = Spell(Vision('blade_of_darkness'), Bind('shift', 'right'), 0.25, 8, get_attack_speed)
cartian_nightmare = Spell(Vision('cartian_nightmare'), Bind('shift+e', None), 5.8, 15, get_attack_speed)
cartian_protection = Spell(Vision('cartian_protection'), Bind(None, 'right'), 0.4, 6, get_attack_speed)
dead_hunt = Spell(Vision('dead_hunt'), Bind('s', 'left'), 1, 6, get_attack_speed)
grim_reaper_judgement = Spell(Vision('grim_reaper_judgement'), Bind('space', 'left+right'), 1, 8, get_attack_speed)
grim_reaper_judgement_cheat1 = Spell(Vision('grim_reaper_judgement'), Bind(None, 'left+right'), 0.1, 8, get_attack_speed)
grim_reaper_judgement_cheat2 = NoCooldownSpell('grim_reaper_judgement', Bind('space', 'left+right'), 0.9, get_attack_speed)
soul_harvest = Spell(Vision('soul_harvest'), Bind('shift+q', None), 0.75, 5, get_attack_speed)
soul_reaper = Spell(Vision('soul_reaper'), Bind('3', None, hotbar=True), 1.1, 7, get_attack_speed)
swirling_darkness = Spell(Vision('swirling_darkness'), Bind('shift+f', None), 0.6, 8, get_attack_speed)
turn_back_slash = Spell(Vision('turn_back_slash'), Bind('s', 'right'), 0.7, 5, get_attack_speed)
turn_back_slash_cancel = Spell(Vision('turn_back_slash'), Bind('s', 'right'), 0.2, 5, get_attack_speed)
vile_plan = Spell(Vision('vile_plan'), Bind('space', None), 0.7, 5, get_attack_speed)
vile_plan_cancel = Spell(Vision('vile_plan'), Bind('space', None), 0.4, 5, get_attack_speed)
violation = Spell(Vision('violation'), Bind('w', 'right'), 0.5, 6, get_attack_speed)
violation_2 = NoCooldownSpell('violation', Bind('w', 'right'), 1.3, get_attack_speed)
wings_of_the_crow_awak = Spell(Vision('wings_of_the_crow'), Bind('w+e', None), 0.45, 4, get_attack_speed)
night_crow_awak = Spell(Vision('night_crow_awak'), Bind(None, 'middle'), 0.5, 1, get_attack_speed)

link_spells(turn_back_slash, turn_back_slash_cancel)
link_spells(vile_plan, vile_plan_cancel)

# Pre-awak
dark_tendrils_hotbar = Spell(Vision('dark_tendrils'), Bind('2', None, hotbar=True), 1.4, 11, get_attack_speed)
midnight_stinger = Spell(Vision('midnight_stinger'), Bind('shift', 'left'), 0.4, 2, get_attack_speed)
engulfing_shadow = Spell(Vision('engulfing_shadow'), Bind('shift+z', None), 0.65, 7, get_attack_speed)
shadow_ignition = Spell(Vision('shadow_ignition'), Bind('shift+x', None), 0.5, 10, get_attack_speed)
shadow_hellfire_hotbar = Spell(Vision('shadow_hellfire'), Bind('1', None, hotbar=True), 0.6, 4, get_attack_speed)
wings_of_the_crow = Spell(Vision('wings_of_the_crow'), Bind('w', 'right'), 0.45, 4, get_attack_speed)
imminent_doom = Spell(Vision('imminent_doom'), Bind('shift+e', 'right'), 0.3, 18, get_attack_speed)
bloody_calamity = Spell(Vision('bloody_calamity'), Bind('space', None), 0.15, 20, get_attack_speed)
shadow_hellfire = Spell(Vision('shadow_hellfire'), Bind(None, 'right', hold_bind_release_early), 0.6, 4, get_attack_speed)
dark_tendrils = Spell(Vision('dark_tendrils'), Bind('s+e', None), 1.4, 11, get_attack_speed)

iframe_right = Iframe(Bind('shift+d', None), 0.6, get_attack_speed)
iframe_left = Iframe(Bind('shift+a', None), 0.6, get_attack_speed)

# Combos
tbs_blade_opener = Combo([night_crow_awak, turn_back_slash_cancel, blade_of_darkness, soul_harvest, vile_plan_cancel])
tbs_blade = Combo([turn_back_slash, blade_of_darkness])
tbs_blade_soul_vile = Combo([turn_back_slash, blade_of_darkness, soul_harvest, vile_plan_cancel])
tbs_blade_soul = Combo([turn_back_slash, blade_of_darkness, soul_harvest])
violation_combo = Combo([violation, violation_2])
grim_reaper_combo = Combo([grim_reaper_judgement_cheat1, grim_reaper_judgement_cheat2, vile_plan])
grim_reaper = Combo([grim_reaper_judgement_cheat1, grim_reaper_judgement_cheat2])
soul_harvest_vile_plan_combo = Combo([soul_harvest, vile_plan_cancel])

ignition_hellfire_combo = Combo([shadow_ignition, shadow_hellfire])
hellfire_tendrils_combo = Combo([shadow_hellfire_hotbar, dark_tendrils])
hellfire_engulfing_combo = Combo([shadow_hellfire_hotbar, engulfing_shadow])
calamity_combo1 = Combo([bloody_calamity, shadow_ignition])
calamity_combo2 = Combo([bloody_calamity, engulfing_shadow])

def crit_buff_active():
    buffs = wincap.get_buffs()
    if e_buff.ready(buffs):
        return True
    else:
        x, y = crit_buff.ready(buffs, count=True)
        if x and y >= 2:
            return True
    return False

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

def target_dp_debuffed():
    debuffs = wincap.get_debuffs()
    x = dp_debuff.ready(debuffs)
    if x:
        return True
    return False

def calamity(context, direction, state):
    if direction == 'left':
        iframe_left.cast(context)
    elif direction == 'right':
        iframe_right.cast(context)
    
    if calamity_combo1.ready():
        if calamity_combo1.cast(context):
            return 1, time.time()
    elif calamity_combo2.ready():
        if calamity_combo2.cast(context):
            return 1, time.time()
    
    return state, time.time()

# State 0 = Awakening
# State 1 = Pre-Awak
# State 2 = Unsure
def pve(context, last_cast, state):
    # Unsure what state we are in
    if time.time() - last_cast <= 1.5 and state == 2:
        if soul_harvest_vile_plan_combo.ready():
            if soul_harvest_vile_plan_combo.cast(context):
                return 0
            return 2
        elif soul_harvest.ready():
            if soul_harvest.cast(context):
                return 0
            return 2
        elif shadow_ignition.ready():
            if shadow_ignition.cast(context):
                return 1
            return 2
        elif shadow_hellfire_hotbar.ready():
            if shadow_hellfire_hotbar.cast(context):
                return 1
            return 2
    elif state == 1:
        if soul_harvest_vile_plan_combo.ready():
            if soul_harvest_vile_plan_combo.cast(context):
                return 0
            return 2
        elif soul_harvest.ready():
            if soul_harvest.cast(context):
                return 0
            return 2
        elif shadow_ignition.ready():
            shadow_ignition.cast(context)
            return 1
        elif shadow_hellfire.ready():
            shadow_hellfire.cast(context)
            return 1
        elif soul_reaper.ready():
            if soul_reaper.cast(context):
                return 0
            return 2
        elif dark_tendrils.ready():
            dark_tendrils.cast(context)
            return 1
        elif engulfing_shadow.ready():
            engulfing_shadow.cast(context)
            return 1
        elif wings_of_the_crow.ready():
            if wings_of_the_crow.cast(context):
                return 0
            return 2
    elif tbs_blade_soul_vile.ready():
        tbs_blade_soul_vile.cast(context)
    elif tbs_blade_soul.ready():
        tbs_blade_soul.cast(context)
    elif tbs_blade.ready():
        tbs_blade.cast(context)
    elif violation_combo.ready():
        violation_combo.cast(context)
    elif not crit_buff_active() and midnight_stinger.ready():
        if midnight_stinger.cast(context):
            return 1
        return 2
    elif swirling_darkness.ready():
        swirling_darkness.cast(context)
    elif grim_reaper_combo.ready():
        grim_reaper_combo.cast(context)
    elif grim_reaper.ready():
        grim_reaper.cast(context)
    elif soul_harvest_vile_plan_combo.ready():
        soul_harvest_vile_plan_combo.cast(context)
    elif soul_harvest.ready():
        soul_harvest.cast(context)
    elif ignition_hellfire_combo.ready():
        if ignition_hellfire_combo.cast(context):
            return 1
        return 2
    elif hellfire_tendrils_combo.ready():
        if hellfire_tendrils_combo.cast(context):
            return 1
        return 2
    elif hellfire_engulfing_combo.ready():
        if hellfire_engulfing_combo.cast(context):
            return 1
        return 2
    elif soul_reaper.ready():
        soul_reaper.cast(context)
    
    return state