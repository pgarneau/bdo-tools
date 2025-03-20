import os
import time
from common.windowcapture import wincap
from common.spell import Spell, NoCooldownSpell, SkillLogSpell
from common.combo import Combo
from common.bind import Bind, hold_bind, hold_bind_release_early
from common.vision import Vision
from .shards import Shards
from .tidal_burst import TidalBurst

# Change the working directory to the folder this script is in.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# buffs
crit_rate_buff = Spell(Vision('crit', 0.98), None)
attack_speed_buff = Spell(Vision('attack_speed', 0.98), None)
attack_cast_speed_buff = Spell(Vision('attack_cast_speed', 0.98), None)
dragonize_buff = Spell(Vision('dragonize_buff', 0.98), None)
ap_buff = Spell(Vision('ap', 0.98), None)

shard_count = Shards(Vision('no_shards', 0.9), None)

# Debuffs
dp_debuff = Spell(Vision('dp_debuff', 0.98), None)

def get_attack_speed():
    speed = 1
    buffs = wincap.get_buffs()
    if dragonize_buff.ready(buffs):
        speed = speed + 0.3
    else:
        if attack_speed_buff.ready(buffs):
            speed = speed + 0.2
    
    # Generic modifier to press keybinds faster than actual animations
    speed = speed + 0.3
    
    return speed

# Awak
#rapid 0.42 to tidal
#rapid 0.40-0.41 to tidal with 20% AS
# rapid + tidal -> crouching 1.24
# rapid + tidal -> crouching 1.08 with 30% AS
# tidalshort -> crouching 0.72 with 30% AS, 0.81 with 10%
#tidal full -> crouching 1.15, 1.01 with 20% AS
# tidal full -> rising dragon 1.23, 1.05 with 20% AS 
#tidal full -> wave orb 1.22, 0.99 with 20% AS
#crouching_wolf -> 0.46 -> 0.43 (10%)
#rising -> gushing  0.60, 0.54
#gushing -> waveorb 0.58 ,0.48
#gushing -> sea_burial 0.66, 0.57
#gushing -> earthsplitter 0.56, 0.48
#earthsplitter -> seaburial 0.69, 0.53
#earthsplitter -> crouching 0.62, 0.55
#wave_orb -> earthsplitter 0.36, 0.32
#wave_orb -> crouching 0.43, 0.4
rapid_stream = Spell(Vision('rapid_stream'), Bind('shift', 'left'), 0.6, 5, get_attack_speed)
rapid_stream_log = SkillLogSpell(Vision('rapid_stream', threshold=0.91), Bind('shift', 'left'), 0.6, 5, get_attack_speed)
tidal_burst_quick = TidalBurst(Vision('tidal_burst'), Bind('shift', 'right', hold_bind_release_early), 1.1, 3, get_attack_speed)
tidal_burst = TidalBurst(Vision('tidal_burst'), Bind('shift', 'right', hold_bind_release_early), 1.5, 3, get_attack_speed)

dragon_strike = Spell(Vision('dragon_strike'), Bind(None, 'right', hold_bind), 1.0, 6, get_attack_speed)
short_dragon_strike = Spell(Vision('dragon_strike'), Bind(None, 'right'), 0.5, 6, get_attack_speed)
earthsplitter = Spell(Vision('earthsplitter'), Bind('s', 'right'), 0.7, 6, get_attack_speed)
gushing_waters = Spell(Vision('gushing_waters'), Bind(None, 'left'), 0.55, 7, get_attack_speed)
gushing_waters_hotkey = Spell(Vision('gushing_waters'), Bind('3', None, hotbar=True), 0.55, 7, get_attack_speed)
rising_dragon = Spell(Vision('rising_dragon'), Bind('shift+q', None), 0.7, 8, get_attack_speed)
sea_burial = Spell(Vision('sea_burial'), Bind('w', 'right'), 1.15, 7, get_attack_speed)
wave_orb = Spell(Vision('wave_orb'), Bind(None, 'left+right', hold_bind_release_early), 0.5, 11, get_attack_speed)
dragonize = Spell(Vision('dragonize'), Bind('shift+e', None), 1.5, 180, get_attack_speed)
hurricane_sweep = Spell(Vision('hurricane_sweep'), Bind('f', None, hold_bind), 1.65, 6, get_attack_speed)
hurricane_sweep_kick = Spell(Vision('hurricane_sweep'), Bind('s+f', None, hold_bind_release_early), 0.5, 6, get_attack_speed)

# PreAwak
c_swap = NoCooldownSpell('c_swap', Bind('w+c', None, hold_bind), 0.6, get_attack_speed)
crouching_wolf = Spell(Vision('crouching_wolf'), Bind('space', None), 0.3, 5, get_attack_speed)
crouching_wolf_hotkey = Spell(Vision('crouching_wolf'), Bind('3', None, hotbar=True), 0.55, 5)
silent_step = Spell(Vision('silent_step'), Bind('shift+a', None), 0.75, 4)
scissor_kick = Spell(Vision('scissor_kick'), Bind('2', None, hotbar=True), 0.7, 6)
rage_hammer = Spell(Vision('rage_hammer'), Bind('shift+q', None), 1.5, 8)
mass_destruction = Spell(Vision('mass_destruction'), Bind('a', 'right', hold_bind), 1.2, 5)
twisted_collision_sa = Spell(Vision('twisted_collision'), Bind('q', 'left', hold_bind), 1.0, 5)
twisted_collision = Spell(Vision('twisted_collision'), Bind('q', None), 0.2, 5, get_attack_speed)
sky_rammer = Spell(Vision('sky_rammer'), Bind('f', None), 0.7, 12)
elbow_edge = Spell(Vision('elbow_edge'), Bind('shift', 'left', hold_bind), 0.7, 5)
hurricane_kick = Spell(Vision('hurricane_kick'), Bind('2', None, hotbar=True), 0.95, 9, get_attack_speed)
hurricane_kick_rmb = Spell(Vision('hurricane_kick'), Bind(None, 'right', hold_bind_release_early), 1.3, 9, get_attack_speed)
recoil_slam = Spell(Vision('recoil_slam'), Bind('w+c', None), 0.4, 3, get_attack_speed)
unbridled_wrath = Spell(Vision('unbridled_wrath'), Bind('shift+x', None), 1.0, 10, get_attack_speed)

# Combos
tidal_combo = Combo([rapid_stream, tidal_burst_quick])
tidal_crouching_combo = Combo([rapid_stream, tidal_burst_quick, crouching_wolf])
rising_gushing_combo = Combo([rising_dragon, gushing_waters])
rising_gushing_wave_combo = Combo([rising_dragon, gushing_waters, wave_orb])
rising_gushing_sea_combo = Combo([rising_dragon, gushing_waters, sea_burial])
earthsplitter_wave_combo = Combo([earthsplitter, wave_orb])
tidal_wave_combo = Combo([tidal_burst, wave_orb])
dragon_wave_combo = Combo([short_dragon_strike, wave_orb])
splitter_burial_combo = Combo([earthsplitter, sea_burial])
hurricane_c_swap = Combo([hurricane_kick, c_swap])
hurricane_wave_combo = Combo([hurricane_kick, wave_orb])
hurricane_sea_combo = Combo([hurricane_kick, sea_burial])

# PVP Combos
rising_opener = Combo([rising_dragon, short_dragon_strike, wave_orb, hurricane_sweep_kick])
no_rising_opener = Combo([short_dragon_strike, wave_orb, hurricane_sweep])
downsmash_finisher = Combo([twisted_collision, sea_burial, gushing_waters, earthsplitter, recoil_slam])

twisted_sa = Combo([twisted_collision_sa, sky_rammer])

def crit_rate_active():
    buffs = wincap.get_buffs()
    if crit_rate_buff.ready(buffs):
        return True
    return False

def attack_speed_active():
    buffs = wincap.get_buffs()
    if attack_speed_buff.ready(buffs) or dragonize_buff.ready(buffs):
        return True
    return False

def target_dp_debuffed():
    debuffs = wincap.get_debuffs()
    x, y = dp_debuff.ready(debuffs, count=True)
    if x and y >= 2:
        return True
    return False

def double_crit_active():
    buffs = wincap.get_buffs()
    x, y = crit_rate_buff.ready(buffs, count=True)
    if x and y >= 2:
        return True
    return False

def ap_buff_active():
    buffs = wincap.get_buffs()
    if ap_buff.ready(buffs):
        return True
    return False
