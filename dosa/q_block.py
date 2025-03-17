from vision import Vision
import settings
from windowcapture import WindowCapture
import time
from spell import Spell

wincap = WindowCapture()

def default_speed_function():
    return 1

class QBlock():
    # properties
    vision = 0
    wincap = 0
    threshold = 0
    name = 0
    location = None
    cooldown = 0
    last_cast = 0

    # constructor
    def __init__(self, name, bind, speed_function=default_speed_function, threshold=0.96):
        self.name = name
        self.vision = Vision(f"./spells/block.png")
        self.vision_bright = Vision("./spells/bright_block.png")
        self.bind = bind
        self.threshold = threshold
        self.wincap = wincap
        self.speed_function = speed_function
    
    def ready(self, debug=None):
        self.bind.press()
        time.sleep(0.1)
        self.cast_successful()
        self.bind.release()
        # self.cast()
    
    def ready_in(self, seconds):
        return True

    def cast_successful(self, debug=None):
        if debug: print(f"looking for {self.name}")
        threshold = self.threshold
        
        screenshot = self.wincap.get_defense_icon()

        coords = self.vision.find(screenshot, threshold, debug)
        coords = coords if len(coords) > 0 else self.vision_bright.find(screenshot, threshold, debug)

        if len(coords) > 0:
            return True
        
        return False

    def cast(self):
        counter = 0
        if settings.keybind_active():
            print(f"Casting: {self.name}")
            self.bind.press()
            while(not self.cast_successful() and counter < 8 and settings.keybind_active()):
                counter += 1
                time.sleep(0.08)
        
            if counter >= 8:
                print("Spell cast failed")
                self.bind.release()
                return False
            else:
                self.bind.hold_and_release(self.speed_function())
                return True