
import os
import time
from .windowcapture import wincap
from .vision import Vision
from common.listener import Context

def default_speed_function():
    return 1

def link_spells(*spells):
    shared_spell_data = SharedSpellData()

    for spell in spells:
        spell.shared_data = shared_spell_data

class SharedSpellData:
    def __init__(self):
        self.last_cast = 0
        self.location = 0

class Spell:
    # Instances of Spell
    instances = []

    # constructor
    def __init__(self, vision, bind, duration=0, cooldown=0, speed_function=default_speed_function):
        self.name = vision.name
        self.vision = vision
        self.bind = bind
        self.duration = duration
        self.cooldown = cooldown
        self.speed_function = speed_function

        self.shared_data = SharedSpellData()

        Spell.instances.append(self)
    
    def ready(self, screenshot=None, count=False, debug=False):
        if debug: print(f"looking for {self.name}")
        if screenshot is None:
            if self.shared_data.location:
                screenshot = wincap.get_screenshot(*self.shared_data.location)
            else:
                screenshot = wincap.get_skills()

        coords = self.vision.find(screenshot, debug=debug)
        if len(coords) > 0:
            # Store where u found the skill for future screenshotting
            if not self.shared_data.location:
                temp_location = (0, 0, 0, 0)
                for coord in coords:
                    # if coord is not None and isinstance(coord, (list, tuple)) and len(coord) == 4:
                    if coord[0] > temp_location[0]:
                        temp_location = coord
                
                if temp_location[0] != 0:
                    self.shared_data.location = temp_location
            
            if count:
                return True, len(coords)
            return True

        if count:
            return False, 0
        return False
    
    def ready_in(self, seconds):
        if seconds == 0 or self.shared_data.last_cast == 0:
            return self.ready()

        time_left = self.shared_data.last_cast + self.cooldown - time.time()

        if time_left <= 0 or time_left <= seconds:
            return True
        return False
        
    def cast(self, context, debug=False):
        counter = 0
        counter_max = 8

        if context.is_active():
            print(f"Casting: {self.name}")
            if self.bind.hotbar:
                while(self.ready(debug=debug) and counter < counter_max and context.is_active()):
                    if counter > 0 :
                        self.bind.release()
                    self.bind.press()
                    counter += 1
                    time.sleep(0.08)
            else:
                self.bind.press()
                while(self.ready(debug=debug) and counter < counter_max and context.is_active()):
                    counter += 1
                    time.sleep(0.08)
            
            if counter >= 8:
                print("Spell cast failed")
                self.bind.release()
                return False
            elif not context.is_active():
                self.bind.release()
                if self.ready(debug=debug):
                    print("Spell cast not completed")
                    return False
                else:
                    self.shared_data.last_cast = time.time()
                    return True
            else:
                self.shared_data.last_cast = time.time()
                self.bind.hold_and_release(context, self.duration, self.speed_function())
                return True

class BsrConsume(Spell):
    def ready(self, screenshot=None, count=False, debug=False):
        bsr_ss = wincap.get_bsr()
        return super().ready(bsr_ss, count, debug)

class NoCooldownSpell:
    # constructor
    def __init__(self, name, bind, duration, speed_function=default_speed_function):
        self.name = name
        self.bind = bind
        self.duration = duration
        self.speed_function = speed_function
    
    def ready(self):
        return True
        
    def cast(self, context):
        counter = 0
        if context.is_active():
            print(f"Casting: {self.name}")
            if self.bind.hotbar:
                while (counter < 3 and context.is_active()):
                    if counter > 0:
                        self.bind.release()
                    self.bind.press()
                    counter += 1
                    time.sleep(0.08)
            else:
                self.bind.press()
        
            self.bind.hold_and_release(context, self.duration, self.speed_function())
            return True
    
    def ready_in(self, seconds):
        return True

class HoldAndSpamSpell(Spell):
    def __init__(self, vision, bind, spam_bind, duration, cooldown, speed_function=default_speed_function):
        super().__init__(vision, bind, duration, cooldown, speed_function)
        self.spam_bind = spam_bind
    
    def cast(self, context):
        counter = 0
        counter_max = 8

        if context.is_active():
            print(f"Casting: {self.name}")

            self.bind.press()
            # MINI DELAY
            time.sleep(0.05)
            while(self.ready() and counter < counter_max and context.is_active()):
                if counter > 0:
                    self.bind.release(kb_override=self.spam_bind.kb_input, ms_override=self.spam_bind.ms_input)
                self.bind.press(kb_override=self.spam_bind.kb_input, ms_override=self.spam_bind.ms_input)
                counter += 1
                time.sleep(0.08)
            
            if counter >= 8:
                print("Spell cast failed")
                self.bind.release()
                return False
            elif not context.is_active():
                self.bind.release()
                if self.ready():
                    print("Spell cast not completed")
                    return False
                else:
                    self.shared_data.last_cast = time.time()
                    return True
            else:
                self.shared_data.last_cast = time.time()
                self.bind.hold_and_release(context, self.duration, self.speed_function())
                return True

class DefenseSpell:
    # constructor
    def __init__(self, vision, bind, duration, speed_function=default_speed_function):
        self.name = vision.name
        self.vision = vision
        self.bind = bind
        self.duration = duration
        self.speed_function = speed_function
    
    def ready(self):
        return True
    def ready_in(self, seconds):
        return True
    def cast_successful(self, debug=None):
        if debug: print(f"looking for {self.name}")
        
        screenshot = wincap.get_defense_icon()

        coords = self.vision.find(screenshot, debug=debug)

        if len(coords) > 0:
            return True
        
        return False
    def cast(self, context, debug=False):
        counter = 0
        counter_max = 16

        if context.is_active():
            print(f"Casting: {self.name}")
            if self.bind.hotbar:
                while(not self.cast_successful(debug) and counter < counter_max and context.is_active()):
                    if counter > 0 :
                        self.bind.release()
                    self.bind.press()
                    counter += 1
                    time.sleep(0.05)
            else:
                while(not self.cast_successful(debug) and counter < counter_max and context.is_active()):
                    if counter > 0 :
                        self.bind.release()
                    self.bind.press()
                    counter += 1
                    time.sleep(0.05)
            
            if counter >= 8:
                print("Spell cast failed")
                self.bind.release()
                return False
            elif not context.is_active():
                self.bind.release()
                if not self.cast_successful(debug):
                    print("Spell cast not completed")
                    return False
                else:
                    return True
            else:
                self.bind.hold_and_release(context, self.duration, self.speed_function())
                return True
    
class Iframe(DefenseSpell):
    def __init__(self, bind, duration, speed_function=default_speed_function):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        super().__init__(Vision('iframe2', threshold=0.98, base_path=os.path.join(current_dir, 'spells')), bind, duration, speed_function)

class SkillLogSpell(Spell):
    def ready(self, debug=False):
        return True
    def ready_in(self, seconds):
        return True
    
    def cast_successful(self, debug=False):
        if debug: print(f"looking for {self.name}")
        
        screenshot = wincap.get_skill_log()
        coords = self.vision.find(screenshot, debug=debug)

        if len(coords) > 0:
            return True
        
        return False

    def cast(self, context, debug=False):
        counter = 0
        counter_max = 12

        if context.is_active():
            print(f"Casting: {self.name}")
            if self.bind.hotbar:
                while(not self.cast_successful(debug) and counter < counter_max and context.is_active()):
                    if counter > 0 :
                        self.bind.release()
                    self.bind.press()
                    counter += 1
                    time.sleep(0.05)
            else:
                while(not self.cast_successful(debug) and counter < counter_max and context.is_active()):
                    if counter > 0 :
                        self.bind.release()
                    self.bind.press()
                    counter += 1
                    time.sleep(0.05)
            
            if counter >= 8:
                print("Spell cast failed")
                self.bind.release()
                return False
            elif not context.is_active():
                self.bind.release()
                if not self.cast_successful(debug):
                    print("Spell cast not completed")
                    return False
                else:
                    return True
            else:
                self.bind.hold_and_release(context, self.duration, self.speed_function())
                return True
