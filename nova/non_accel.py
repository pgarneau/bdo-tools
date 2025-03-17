from .spells import *

def non_accel(last_cast):
    if combust.ready():
        if combust.cast():
            return
    elif riposte.ready() and time.time() - last_cast < 1:
        if riposte.cast():
            return time.time()
    elif frozen_ring.ready():
        if frozen_ring.cast(hotbar=True):
            return time.time()
    elif slicing_ring.ready() and time.time() - last_cast <= 1:
        if slicing_ring.cast():
            return time.time()
    elif remise_combo.ready():
        if remise_combo.cast():
            return time.time()
    elif starfall_lunge_combo.ready():
        if starfall_lunge_combo.cast():
            return time.time()
    elif brutal_ring.ready():
        if brutal_ring.cast(hotbar=True):
            return time.time()
    elif fleche.ready():
        if fleche.cast():
            return time.time()
    remise.cast()