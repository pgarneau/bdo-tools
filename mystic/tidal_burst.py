import time
import keyboard
from vision import Vision
import settings
from windowcapture import WindowCapture
from spell import Spell

wincap = WindowCapture()

class TidalBurst(Spell):
    # constructor
    # def __init__(self, name, bind, speed_function, threshold=0.96):
    #     super().__init__(name, bind, speed_function, threshold)
    #     self.mov_speed_vision = Vision(f"./spells/movement_speed_5.png")
    
    def cast(self):
        counter = 0
        if settings.keybind_active():
            print(f"Casting: {self.name}")
            self.bind.press()
            while(self.ready() and counter < 8 and settings.keybind_active()):
                counter += 1
                time.sleep(0.08)
        
            if counter >= 8 and counter != 0:
                print("Spell cast failed")
                self.bind.release()
                return False
            elif counter == 0:
                self.last_cast = time.time()
                time.sleep(0.3)
                self.bind.hold_and_release(self.speed_function())
                return True
            else:
                self.last_cast = time.time()
                self.bind.hold_and_release(self.speed_function())
                return True
    
    # def mov_speed_buff_active(self, debug=None):
    #     screenshot = self.wincap.get_buffs()

    #     coords = self.mov_speed_vision.find(screenshot, 0.99, debug)
    #     if len(coords) > 0:
    #         return True
    
    #     return False
