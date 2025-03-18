import cv2 as cv
import time
from common.windowcapture import wincap
import common.utils as utils
from common.listener import Listener
from mystic.pve import *
from mystic.pvp import *


spells_init = False
var = utils.Variables()
var.last_cast = 0

def main(context):
    new_last_cast = pve(context, var.last_cast)
    var.last_cast = new_last_cast if new_last_cast is not None else var.last_cast

listener = Listener()
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