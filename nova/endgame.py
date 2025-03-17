from .spells import *

def endgame_with_opener(last_cast):
    # Cast Speed for low BSR spots
    if not cast_speed_active() and fleche_lunge_combo.ready():
        if fleche_lunge_combo.cast():
            return time.time()
    # Starfall combos
    elif starfall_full_combo.ready():
        if starfall_full_combo.cast():
            return time.time()
    elif starfall_lunge_combo.ready():
        if starfall_lunge_combo.cast():
            return time.time()
    elif starfall_remise_combo.ready():
        if starfall_remise_combo.cast():
            return time.time()
    elif swooping_accel.ready():
        if swooping_accel.cast():
            return time.time()
    elif remise_accel_combo.ready():
        if remise_accel_combo.cast():
            return time.time()
    elif remise_accel.ready():
        if remise_accel.cast():
            return time.time()
    elif frozen_ring_accel.ready():
        if frozen_ring_accel.cast():
            return time.time()
    elif lunge.ready():
        if lunge.cast():
            return time.time()
    elif riposte.ready() and time.time() - last_cast < 1:
        if riposte.cast():
            return time.time()
    elif brutal_ring.ready():
        if brutal_ring.cast(hotbar=True):
            return time.time()
    elif slicing_ring.ready():
        if slicing_ring.cast():
            return time.time()
    elif frozen_ring.ready():
        if frozen_ring.cast(hotbar=True):
            return time.time()
    elif fleche_accel.ready():
        if fleche_accel.cast():
            return time.time()
    elif quoratum_earth.ready():
        if quoratum_earth.cast():
            quoratum_awak_swap.cast()
            return time.time()
    return

def endgame_no_opener(last_cast):
    # Cast Speed for low BSR spots
    if not cast_speed_active() and fleche_lunge_combo.ready():
        if fleche_lunge_combo.cast():
            return time.time()
    # Starfall combos
    elif starfall_full_combo.ready():
        if starfall_full_combo.cast():
            return time.time()
    elif starfall_lunge_combo.ready():
        if starfall_lunge_combo.cast():
            return time.time()
    elif starfall_remise_combo.ready():
        if starfall_remise_combo.cast():
            return time.time()
    elif swooping_accel.ready():
        if swooping_accel.cast():
            return time.time()
    elif remise_accel_combo.ready():
        if remise_accel_combo.cast():
            return time.time()
    elif remise_accel.ready():
        if remise_accel.cast():
            return time.time()
    elif starcall_accel.ready():
        if starcall_accel.cast():
            return time.time()
    # Comet Combo
    # elif comet_180_combo.ready():
    #     if comet_180_combo.cast():
    #         return time.time()
    # elif comet_180.ready() and time.time() - last_cast < 1:
    #     if comet_180.cast():
    #         return time.time()
    elif frozen_ring_accel.ready():
        if frozen_ring_accel.cast():
            return time.time()
    elif riposte.ready() and time.time() - last_cast < 1:
        if riposte.cast():
            return time.time()
    elif brutal_ring.ready():
        if brutal_ring.cast(hotbar=True):
            return time.time()
    elif slicing_ring.ready():
        if slicing_ring.cast():
            return time.time()
    elif frozen_ring.ready():
        if frozen_ring.cast(hotbar=True):
            return time.time()
    elif fleche_accel.ready():
        if fleche_accel.cast():
            return time.time()
    elif quoratum_earth.ready():
        if quoratum_earth.cast():
            quoratum_awak_swap.cast()
            return time.time()
    return
