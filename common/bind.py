import time
import keyboard
import mouse
import pynput.keyboard as kboard
from pynput.keyboard import Key, KeyCode
import win32api
import pynput


def apply_speed_modifier(base, modifier):
    return 1/(modifier/base)


def custom_mouse_handler(x, y, delay, absolute=False, mouse_click=False, handler_type='release'):
    def handler(bind, context, hold_time, modifier):
        if handler_type == 'hold_and_release_early':
            start_time = time.time()
            calculated_hold_time = apply_speed_modifier(hold_time, modifier)
            while(context.is_active() and time.time() - start_time < calculated_hold_time * 0.7 - delay - 0.05):
                time.sleep(0.05)
        bind.release()
        bind.mouse_listener = pynput.mouse.Listener(win32_event_filter=bind._win32_event_filter)
        bind.mouse_listener.start()

        try:
            if mouse_click:
                keyboard.send('left ctrl')
                time.sleep(0.05)
            bind.mouse_suppressed = False
            if not absolute:
                current_mouse_x, current_mouse_y = mouse.get_position()
                print(current_mouse_x, current_mouse_y)
                screen_width, screen_height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
                target_x = current_mouse_x + x
                target_y = current_mouse_y + y

                min_x = 15
                max_x = screen_width - 15
                min_y = 15
                max_y = screen_height - 15

                first_x = max(min(target_x, max_x), min_x)
                first_y = max(min(target_y, max_y), min_y)

                if target_x != first_x or target_y != first_y:
                    delta_x = first_x - current_mouse_x
                    delta_y = first_y - current_mouse_y
                    # print(f"Moving: {delta_x}, {delta_y}")
                    mouse.move(delta_x, delta_y, False)
                    # Important small delay to allow mouse to reset
                    delay = delay - 0.05
                    time.sleep(0.05)
                    # print(mouse.get_position())
                    mouse.move(x - delta_x, y - delta_y, False)
                else:
                    mouse.move(x, y, False)
            else:
                mouse.move(x, y, True)
            if mouse_click:
                mouse.click('left')
                bind.mouse_suppressed = True
                time.sleep(delay)
                keyboard.send('left ctrl')
        finally:
            if bind.mouse_listener and bind.mouse_listener.is_alive():
                bind.mouse_listener.stop()
                bind.mouse_listener = None

        if handler_type == 'release':
            start_time = time.time()
            while(context.is_active() and time.time() - start_time < apply_speed_modifier(hold_time, modifier) - delay - 0.05):
                time.sleep(0.05)
    
    return handler

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
    def __init__(self, kb, mouse, hold_handler=default_hold_and_release_handler, hotbar=False, movement_handler=None):
        self.kb_input = kb
        self.ms_input = mouse
        self.hold_handler = hold_handler
        self.hotbar = hotbar
        self.pressed_kb_keys = []
        self.pressed_ms_keys = []
        self.mouse_listener = None
        self.mouse_suppressed = False
    
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

    def _win32_event_filter(self, msg, data):
        if msg == 513 or msg == 514 or msg == 512:
            if self.mouse_suppressed:
                self.mouse_listener.suppress_event()
