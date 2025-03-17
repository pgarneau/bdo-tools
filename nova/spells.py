import os
import time
from windowcapture import WindowCapture
from spell import Spell
from combo import Combo
from bind import Bind, hold_bind
from nova import utils

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their 
# own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# initialize the WindowCapture class
wincap = WindowCapture()

# constants
IN_ACCEL = 1
ACCEL_READY = 2
NOT_ACCEL = 3

# Custom Spell Behaviors
class StarcallAccelSpell(Spell):
   def cast(self):
      utils.camera_point_down()
      if super().cast():
          return True

class Comet180Spell(Spell):
    def cast(self):
        if super().cast():
            utils.camera_180()
            return True

def quoratum_pvp_cast():
    if Spell.cast(quoratum_earth_pvp, hotbar=True):
        return True

# Accel Management
accel_buff = Spell('accel_buff', None, wincap, 0.99)
accel = Spell('accel', Bind('e'), wincap, 0.98)
combust = Spell('combust', Bind('shift+e'), wincap)
cast_speed_buff = Spell('cast_speed', None, wincap, 0.98)

# Pre-Awak
quoratum_earth = Spell('quoratum_earth', Bind('3', None, 1.5), wincap)
quoratum_earth_pvp = Spell('quoratum_earth', Bind('1', None, 0.7), wincap)
quoratum_earth_pvp.cast = quoratum_pvp_cast
quoratum_awak_swap = Spell('quoratum_earth', Bind('w+c', None, 0.5, hold_bind), wincap)
queen_gambit = Spell('queen_gambit', Bind('3', None, 2.3), wincap)
queen_gambit_awak_swap = Spell('queen_gambit', Bind('w+c', None, 0.1), wincap)
grab = Spell('punishing_trap', Bind('w+e', None, 1.5), wincap)

# Non Accel
swooping = Spell('swooping', Bind('w', 'right', 0.5), wincap)
starcall = Spell('starcall', Bind('shift', 'left', 1.5), wincap)
comet = Spell('comet', Bind('w+f', None, 0.1), wincap)
comet_180 = Comet180Spell('comet', Bind('w+f', None, 0.1), wincap)
lunge = Spell('lunge', Bind('f', None , 0.1), wincap)
riposte = Spell('riposte', Bind('s+q'), wincap)
remise = Spell('remise', Bind('s', 'left', 1, hold_bind), wincap)
frozen_ring = Spell('frozen_ring', Bind('2', None, 1.6), wincap)
starfall = Spell('starfall', Bind('shift', 'right', 0.1), wincap)
brutal_ring = Spell('brutal_ring', Bind('1', None, 0.4), wincap)
brutal_ring_lmb = Spell('brutal_ring', Bind(None, 'left', 0.3), wincap)
slicing_ring = Spell('slicing_ring', Bind('q', None, 0.8, hold_bind), wincap)
fleche = Spell('fleche', Bind('s+f'), wincap)

# Accel
swooping_accel = Spell('swooping_accel', Bind('w+q', None, 0.1), wincap)
# starcall_accel = StarcallAccelSpell('starcall_accel', Bind('shift', 'left', 0.5), wincap)
starcall_accel = Spell('starcall_accel', Bind('shift', 'left', 0.5), wincap)
remise_accel = Spell('remise_accel', Bind('s', 'left', 0.9, hold_bind), wincap)
frozen_ring_accel = Spell('frozen_ring_accel', Bind('shift+q', None, 1.2), wincap)
fleche_accel = Spell('fleche_accel', Bind('s+f', None, 1.4, hold_bind), wincap)
fleche_accel_short = Spell('fleche_accel', Bind('s+f', None, 0.4), wincap)
break_orbit_accel = Spell('break_orbit_accel', Bind('shift+s', None, 0.2, hold_bind), wincap, 0.94)

# Combos
# Starfall
starfall_full_combo = Combo([lunge, remise_accel, starfall])
starfall_lunge_combo = Combo([lunge, starfall])
starfall_remise_combo = Combo([remise_accel, starfall])

# Remise
remise_combo = Combo([lunge, remise])
remise_accel_combo = Combo([lunge, remise_accel])

# Comet
comet_combo = Combo([lunge, comet])
comet_180_combo = Combo([lunge, comet_180])

# Starcall
starcall_combo = Combo([break_orbit_accel, starcall_accel])

# Frozen Ring
frozen_ring_accel_combo = Combo([frozen_ring_accel, brutal_ring_lmb])
frozen_ring_combo = Combo([frozen_ring, brutal_ring_lmb])

# Fleche Cancel
fleche_lunge_combo = Combo([fleche_accel_short, lunge])

# PVP
bomba_combo = Combo([starcall_accel, swooping_accel, lunge, starfall, remise_accel, riposte, slicing_ring, frozen_ring_accel])
downsmash_combo = Combo([lunge, quoratum_earth_pvp, quoratum_awak_swap])
# Phase 0 Combos
remise_combo = Combo([lunge, remise])
remise_accel_combo = Combo([lunge, remise_accel])
lunge_slicing_combo = Combo([lunge, slicing_ring])
lunge_starcall_combo = Combo([lunge, starcall])
lunge_frozen_ring_combo = Combo([lunge, frozen_ring])
lunge_frozen_ring_accel_combo = Combo([lunge, frozen_ring_accel])
swooping_remise_accel_combo = Combo([swooping_accel, remise_accel])
swooping_lunge_remise_accel_combo = Combo([swooping_accel, lunge, remise_accel])
# CC Combos
cc_combo1 = Combo([starfall, riposte])
cc_combo2 = Combo([comet_180, starcall_accel])
# Finisher Combos
riposte_swooping_combo = Combo([riposte, swooping_accel])
riposte_slicing_combo = Combo([riposte, slicing_ring])
riposte_slicing_quoratum_combo = Combo([riposte, slicing_ring, quoratum_earth_pvp, quoratum_awak_swap])
riposte_starfall_combo = Combo([riposte, starfall])
comet_180_quoratum_combo = Combo([lunge, comet_180, quoratum_earth_pvp, quoratum_awak_swap])
lunge_starfall_quoratum_combo = Combo([lunge, starfall, quoratum_earth_pvp, quoratum_awak_swap])
lunge_starfall_starcall_combo = Combo([lunge, starfall, starcall])
remise_accel_quoratum_combo = Combo([lunge, remise_accel, quoratum_earth_pvp, quoratum_awak_swap])
remise_quoratum_combo = Combo([lunge, remise, quoratum_earth_pvp, quoratum_awak_swap])


def init_spells():
   # Pre-Awak
   quoratum_earth.ready()
   quoratum_earth_pvp.ready()
   quoratum_awak_swap.ready()
   queen_gambit.ready()
   queen_gambit_awak_swap.ready()
   grab.ready()

   # Non Accel
   swooping.ready()
   starcall.ready()
   comet.ready()
   comet_180.ready()
   lunge.ready()
   riposte.ready()
   remise.ready()
   frozen_ring.ready()
   starfall.ready()
   brutal_ring.ready()
   brutal_ring_lmb.ready()
   slicing_ring.ready()
   fleche.ready()

   # Accel
   swooping_accel.ready()
   starcall_accel.ready()
   remise_accel.ready()
   frozen_ring_accel.ready()
   fleche_accel.ready()
   break_orbit_accel.ready()
   fleche_accel_short.ready()

   print("Spells Initiated")

   return True

def get_accel_state():
    buffs = wincap.get_buffs()
    if accel_buff.ready(buffs):
        return IN_ACCEL
    else:
        if accel.ready(wincap.get_accel()):
            return ACCEL_READY
        return NOT_ACCEL

def cast_speed_active():
    buffs = wincap.get_buffs()
    if cast_speed_buff.ready(buffs):
        return True
    return False
