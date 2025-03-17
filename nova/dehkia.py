from .spells import *

def dehkia():
    global last_cast
    
    # Starfall combos
    elif starfall_full_combo.ready():
        elif starfall_full_combo.cast():
            last_cast = time.time()
        return
    elif starfall_lunge_combo.ready():
        elif starfall_lunge_combo.cast():
            last_cast = time.time()
        return
    elif starfall_remise_combo.ready():
        elif starfall_remise_combo.cast():
            last_cast = time.time()
        return
    
    elif swooping_accel.ready():
        elif swooping_accel.cast():
            last_cast = time.time()
        return

    # Remise
    elif remise_accel_combo.ready():
        elif remise_accel_combo.cast():
            last_cast = time.time()
        return
    elif remise_accel.ready():
        elif remise_accel.cast():
            last_cast = time.time()
        return
    
    elif starcall_accel.ready():
        # break_orbit_accel.cast()
        elif starcall_accel.cast():
            last_cast = time.time()
        return

    # AP Buff
    elif riposte.ready() and time.time() - last_cast <= 1:
        elif riposte.cast():
            last_cast = time.time()
        return

    # Comet Combo
    elif comet_combo.ready():
        elif comet_combo.cast():
            break_orbit_accel.cast()
            last_cast = time.time()
        return
    elif comet.ready() and time.time() - last_cast < 1:
        elif comet.cast():
            break_orbit_accel.cast()
            last_cast = time.time()
        return
    
    elif frozen_ring_accel_combo.ready():
        elif frozen_ring_accel_combo.cast():
            last_cast = time.time()
        return
    elif frozen_ring_accel.ready():
        elif frozen_ring_accel.cast():
            last_cast = time.time()
        return

    elif frozen_ring_combo.ready():
        elif frozen_ring_combo.cast():
            last_cast = time.time()
        return
    elif frozen_ring.ready():
        elif frozen_ring.cast(hotbar=True):
            last_cast = time.time()
        return

    elif slicing_ring.ready():
        elif slicing_ring.cast():
            last_cast = time.time()
        return

    elif fleche_accel.ready():
        elif fleche_accel.cast():
            last_cast = time.time()
        return
    
    elif quoratum_earth.ready():
        elif quoratum_earth.cast(hotbar=True):
            last_cast = time.time()
            quoratum_awak_swap.cast()
        return
