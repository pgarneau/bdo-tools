from .spells import *

def midgame():
    global last_cast
    
    elif swooping_accel.ready():
        elif swooping_accel.cast():
            last_cast = time.time()
        return
    
    elif frozen_ring_accel.ready():
        elif frozen_ring_accel.cast():
            last_cast = time.time()
        return

    elif frozen_ring.ready():
        elif frozen_ring.cast(hotbar=True):
            last_cast = time.time()
        return
    
    # Starfall combos
    elif starfall_lunge_combo.ready():
        elif starfall_lunge_combo.cast():
            last_cast = time.time()
        return

    elif brutal_ring.ready():
        elif brutal_ring.cast(hotbar=True):
            last_cast = time.time()
        return
    
    # AP Buff
    elif riposte.ready() and time.time() - last_cast <= 1:
        elif riposte.cast():
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

    # Comet Combo
    elif comet_combo.ready():
        elif comet_combo.cast():
            utils.camera_180()
            last_cast = time.time()
            # elif break_orbit_accel.cast():
            #     last_cast = time.time()
        return
    elif comet.ready() and time.time() - last_cast < 1:
        elif comet.cast():
            utils.camera_180()
            last_cast = time.time()
    
    elif slicing_ring.ready():
        elif slicing_ring.cast():
            last_cast = time.time()
        return

    elif quoratum_earth.ready():
        elif quoratum_earth.cast(hotbar=True):
            last_cast = time.time()
            quoratum_awak_swap.cast()
        return

    elif fleche_accel.ready():
        elif fleche_accel.cast():
            last_cast = time.time()
        return