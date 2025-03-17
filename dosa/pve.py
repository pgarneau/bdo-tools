from .spells import *

# Combo1 = water
# Combo2 = Fire
def pve(state, last_cast):
    # if elemental_invocation.ready():
    #     if elemental_invocation.cast():
    #         return 0
    if part_1.ready():
        # if time.time() - last_cast >= 1.3 and sundering_sweep.ready():
        #     sundering_sweep_1hit.cast()
        if cast_speed_active() or shai_buff_active():
            if part_1_speed.cast():
                return 0
            return 1
        else:
            if part_1.cast():
                return 0
            return 1

    elif part_2.ready():
        if cast_speed_active() or shai_buff_active():
            if part_2_speed.cast():
                return 0
            return 2
        else:
            if part_2.cast():
                return 0
            return 2

    elif state == 1:
        if metal_earth_metal.ready():
            if cast_speed_active() or shai_buff_active():
                if metal_earth_metal_speed.cast():
                    return 0
            else:
                if metal_earth_metal.cast():
                    return 0

        elif earth_metal.ready():
            if cast_speed_active() or shai_buff_active():
                earth_metal_speed.cast()
                return 0
            else:
                earth_metal.cast()
                return 0
        
    elif state == 2:
        if fire_wood_fire_wood.ready():
            if cast_speed_active() or shai_buff_active():
                if fire_wood_fire_wood_speed.cast():
                    return 0
            else:
                if fire_wood_fire_wood.cast():
                    return 0
        elif wood_fire_wood.ready():
            if wood_fire_wood.cast():
                return 0
        elif fire_wood.ready():
            fire_wood.cast()
            return 0

    elif not shai_buff_active() and sundering_sweep.ready():
        if sundering_sweep_1hit.cast():
            return 0
    elif cast_speed_active() and shai_buff_active() and sundering_sweep.ready():
        if sundering_sweep.cast():
            return 0
    
    elif pre_awak_combo.ready():
        if pre_awak_combo.cast():
            return 0

    elif fire_wood.ready():
        fire_wood.cast()
        return 0
    
    return 0
