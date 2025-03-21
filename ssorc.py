import time

from sorc.succession import *
import common.utils as utils
from common.listener import Listener
from common.spell import Spell
from common.config_manager import initialize_configuration, init_spells, wait_for_bdo_active

spells_init = False
var = utils.Variables()
var.state = [False, False, False, False, False, False, False]
var.last_cast = 0

print("Starting BDO Sorc Tool...")

if not initialize_configuration(wait_for_bdo=True, max_wait_seconds=120):
    print("Configuration initialization failed. Some features may not work correctly.")

def main(context):
    if time.time() - var.last_cast > 0.6:
        var.state = [False, False, False, False, False, False, False]

    print(f"Entering main loop at time: {time.time()}")
    var.state = pve(context, var.state, var.last_cast)
    var.last_cast = time.time()

def reposition_right(context):
    iframe_right.cast(context)

def reposition_left(context):
    iframe_left.cast(context)

def iframe_forward_mmb(context):
    iframe_forward_180_mmb.cast(context)
    var.state = [False, False, False, False, False, False, False]

def iframe_forward_button4(context):
    iframe_forward_180_button4.cast(context)
    var.state = [False, False, False, False, False, False, False]

listener = Listener(debug=False)
listener.register_keybind('f24', main)
listener.register_mouse_override('middle', iframe_forward_mmb)
listener.register_mouse_override('button4', iframe_forward_button4)
# listener.register_keybind('shift+d', reposition_right, override=True)
# listener.register_keybind('shift+a', reposition_left, override=True)
# listener.register_keybind('f22', iframe_forward)
listener.start()

try:
    while True:
        if not spells_init:
            # Wait for BDO to be active before initializing spells
            if wait_for_bdo_active(max_wait_seconds=0):  # Wait indefinitely
                if init_spells(Spell.instances):
                    spells_init = True
                else:
                    print("Spell initialization failed. Will retry in 10 seconds.")
                    time.sleep(10)  # Wait before retry
        time.sleep(5)
except KeyboardInterrupt:
    print("end")
finally:
    listener.stop()
