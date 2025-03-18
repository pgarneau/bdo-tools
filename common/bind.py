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
    def __init__(self, kb, mouse, hold_handler=default_hold_and_release_handler, hotbar=False):
        self.kb_input = kb
        self.ms_input = mouse
        self.hold_handler = hold_handler
        self.hotbar = hotbar
        self.pressed_kb_keys = []
        self.pressed_ms_keys = []
    
    def press(self, kb_override=None, ms_override=None):
        if kb_override is None and ms_override is None:
            if self.kb_input is not None:
                keyboard.press(self.kb_input)
                self.pressed_kb_keys.append(self.kb_input)

            if self.ms_input is not None:
                ms_input_parts = self.ms_input.split('+')
                for part in ms_input_parts:
                    mouse.press(part)
                    self.pressed_ms_keys.append(part)
                    if len(ms_input_parts) > 1:
                        time.sleep(0.02)
        
        else:
            if kb_override is not None:
                keyboard.press(kb_override)
                self.pressed_kb_keys.append(kb_override)
            if ms_override is not None:
                ms_override_parts = ms_override.split('+')
                for part in ms_override_parts:
                    mouse.press(part)
                    self.pressed_ms_keys.append(part)
                    if len(ms_override_parts) > 1:
                        time.sleep(0.02)
    
    def hold_and_release(self, context, hold_time, modifier):
        self.hold_handler(self, context, hold_time, modifier)
    
    def release(self, kb_override=None, ms_override=None):
        if kb_override is None and ms_override is None:
            for key in list(self.pressed_kb_keys):
                keyboard.release(key)
                self.pressed_kb_keys.remove(key)
            for key in list(self.pressed_ms_keys):
                mouse.release(key)
                self.pressed_ms_keys.remove(key)
        else:
            if kb_override is not None:
                keyboard.release(kb_override)
                self.pressed_kb_keys.remove(kb_override)
            if ms_override is not None:
                ms_input_parts = ms_override.split('+')
                for part in ms_input_parts:
                    mouse.release(part)
                    self.pressed_ms_keys.remove(part)

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