import os
import time
from common.windowcapture import wincap
from common.spell import *
from common.combo import Combo
from common.bind import Bind, hold_bind, hold_bind_release_early
from common.vision import Vision

from .utils import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# buffs
cast_speed_buff = Spell(Vision('cast_speed', 0.98), None)
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
dark_tendrils_hotbar = Spell(Vision('dark_tendrils'), Bind('2', None, hotbar=True), 1.4, 8, get_attack_speed)
engulfing_shadow = Spell(Vision('engulfing_shadow'), Bind('shift+z', None), 0.65, 7, get_attack_speed)
shadow_ignition = Spell(Vision('shadow_ignition'), Bind('shift+x', None), 0.5, 8, get_attack_speed)
shadow_hellfire_hotbar = Spell(Vision('shadow_hellfire'), Bind('1', None, hotbar=True), 0.6, 4, get_attack_speed)

# Succession
prime_claws_of_darkness_cancel = Spell(Vision('prime_claws_of_darkness'), Bind('w', 'left'), 0.25, 5, get_attack_speed)
prime_claws_of_darkness = Spell(Vision('prime_claws_of_darkness'), Bind('w', 'left', hold_bind), 1.2, 5, get_attack_speed)
prime_abyssal_flame = Spell(Vision('prime_abyssal_flame'), Bind(None, 'left+right'), 0.4, 7, get_attack_speed)
prime_bloody_calamity = Spell(Vision('prime_bloody_calamity'), Bind('space', None, hold_bind), 0.2, 16, get_attack_speed)
# prime_bloody_calamity_cheat = NoCooldownSpell('prime_bloody_calamity', Bind('space', 'left', calamity_handler()), 0.25, get_attack_speed)
prime_bloody_calamity_cheat = NoCooldownSpell('prime_bloody_calamity', Bind('space', 'left', hold_bind_release_early), 0.25, get_attack_speed)
prime_crow_flare = Spell(Vision('prime_crow_flare'), Bind('e', None), 0.45, 2, get_attack_speed)
prime_dark_flame = Spell(Vision('prime_dark_flame'), Bind('s', 'left'), 0.55, 8, get_attack_speed)
prime_darkness_released = Spell(Vision('prime_darkness_released'), Bind('w+f', None), 0.35, 6, get_attack_speed)
# prime_midnight_stinger = Spell(Vision('prime_midnight_stinger'), Bind('shift', 'left', midnight_handler()), 0.2, 2, get_attack_speed)
prime_midnight_stinger = Spell(Vision('prime_midnight_stinger'), Bind('shift', 'left'), 0.2, 2, get_attack_speed)
prime_shadow_eruption = Spell(Vision('prime_shadow_eruption'), Bind('shift+f', None), 0.25, 7, get_attack_speed)
prime_turn_back_slash = Spell(Vision('prime_turn_back_slash'), Bind('s+c', None), 0.3, 5, get_attack_speed)
ultimate_dark_flame = Spell(Vision('ultimate_dark_flame'), Bind('s', 'left'), 1, 8, get_attack_speed)
ultimate_shadow_eruption = Spell(Vision('ultimate_shadow_eruption'), Bind('w', 'left'), 0.45, 9, get_attack_speed)
# prime_imminent_doom = HoldAndSpamSpell(Vision('imminent_doom'), Bind('shift+e', None, imminent_handler()), Bind(None, 'left+right'), 0.2, 14, get_attack_speed)
prime_dream_of_doom = Spell(Vision('prime_dream_of_doom'), Bind('shift+e', None), 0, 14, get_attack_speed)
# prime_dream_of_doom_cheat = NoCooldownSpell('prime_dream_of_doom', Bind(None, 'left', imminent_handler()), 0.15, get_attack_speed)
prime_dream_of_doom_cheat = NoCooldownSpell('prime_dream_of_doom', Bind(None, 'left'), 0.15, get_attack_speed)
# prime_violation = Spell(Vision('prime_violation'), Bind('w+c', None, violation_handler()), 0.7, 6, get_attack_speed)
# prime_violation_claw = Spell(Vision('prime_violation'), Bind('c', None, violation_handler()), 0.7, 6, get_attack_speed)
prime_violation = Spell(Vision('prime_violation'), Bind('w+c', None), 0.7, 6, get_attack_speed)
prime_violation_claw = Spell(Vision('prime_violation'), Bind('c', None), 0.7, 6, get_attack_speed)
shadow_hellfire = Spell(Vision('shadow_hellfire'), Bind(None, 'right', hold_bind_release_early), 0.6, 4, get_attack_speed)
dark_tendrils = Spell(Vision('dark_tendrils'), Bind('s+e', None), 1.45, 8, get_attack_speed)
prime_black_wave = HoldAndSpamSpell(Vision('prime_black_wave'), Bind('s', None, hold_bind), Bind(None, 'right+left'), 1.7, 8, get_attack_speed)

iframe_right = Iframe(Bind('shift+d', None), 0.6, get_attack_speed)
iframe_left = Iframe(Bind('shift+a', None), 0.6, get_attack_speed)
iframe_forward_180_mmb = SkillLogSpell(Vision('night_crow'), Bind(None, 'middle', camera_180()), 0.2, get_attack_speed)
iframe_forward_180_button4 = SkillLogSpell(Vision('night_crow'), Bind(None, 'x1', camera_180_1080p_1200dpi()), 0.2, get_attack_speed)


link_spells(prime_violation, prime_violation_claw)
link_spells(prime_claws_of_darkness_cancel, prime_claws_of_darkness)
link_spells(dark_tendrils, dark_tendrils_hotbar)
link_spells(shadow_hellfire, shadow_hellfire_hotbar)

# Combos
# Generic Combos
claws_vio_combo = Combo([prime_claws_of_darkness_cancel, prime_violation_claw])
prime_imminent_doom = Combo([prime_dream_of_doom, prime_dream_of_doom_cheat])

# TBS Combos
midnight_tbs = Combo([prime_midnight_stinger, prime_turn_back_slash])
ignition_tbs = Combo([shadow_ignition, prime_turn_back_slash])
engulfing_tbs = Combo([engulfing_shadow, prime_turn_back_slash])
crow_tbs = Combo([prime_crow_flare, prime_turn_back_slash])
claw_eruption = Combo([prime_claws_of_darkness_cancel, ultimate_shadow_eruption])
prime_ultimate_eruption = Combo([prime_shadow_eruption, ultimate_shadow_eruption])

# Calamity Combos
calamity_combo = Combo([prime_bloody_calamity, prime_bloody_calamity_cheat])
midnight_calamity = Combo([prime_midnight_stinger, prime_bloody_calamity, prime_bloody_calamity_cheat])
violation_calamity = Combo([prime_violation, prime_bloody_calamity, prime_bloody_calamity_cheat])
eruption_calamity = Combo([prime_shadow_eruption, prime_bloody_calamity, prime_bloody_calamity_cheat])
crow_calamity = Combo([prime_crow_flare, prime_bloody_calamity, prime_bloody_calamity_cheat])

# Suc Combos
midnight_calamity_combo = Combo([prime_midnight_stinger, prime_bloody_calamity, prime_bloody_calamity_cheat])
imminent_midnight_combo = Combo([prime_imminent_doom, prime_midnight_stinger])
blackwave_eruption_combo = Combo([prime_black_wave, ultimate_shadow_eruption])
midnight_claw_eruption_combo = Combo([prime_midnight_stinger, ultimate_shadow_eruption])
full_claw_eruption_combo = Combo([prime_claws_of_darkness, ultimate_shadow_eruption])

# Prime Shadow Eruption Combos
midnight_double_eruption = Combo([prime_midnight_stinger, prime_shadow_eruption, ultimate_shadow_eruption])
midnight_eruption = Combo([prime_midnight_stinger, prime_shadow_eruption])

def crit_buff_active():
    buffs = wincap.get_buffs()
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

# State = [0, 0, 0, 0, 0, 0]
# State[0] = Cancellable State
# State[1] = Hellfire Useable
# State[2] = Calamity Useable
# State[3] = TBS Useable
# State[4] = Post TBS State
# State[5] = Post Darkness Released
def pve(context, state):
    if state[0]:
        if not state[5] and not target_dp_debuffed() and prime_violation.ready():
            if prime_violation.cast(context):
                return [False, False, True, False, False, False]
        elif prime_midnight_stinger.ready():
            if prime_midnight_stinger.cast(context):
                return [False, True, True, True, False, False]
        elif prime_bloody_calamity.ready() and not state[5] and prime_violation.ready():
            if prime_violation.cast(context):
                return [False, False, True, False, False, False]
        elif prime_bloody_calamity.ready() and prime_crow_flare.ready():
            if prime_crow_flare.cast(context):
                return [False, False, True, True, False, False]
        elif prime_turn_back_slash.ready() and shadow_ignition.ready():
            if shadow_ignition.cast(context):
                return [False, False, False, True, False, False]
        elif prime_turn_back_slash.ready() and engulfing_shadow.ready():
            if engulfing_shadow.cast(context):
                return [False, True, False, True, False, False]
        elif shadow_ignition.ready():
            if shadow_ignition.cast(context):
                return [False, False, False, True, False, False]
        elif engulfing_shadow.ready():
            if engulfing_shadow.cast(context):
                return [False, True, False, True, False, False]
        elif state[1] and shadow_hellfire.ready():
            if shadow_hellfire.cast(context):
                return [False, False, False, False, False, False]
        elif not state[5] and prime_violation.ready():
            if prime_violation.cast(context):
                return [False, False, True, False, False, False]
        elif prime_crow_flare.ready():
            if prime_crow_flare.cast(context):
                return [False, False, True, True, False, False]

    # BUFFS AND DEBUFFS
    elif not cast_speed_active() and prime_claws_of_darkness_cancel.ready():
        if prime_claws_of_darkness_cancel.cast(context):
            return [True, False, False, False, False, False]
    elif not target_dp_debuffed() and claws_vio_combo.ready():
        if claws_vio_combo.cast(context):
            return [False, False, True, False, False, False]
    elif not crit_buff_active() and prime_midnight_stinger.ready():
        if prime_midnight_stinger.cast(context):
            return [False, True, True, True, False, False]
    
    # DPS
    # DoD cheat for cooldown
    elif prime_imminent_doom.ready() and time.time() - prime_dream_of_doom.shared_data.last_cast >= 14:
        if prime_imminent_doom.cast(context):
            return [True, True, False, False, False, False]
    
    # Calamity Combos
    elif state[2] and prime_bloody_calamity.ready():
        if calamity_combo.cast(context):
            return [True, False, False, False, False, False]
    elif midnight_calamity_combo.ready():
        if midnight_calamity_combo.cast(context):
            return [True, False, False, False, False, False]
    elif eruption_calamity.ready():
        if eruption_calamity.cast(context):
            return [True, False, False, False, False, False]
    elif violation_calamity.ready():
        if violation_calamity.cast(context):
            return [True, False, False, False, False, False]
    elif crow_calamity.ready():
        if crow_calamity.cast(context):
            return [True, False, False, False, False, False]    
    
    # TBS Combos
    elif state[3] and prime_turn_back_slash.ready():
        if prime_turn_back_slash.cast(context):
            return [False, False, False, False, True, False]
    elif state[4] and prime_ultimate_eruption.ready():
        prime_ultimate_eruption.cast(context)
    elif state[4] and prime_abyssal_flame.ready():
        prime_abyssal_flame.cast(context)
    elif state[4] and prime_shadow_eruption.ready():
        prime_shadow_eruption.cast(context)
    elif state[4] and claw_eruption.ready():
        claw_eruption.cast(context)
    elif midnight_tbs.ready():
        if midnight_tbs.cast(context):
            return [False, False, False, False, True, False]
    elif ignition_tbs.ready():
        if ignition_tbs.cast(context):
            return [False, False, False, False, True, False]
    elif engulfing_tbs.ready():
        if engulfing_tbs.cast(context):
            return [False, False, False, False, True, False]
    elif crow_tbs.ready():
        if crow_tbs.cast(context):
            return [False, False, False, False, True, False]
    
    # Darkness Released Combos
    elif prime_darkness_released.ready():
        if prime_darkness_released.cast(context):
            return [True, False, False, False, False, True]
    
    # Shadow Eruption Combos
    elif midnight_double_eruption.ready():
        midnight_double_eruption.cast(context)
    elif midnight_eruption.ready():
        midnight_eruption.cast(context)

    # Ultimate Shadow Eruption
    elif midnight_claw_eruption_combo.ready():
        midnight_claw_eruption_combo.cast(context)
    elif blackwave_eruption_combo.ready():
        blackwave_eruption_combo.cast(context)
    elif full_claw_eruption_combo.ready():
        full_claw_eruption_combo.cast(context)
    
    # Generic
    elif prime_midnight_stinger.ready():
        if prime_midnight_stinger.cast(context):
            return [False, True, True, True, False, False]
    elif prime_black_wave.ready():
        if prime_black_wave.cast(context):
            return [True, False, False, False, False, False]
    elif prime_claws_of_darkness.ready():
        if prime_claws_of_darkness_cancel.cast(context):
            return [True, False, False, False, False, False]
    elif shadow_ignition.ready():
        if shadow_ignition.cast(context):
            return [False, False, False, True, False, False]
    elif engulfing_shadow.ready():
        if engulfing_shadow.cast(context):
            return [False, True, False, True, False, False]
    elif state[1] and shadow_hellfire.ready():
        shadow_hellfire.cast(context)
    elif dark_tendrils.ready():
        dark_tendrils.cast(context)
    elif prime_crow_flare.ready():
        if prime_crow_flare.cast(context):
            return [False, False, True, True, False, False]
    
    return [False, False, False, False, False, False]