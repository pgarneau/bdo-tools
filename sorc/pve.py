# from spells import *
from .spells import *
import time

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

def pve(context, last_cast, state):
    if prime_claws_of_darkness.ready():
        prime_claws_of_darkness.cast(context)
    
    return state
# State 0 = Awakening
# State 1 = Pre-Awak
# State 2 = Unsure
def pvez(context, last_cast, state):
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
        elif shadow_hellfire.ready():
            if shadow_hellfire.cast(context):
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

# def grim():
#     if grim_reaper_judgement.ready():
#         grim_reaper_judgement.cast()