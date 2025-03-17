from .spells import *

def sa_rotation():
    if crouching_wolf_hotkey.ready():
        if crouching_wolf_hotkey.cast():
            return
    elif mass_destruction.ready():
        if mass_destruction.cast():
            return
    elif silent_step.ready():
        if silent_step.cast():
            return
    elif scissor_kick.ready():
        if scissor_kick.cast():
            return
    elif rage_hammer.ready():
        if rage_hammer.cast():
            return
    elif sky_rammer.ready():
        if twisted_sa.cast():
            return
    elif elbow_edge.ready():
        if elbow_edge.cast():
            return

def combo():
    if rising_opener.ready():
        rising_opener.cast()
    elif no_rising_opener.ready():
        no_rising_opener.cast()
    elif downsmash_finisher.ready():
        downsmash_finisher.cast()
    elif unbridled_wrath.ready():
        unbridled_wrath.cast()
    elif hurricane_kick.ready():
        hurricane_kick_rmb.cast()
