import time
import keyboard
import mouse
import pynput.keyboard as kboard
from pynput.keyboard import Key, KeyCode
from pynput.mouse import Button, Controller
import win32api
import pynput


def apply_speed_modifier(base, modifier):
    return 1/(modifier/base)


def custom_mouse_handler(x, y, delay, absolute=False, mouse_click=False, handler_type='release'):
    def handler(bind, context, hold_time, modifier):
        local_delay = delay

        if handler_type == 'hold_and_release_early':
            start_time = time.time()
            calculated_hold_time = apply_speed_modifier(hold_time, modifier)
            while(context.is_active() and time.time() - start_time < calculated_hold_time * 0.7 - local_delay - 0.05):
                time.sleep(0.05)
        bind.release()
        bind.mouse_listener = pynput.mouse.Listener(win32_event_filter=bind._win32_event_filter)
        bind.mouse_listener.start()

        try:
            if mouse_click:
                keyboard.send('left ctrl')
                local_delay -= 0.05
                time.sleep(0.05)
            bind.mouse_suppressed = False
            if not absolute:
                current_mouse_x, current_mouse_y = mouse.get_position()
                screen_width, screen_height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
                target_x = current_mouse_x + x
                target_y = current_mouse_y + y

                # Define boundary constants
                min_x = 15
                max_x = screen_width - 15
                min_y = 15
                max_y = screen_height - 15

                # Initial remaining calculation
                remaining_x = target_x - current_mouse_x
                remaining_y = target_y - current_mouse_y
                # print(f"Moving to: {target_x}, {target_y}")

                # Counter to prevent infinite loops
                move_counter = 0
                max_moves = 20  # Safety limit
                
                while (abs(remaining_x) > 5 or abs(remaining_y) > 5) and move_counter < max_moves:
                    # Initialize default values for bounded_x and bounded_y
                    bounded_x = 0
                    bounded_y = 0
                    
                    # Only calculate bounded_x if there's significant x movement needed
                    if abs(remaining_x) > 5:
                        # Calculate the target position after movement
                        next_x = current_mouse_x + remaining_x
                        
                        # Constrain the target position to screen boundaries
                        bounded_next_x = max(min(next_x, max_x), min_x)
                        
                        # Calculate the movement needed to reach the bounded position
                        bounded_x = bounded_next_x - current_mouse_x
                    
                    # Only calculate bounded_y if there's significant y movement needed
                    if abs(remaining_y) > 5:
                        # Calculate the target position after movement
                        next_y = current_mouse_y + remaining_y
                        
                        # Constrain the target position to screen boundaries
                        bounded_next_y = max(min(next_y, max_y), min_y)
                        
                        # Calculate the movement needed to reach the bounded position
                        bounded_y = bounded_next_y - current_mouse_y

                    # print(f"Moving by: {bounded_x}, {bounded_y}")
                    mouse.move(bounded_x, bounded_y, False)
                    time.sleep(0.02)  # Reduced from 1.0 for faster response
                    local_delay -= 0.02

                    # print(f"Current: {mouse.get_position()}")
                    current_mouse_x, current_mouse_y = mouse.get_position()
                    
                    # Update remaining movement
                    remaining_x = remaining_x - bounded_x
                    remaining_y = remaining_y - bounded_y
                    # print(f"Remaining: {remaining_x}, {remaining_y}")
                    
                    # Increment counter for safety
                    move_counter += 1
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
            while(context.is_active() and time.time() - start_time < apply_speed_modifier(hold_time, modifier) - local_delay):
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
        self.mouse_controller = Controller()
    
    def press(self, kb_override=None, ms_override=None):
        if kb_override is None and ms_override is None:
            if self.kb_input is not None:
                keyboard.press(self.kb_input)
                self.pressed_kb_keys.append(self.kb_input)

            if self.ms_input is not None:
                ms_input_parts = self.ms_input.split('+')
                for part in ms_input_parts:
                    self.mouse_controller.press(Button[part])
                    # mouse.press(part)
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
                    self.mouse_controller.press(Button[part])
                    # mouse.press(part)
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
                self.mouse_controller.release(Button[key])
                # mouse.release(key)
                self.pressed_ms_keys.remove(key)
        else:
            if kb_override is not None:
                keyboard.release(kb_override)
                self.pressed_kb_keys.remove(kb_override)
            if ms_override is not None:
                ms_input_parts = ms_override.split('+')
                for part in ms_input_parts:
                    self.mouse_controller.release(Button[part])
                    # mouse.release(part)
                    self.pressed_ms_keys.remove(part)

    def _win32_event_filter(self, msg, data):
        if msg == 513 or msg == 514 or msg == 512:
            if self.mouse_suppressed:
                self.mouse_listener.suppress_event()
