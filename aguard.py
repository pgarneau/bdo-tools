import time

from guardian.awakening import *
import common.utils as utils
from common.listener import Listener, Context
from common.spell import Spell
from common.config_manager import initialize_configuration, init_spells, wait_for_bdo_active

spells_init = False
var = utils.Variables()
var.state = 0
var.last_cast = 0


def main(context):
    pve(context)

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
