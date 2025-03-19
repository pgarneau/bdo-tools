import time

from guardian.awakening import *
import common.utils as utils
from common.listener import Listener, Context
from common.spell import Spell

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
            if utils.init_spells(Spell.instances):
                spells_init = True
        time.sleep(5)
        # pass
except KeyboardInterrupt:
    print("end")
finally:
    listener.stop()
