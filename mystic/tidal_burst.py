import time
from common.spell import Spell

class TidalBurst(Spell):
    # constructor
    # def __init__(self, name, bind, speed_function, threshold=0.96):
    #     super().__init__(name, bind, speed_function, threshold)
    #     self.mov_speed_vision = Vision(f"./spells/movement_speed_5.png")
    
    def cast(self, context):
        counter = 0
        counter_max = 8

        if context.is_active():
            print(f"Casting: {self.name}")
            self.bind.press()
            while(self.ready() and counter < counter_max and context.is_active()):
                counter += 1
                time.sleep(0.08)
        
            if counter >= counter_max and counter != 0:
                print("Spell cast failed")
                self.bind.release()
                return False
            elif counter == 0:
                self.last_cast = time.time()
                time.sleep(0.3)
                self.bind.hold_and_release(context, self.duration, self.speed_function())
                return True
            else:
                self.last_cast = time.time()
                self.bind.hold_and_release(context, self.duration, self.speed_function())
                return True
    
    # def mov_speed_buff_active(self, debug=None):
    #     screenshot = self.wincap.get_buffs()

    #     coords = self.mov_speed_vision.find(screenshot, 0.99, debug)
    #     if len(coords) > 0:
    #         return True
    
    #     return False
