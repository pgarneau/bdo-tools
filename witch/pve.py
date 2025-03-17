from .spells import *

# Debuff target (Earth Arrow or Earthquake Destruction (more than 3 healthbars?))
# Voltaic
# MMA
# Frigid

def pve(last_cast, last_element):
    if not target_dp_debuffed() and earth_arrow.ready():
        if earth_arrow.cast():
            return time.time(), "earth"
    elif voltaic_pulse.ready():
        if voltaic_pulse.cast():
            return time.time(), "lightning"
    elif not ap_buff_active() and equilibrium_break.ready():
        if equilibrium_break.cast():
            return time.time(), "earth"
    elif mma.ready() and time.time() - last_cast <= 0.7 and last_element == "fire":
        if mma.cast():
            return time.time(), None
    elif freeze_mma.ready():
        if freeze_mma.cast():
            return time.time(), None
    elif lightning_mma.ready():
        if lightning_mma.cast():
            return time.time(), None
    elif mma.ready() and time.time() - last_cast <= 0.7:
        if mma.cast():
            return time.time(), None
    elif frigid_fog_control.ready():
        if frigid_fog_control.cast():
            return time.time(), "ice"
    elif lightning_combo.ready() and not voltaic_pulse.ready_in(1):
        if lightning_combo.cast():
            return time.time(), "lightning"
    elif meteor_shower_focus.ready():
        if meteor_shower_focus.cast():
            return time.time(), "fire"
    elif equilibrium_break.ready():
        if equilibrium_break.cast():
            return time.time(), "earth"
    elif fireball_explosion_spread.ready():
        if fireball_explosion_spread.cast():
            return time.time(), "fire"
    elif earthquake_destruction.ready():
        if earthquake_destruction.cast():
            return time.time(), "earth"
    elif blizzard_domain.ready():
        if blizzard_domain.cast():
            return time.time(), "ice"
    elif voltaic_discharge_focus.ready():
        if voltaic_discharge_focus.cast():
            return time.time(), "lightning"
    elif fireball.ready():
        if fireball.cast():
            return time.time(), "fire"
    elif earthen_eruption.ready():
        if earthen_eruption.cast():
            return time.time(), "earth"
    
    return None, None