import time
import keyboard
import mouse
import pynput.keyboard as kboard
from pynput.keyboard import Key, KeyCode, Controller


def apply_speed_modifier(base, modifier):
    return 1/(modifier/base)


def default_hold_and_release_handler(bind, context, hold_time, modifier):
    bind.release()
    if hold_time > 0:
        start_time = time.time()
        while(context.is_active() and time.time() - start_time < apply_speed_modifier(hold_time, modifier)):
            time.sleep(0.05)

def hold_bind(bind, context, hold_time, modifier):
    if hold_time > 0:
        start_time = time.time()
        while(context.is_active() and time.time() - start_time < apply_speed_modifier(hold_time, modifier)):
            time.sleep(0.05)
    bind.release()

def hold_bind_release_early(bind, context, hold_time, modifier):
    if hold_time > 0:
        start_time = time.time()
        calculated_hold_time = apply_speed_modifier(hold_time, modifier)
        while(context.is_active() and time.time() - start_time < calculated_hold_time * 0.7):
            time.sleep(0.05)
    bind.release()

class Bind:
    def __init__(self, kb, mouse, hold_handler=hold_bind_release_early, hotbar=False):
        self.kb_input = kb
        self.ms_input = mouse
        self.hold_handler = hold_handler
        self.hotbar = hotbar
        self.kb_controller = Controller()
    
    def press(self):
        if self.kb_input is not None:
            keyboard.press(self.kb_input)
        if self.ms_input is not None:
            if self.ms_input == 'left+right':
                mouse.press('left')
                mouse.press('right')
            else:
                mouse.press(self.ms_input)
    
    def hold_and_release(self, context, hold_time, modifier):
        if self.hotbar:
            self.release()
            return

        self.hold_handler(self, context, hold_time, modifier)
    
    def release(self):
        if self.kb_input is not None:    
            keyboard.release(self.kb_input)
        if self.ms_input is not None:
            if self.ms_input == 'left+right':
                mouse.release('left')
                mouse.release('right')
            else:
                mouse.release(self.ms_input)


    @staticmethod
    def parse(keys):
        modifiers = ['shift', 'ctrl', 'alt']

        def parts():
            start = 0
            for i, c in enumerate(keys):
                if c == '+' and i != start:
                    yield keys[start:i]
                    start = i + 1
            if start == len(keys):
                raise ValueError(keys)
            else:
                yield keys[start:]

        def parse(s):
            if len(s) == 1:
                return KeyCode.from_char(s.lower())
            elif len(s) > 2 and s in modifiers:
                return getattr(Key, s.lower())
            elif len(s) >= 2 and s.lower().startswith('f') and s[1:].isdigit():
                return getattr(Key, f'f{s[1:]}')
            elif len(s) >= 2:
                try:
                    return getattr(Key, s.lower())
                except AttributeError:
                    raise ValueError(f"Unknown key: {s}")

        # Split the string and parse the individual parts
        raw_parts = list(parts())
        parsed_parts = [
            parse(s)
            for s in raw_parts]

        # Ensure no duplicate parts
        if len(parsed_parts) != len(set(parsed_parts)):
            raise ValueError(keys)
        else:
            return parsed_parts