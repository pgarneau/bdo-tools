import os
import time
from common.windowcapture import wincap
from common.spell import Spell, NoCooldownSpell, link_spells, Iframe, HoldAndSpamSpell
from common.combo import Combo
from common.bind import Bind, hold_bind, hold_bind_release_early
from common.vision import Vision

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# buffs
crit_buff = Spell(Vision('crit', 0.98), None)
ap_buff = Spell(Vision('ap', 0.98), None)
shai_buff = Spell(Vision('shai_speed', 0.98), None)
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

# Pre-awak
dark_tendrils_hotbar = Spell(Vision('dark_tendrils'), Bind('2', None, hotbar=True), 1.4, 11, get_attack_speed)
engulfing_shadow = Spell(Vision('engulfing_shadow'), Bind('shift+z', None), 0.65, 7, get_attack_speed)
shadow_ignition = Spell(Vision('shadow_ignition'), Bind('shift+x', None), 0.5, 10, get_attack_speed)
shadow_hellfire_hotbar = Spell(Vision('shadow_hellfire'), Bind('1', None, hotbar=True), 0.6, 4, get_attack_speed)

# Succession
prime_claws_of_darkness_cancel = Spell(Vision('prime_claws_of_darkness'), Bind('w', 'left'), 0.2, 5, get_attack_speed)
prime_claws_of_darkness = Spell(Vision('prime_claws_of_darkness'), Bind('w', 'left'), 1.15, 5, get_attack_speed)
prime_abyssal_flame = Spell(Vision('prime_abyssal_flame'), Bind(None, 'left+right'), 0.4, 7, get_attack_speed)
prime_bloody_calamity = Spell(Vision('prime_bloody_calamity'), Bind('space', None, hold_bind), 0.1, 16, get_attack_speed)
prime_bloody_calamity_cheat = NoCooldownSpell('prime_bloody_calamity', Bind('space', 'left', hold_bind_release_early), 0.55, get_attack_speed)
prime_crow_flare = Spell(Vision('prime_crow_flare'), Bind('e', None), 0.45, 2, get_attack_speed)
prime_dark_flame = Spell(Vision('prime_dark_flame'), Bind('s', 'left'), 0.55, 6, get_attack_speed)
prime_darkness_released = Spell(Vision('prime_darkness_released'), Bind('w+f', None), 0.35, 6, get_attack_speed)
prime_midnight_stinger = Spell(Vision('prime_midnight_stinger'), Bind('shift', 'left'), 0.2, 2, get_attack_speed)
prime_shadow_eruption = Spell(Vision('prime_shadow_eruption'), Bind('shift+f', None), 0.45, 7, get_attack_speed)
prime_turn_back_slash = Spell(Vision('prime_turn_back_slash'), Bind('s+c', None), 0.25, 5, get_attack_speed)
ultimate_dark_flame = Spell(Vision('ultimate_dark_flame'), Bind('s', 'left'), 1, 9, get_attack_speed)
ultimate_shadow_eruption = Spell(Vision('ultimate_shadow_eruption'), Bind('w', 'left'), 0.45, 9, get_attack_speed)
prime_imminent_doom = HoldAndSpamSpell(Vision('imminent_doom'), Bind('shift+e', None), Bind(None, 'left'), 0.2, 14, get_attack_speed)
prime_violation = Spell(Vision('prime_violation'), Bind('w+c', None), 0.75, 6, get_attack_speed)
shadow_hellfire = Spell(Vision('shadow_hellfire'), Bind(None, 'right', hold_bind_release_early), 0.6, 4, get_attack_speed)
dark_tendrils = Spell(Vision('dark_tendrils'), Bind('s+e', None), 1.4, 11, get_attack_speed)
prime_black_wave = HoldAndSpamSpell(Vision('prime_black_wave'), Bind('s', None, hold_bind), Bind(None, 'right+left'), 1.7, 8, get_attack_speed)

iframe_right = Iframe(Bind('shift+d', None), 0.6, get_attack_speed)
iframe_left = Iframe(Bind('shift+a', None), 0.6, get_attack_speed)

link_spells(dark_tendrils, dark_tendrils_hotbar)
link_spells(shadow_hellfire, shadow_hellfire_hotbar)

# Combos
ignition_hellfire_combo = Combo([shadow_ignition, shadow_hellfire])
hellfire_tendrils_combo = Combo([shadow_hellfire_hotbar, dark_tendrils])
hellfire_engulfing_combo = Combo([shadow_hellfire_hotbar, engulfing_shadow])

# Suc Combos
midnight_calamity_ignition_combo = Combo([prime_midnight_stinger, prime_bloody_calamity, prime_bloody_calamity_cheat, shadow_ignition])
midnight_calamity_engulfing_combo = Combo([prime_midnight_stinger, prime_bloody_calamity, prime_bloody_calamity_cheat, engulfing_shadow])
claws_vio_combo = Combo([prime_claws_of_darkness_cancel, prime_violation])
imminent_midnight_combo = Combo([prime_imminent_doom, prime_midnight_stinger])
imminent_hellfire_combo = Combo([prime_imminent_doom, shadow_hellfire])
imminent_ignition_combo = Combo([prime_imminent_doom, shadow_ignition])
blackwave_eruption_combo = Combo([prime_black_wave, ultimate_shadow_eruption])
eruption_combo = Combo([prime_shadow_eruption, ultimate_shadow_eruption])
darkness_crow_tbs_abyssal_combo = Combo([prime_darkness_released, prime_crow_flare, prime_turn_back_slash, prime_abyssal_flame])
crow_tbs_abyssal_combo = Combo([prime_crow_flare, prime_turn_back_slash, prime_abyssal_flame])
crow_tbs_claw_eruption_combo = Combo([prime_crow_flare, prime_turn_back_slash, prime_claws_of_darkness_cancel, prime_shadow_eruption])
midnight_claw_eruption_combo = Combo([prime_midnight_stinger, prime_claws_of_darkness_cancel, prime_shadow_eruption])
full_claw_eruption_combo = Combo([prime_claws_of_darkness, ultimate_shadow_eruption])
darkness_midnight_combo = Combo([prime_darkness_released, prime_midnight_stinger])
darkness_ignition_combo = Combo([prime_darkness_released, shadow_ignition])
darkness_engulfing_combo = Combo([prime_darkness_released, engulfing_shadow])
eruption_midnight_combo = Combo([prime_shadow_eruption, prime_midnight_stinger])
eruption_ignition_combo = Combo([prime_shadow_eruption, shadow_ignition])
eruption_engulfing_combo = Combo([prime_shadow_eruption, engulfing_shadow])

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

def target_dp_debuffed():
    debuffs = wincap.get_debuffs()
    x = dp_debuff.ready(debuffs)
    if x:
        return True
    return False

def pve(context):
    if not target_dp_debuffed() and claws_vio_combo.ready():
        claws_vio_combo.cast(context)
    elif not crit_buff_active() and prime_midnight_stinger.ready():
        prime_midnight_stinger.cast(context)
    elif imminent_midnight_combo.ready():
        imminent_midnight_combo.cast(context)
    elif imminent_hellfire_combo.ready():
        imminent_hellfire_combo.cast(context)
    elif imminent_ignition_combo.ready():
        imminent_ignition_combo.cast(context)
    elif midnight_calamity_ignition_combo.ready():
        midnight_calamity_ignition_combo.cast(context)
    elif midnight_calamity_engulfing_combo.ready():
        midnight_calamity_engulfing_combo.cast(context)
    elif darkness_crow_tbs_abyssal_combo.ready():
        darkness_crow_tbs_abyssal_combo.cast(context)
    elif crow_tbs_abyssal_combo.ready():
        crow_tbs_abyssal_combo.cast(context)
    elif darkness_midnight_combo.ready():
        darkness_midnight_combo.cast(context)
    elif darkness_ignition_combo.ready():
        darkness_ignition_combo.cast(context)
    elif darkness_engulfing_combo.ready():
        darkness_engulfing_combo.cast(context)
    elif midnight_claw_eruption_combo.ready():
        midnight_claw_eruption_combo.cast(context)
    elif crow_tbs_claw_eruption_combo.ready():
        crow_tbs_claw_eruption_combo.cast(context)
    elif blackwave_eruption_combo.ready():
        blackwave_eruption_combo.cast(context)
    elif full_claw_eruption_combo.ready():
        full_claw_eruption_combo.cast(context)
    elif claws_vio_combo.ready():
        claws_vio_combo.cast(context)
    elif prime_black_wave.ready():
        prime_black_wave.cast(context)
    elif prime_claws_of_darkness.ready():
        prime_claws_of_darkness.cast(context)
    elif shadow_hellfire_hotbar.ready():
        shadow_hellfire_hotbar.cast(context)
    elif shadow_ignition.ready():
        shadow_ignition.cast(context)
    elif eruption_combo.ready():
        eruption_combo.cast(context)
    elif eruption_midnight_combo.ready():
        eruption_midnight_combo.cast(context)
    elif eruption_ignition_combo.ready():
        eruption_ignition_combo.cast(context)
    elif eruption_engulfing_combo.ready():
        eruption_engulfing_combo.cast(context)
    elif dark_tendrils.ready():
        dark_tendrils.cast(context)
    elif engulfing_shadow.ready():
        engulfing_shadow.cast(context)