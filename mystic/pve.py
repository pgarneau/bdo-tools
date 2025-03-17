from .spells import *

def pve(last_cast):
    spirits = shard_count.count_shards()
    print(spirits)

    # if dragonize.ready() and not ap_buff_active() and time.time() - last_cast >= 1.5:
    #     if dragonize.cast():
    #         return time.time()
    if not attack_speed_active() and crouching_wolf.ready() and spirits == 3 and time.time() - last_cast <= 0.7:
        if crouching_wolf.cast():
            return time.time()
    elif not target_dp_debuffed() and rapid_stream.ready():
        if not attack_speed_active() and crouching_wolf.ready():
            if tidal_crouching_combo.cast():
                return time.time()
        elif tidal_combo.cast():
            return time.time()
    elif rising_gushing_wave_combo.ready() and spirits == 3:
        if rising_gushing_wave_combo.cast():
            return time.time()
    elif rising_gushing_sea_combo.ready() and spirits >= 2:
        if rising_gushing_sea_combo.cast():
            return time.time()
    elif rising_gushing_combo.ready() and spirits >= 1:
        if rising_gushing_combo.cast():
            return time.time()
    elif earthsplitter_wave_combo.ready() and spirits >= 2:
        if earthsplitter_wave_combo.cast():
            return time.time()
    elif hurricane_wave_combo.ready() and spirits >= 2:
        if hurricane_wave_combo.cast():
            return time.time()
    elif tidal_wave_combo.ready():
        if tidal_wave_combo.cast():
            return time.time()
    elif dragon_wave_combo.ready() and spirits >= 2:
        if dragon_wave_combo.cast():
            return time.time()
    elif hurricane_sea_combo.ready() and spirits >= 1:
        if hurricane_sea_combo.cast():
            return time.time()
    elif sea_burial.ready() and spirits >= 1:
        if sea_burial.cast():
            return time.time()
    elif earthsplitter.ready():
        if earthsplitter.cast():
            return time.time()
    elif not double_crit_active() and rapid_stream.ready():
        if tidal_combo.cast():
            return time.time()
    elif hurricane_c_swap.ready():
        if hurricane_c_swap.cast():
            return time.time()
    elif tidal_burst.ready():
        if tidal_burst.cast():
            return time.time()
    elif dragon_strike.ready():
        if dragon_strike.cast():
            return time.time()
    # elif hurricane_sweep.ready():
    #     if hurricane_sweep.cast():
    #         return time.time()
    else:
        if tidal_burst.cast():
            return time.time()
    
    return None
    

def some_func():
    counter = 0
    while True:
        if not wave_orb.ready():
            while(crouching_wolf.ready()):
                print("waiting")
                counter += 0.01
                time.sleep(0.01)
            break
    
    print(counter)
