import time

def default_additiona_condition():
    return True

class Combo:
    spells = []
    additional_condition = False

    def __init__(self, spells, additional_condition=default_additiona_condition):
        self.spells = spells
        self.additional_condition = additional_condition

    def ready(self):
        time_offset = 0
        for spell in self.spells:
            if not spell.ready_in(time_offset) or not self.additional_condition():
            # if not spell.ready() or not self.additional_condition():
                return False
            time_offset += spell.duration
        
        return True
    
    def cast(self, context):
        counter = 0
        current_index = 0
        while(current_index < len(self.spells) and context.is_active() and counter < 4):
            if self.additional_condition() and self.spells[current_index].cast(context):
                current_index += 1
                counter = 0
                continue

            counter += 1
            time.sleep(0.1)
        
        if current_index == len(self.spells):
            return True
        
        return False
