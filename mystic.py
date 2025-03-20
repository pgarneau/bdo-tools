import cv2 as cv
import time
from common.windowcapture import wincap
import common.utils as utils
from common.listener import Listener
from mystic.pve import *
from mystic.pvp import *
from common.spell import Spell
from common.config_manager import initialize_configuration, init_spells, wait_for_bdo_active

spells_init = False
var = utils.Variables()
var.last_cast = 0

print("Starting BDO Mystic Tool...")

# Initialize configuration automatically at startup
# This will wait for BDO to become active if needed
if not initialize_configuration(wait_for_bdo=True, max_wait_seconds=120):
    print("Configuration initialization failed. Some features may not work correctly.")

def main(context):
    new_last_cast = pve(context, var.last_cast)
    var.last_cast = new_last_cast if new_last_cast is not None else var.last_cast

listener = Listener(debug=False)
listener.register_keybind('f24', main)
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