import time

from sorc.awakening import *
import common.utils as utils
from common.listener import Listener, Context
from common.spell import Spell

spells_init = False
var = utils.Variables()
var.state = 0
var.last_cast = 0


def main(context):
    var.state = pve(context, var.last_cast, var.state)

def reposition_right(context):
    var.state, var.last_cast = calamity(context, 'right', var.state)

def reposition_left(context):
    var.state, var.last_cast = calamity(context, 'left', var.state)

listener = Listener(debug=False)
listener.register_keybind('f24', main)
listener.register_keybind('shift+d', reposition_right, override=True)
listener.register_keybind('shift+a', reposition_left, override=True)
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
