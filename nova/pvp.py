from .spells import *


def bomb():
    if bomba_combo.ready():
        if bomba_combo.cast():
            return

def combo(last_cast, combo_state):
    accel_state = get_accel_state()

    # Initial debuff or stun CC with lunge
    if combo_state == 0:
        if swooping_lunge_remise_accel_combo.ready() and accel_state != NOT_ACCEL:
            if swooping_lunge_remise_accel_combo.cast():
                return time.time(), 1
        elif remise_accel_combo.ready() and accel_state == IN_ACCEL:
            if remise_accel_combo.cast():
                return time.time(), 1
        elif remise_combo.ready() and accel_state != IN_ACCEL:
            if remise_combo.cast():
                return time.time(), 1
        elif swooping_remise_accel_combo.ready() and accel_state != NOT_ACCEL:
            if swooping_remise_accel_combo.cast():
                return time.time(), 1
        
        # FREEZE RESET
    
    # Re-CC Phase
    elif combo_state == 1:
        if cc_combo2.ready() and accel_state == IN_ACCEL:
            if cc_combo2.cast():
                return time.time(), 2
        elif starfall.ready():
            if starfall.cast():
                return time.time(), 2
        elif comet_180.ready() and time.time() - last_cast < 1:
            if comet_180.cast():
                return time.time(), 2
        elif starcall_accel.ready() and accel_state == IN_ACCEL:
            if starcall_accel.cast():
                return time.time(), 2
        elif riposte.ready() and last_cast < 1:
            if riposte.cast():
                return time.time(), 2
        
        # FREEZE, RESET
    
    # DPS Phase
    elif combo_state == 2:
        if riposte_swooping_combo.ready() and accel_state != NOT_ACCEL:
            if riposte_swooping_combo.cast():
                return time.time(), 3
        elif riposte_slicing_combo.ready() and time.time() - last_cast < 1:
            if riposte_slicing_combo.cast():
                return time.time(), 3
        elif starfall_lunge_combo.ready():
            if starfall_lunge_combo.cast():
                return time.time(), 3
        elif riposte_starfall_combo.ready() and time.time() - last_cast < 1:
            if riposte_starfall_combo.cast():
                return time.time(), 3
        elif comet_180.ready() and time.time() - last_cast < 1:
            if comet_180.cast():
                return time.time(), 3
        elif riposte.ready() and time.time() - last_cast < 1:
            if riposte.cast():
                return time.time(), 3
        elif downsmash_combo.ready():
            if downsmash_combo.cast():
                # End sequence. look for freeze
                return time.time(), 4
        elif quoratum_earth_pvp.ready():
            if quoratum_earth_pvp.cast():
                if quoratum_awak_swap.cast():
                    if lunge.ready() and lunge.cast():
                        return time.time(), 4
                return time.time(), 4
    
    elif combo_state == 3:
        if riposte_slicing_quoratum_combo.ready() and time.time - last_cast < 1:
            if riposte_slicing_quoratum_combo.cast():
                return time.time(), 4
        elif lunge_starfall_quoratum_combo.ready():
            if lunge_starfall_quoratum_combo.cast():
                return time.time(), 4
        elif comet_180_quoratum_combo.ready():
            if comet_180_quoratum_combo.cast():
                return time.time(), 4
        elif lunge_starfall_starcall_combo.ready():
            if lunge_starfall_starcall_combo.cast():
                return time.time(), 4
        elif remise_accel_quoratum_combo.ready() and accel_state == IN_ACCEL:
            if remise_accel_quoratum_combo.cast():
                return time.time(), 4
        elif remise_quoratum_combo.ready() and accel_state != IN_ACCEL:
            if remise_quoratum_combo.cast():
                return time.time(), 4
        elif downsmash_combo.ready():
            if downsmash_combo.cast():
                # End sequence. look for freeze
                return time.time(), 4
        elif slicing_ring.ready():
            if slicing_ring.cast():
                if quoratum_earth_pvp.ready() and quoratum_earth_pvp.cast():
                    quoratum_awak_swap.cast()
                return time.time(), 4
        elif quoratum_earth_pvp.ready():
            print("why am I here")
            if quoratum_earth_pvp.cast():
                if quoratum_awak_swap.cast():
                    if lunge.ready() and lunge.cast():
                        return time.time(), 4
                return time.time(), 4
        # elif frozen_ring_accel.ready() and accel_state == IN_ACCEL:
        #     if frozen_ring_accel.cast():
        #         return time.time(), 4
        # elif frozen_ring.ready():
        #     if frozen_ring.cast(hotbar=True):
        #         return time.time(), 4
                