import time
from pynput import keyboard
import threading
import keyboard as kb

MODIFIERS = ['shift', 'ctrl', 'alt']

class Context:
    def __init__(self):
        self.cancelled = False
        self.keybind_id = None
    
    def cancel(self):
        self.cancelled = True
    
    def is_cancelled(self):
        return self.cancelled

    def is_active(self):
        return not self.cancelled

    def set_keybind_id(self, keybind_id):
        self.keybind_id = keybind_id
    
    def get_keybind_id(self):
        return self.keybind_id
    
    def reset(self):
        self.cancelled = False
        self.keybind_id = None

class KeyBind:
    def __init__(self, key_input, callback, name, debug=False):
        self.input = key_input
        self.callback = callback
        self.scan_code_set = self.parse_input(key_input, debug)
        self.name = name
        self.is_active = False
        self.debug = debug

    def _map_key(self, key):
        if key in MODIFIERS:
            return getattr(keyboard.Key, key)
        elif key.startswith('f') and key[1:].isdigit():
            return getattr(keyboard.Key, f'f{key[1:]}')
        elif len(key) == 1:
            return keyboard.KeyCode.from_char(key)
        else:
            raise ValueError(f"Invalid key: {key}")
    
    def parse_input(self, key_input, debug=False):
        try:
            scan_code_set = frozenset(min(scan_code) for scan_code in kb.parse_hotkey(key_input)[0])
            if debug:
                print(f"Scan codes for {key_input}: {scan_code_set}")
        except Exception as e:
            if debug:
                print(f"Error parsing scan codes for {key_input}: {e}")
            scan_code_set = frozenset()

        return scan_code_set
    
    def is_pressed(self, current_keys):
        try:
            key_match = self.scan_code_set.issubset(current_keys)
            if self.debug:
                print(f"  Checking scan codes: {self.scan_code_set} against {current_keys}: {key_match}")
            return key_match
        except Exception as e:
            if self.debug:
                print(f"Error in is_pressed: {e}")
            return False

class Listener:

    def __init__(self, debug=False):
        self.debug = debug
        self.current_keys = set()
        self.listener = keyboard.Listener(
            on_press=self.on_press, 
            on_release=self.on_release, 
            win32_event_filter=self.win32_event_filter
        )

        self.main_keybinds = {}
        self.override_keybinds = {}

        self.action_thread = None
        self.action_lock = threading.Lock()
        self.thread_running = False
        self.current_context = Context()

        self.override_queued = False
        self.current_thread_is_override = False
        self.queued_override_id = None

        self.active_main_keybind_id = None
        self.triggering_main_keybind_id = None
        self.any_main_keybind_active = False
    
    def register_keybind(self, key_combination, callback, override=False):
        if override:
            keybind_id = f"override_{len(self.override_keybinds)}"
        else:
            keybind_id = f"main_{len(self.main_keybinds)}"

        keybind = KeyBind(key_combination, callback, keybind_id, debug=self.debug)
        
        if override:
            self.override_keybinds[keybind_id] = keybind
            if self.debug:
                print(f"Registered override keybind '{keybind_id}': {key_combination}")
        else:
            self.main_keybinds[keybind_id] = keybind
            if self.debug:
                print(f"Registered main keybind '{keybind_id}': {key_combination}")
                
        return keybind_id
    
    def update_keybind_states(self):
        if self.debug:
            print("Updating keybind states")
        
        self.any_main_keybind_active = False
        currently_active = []
        
        # Single pass to update states and handle releases/activations
        for keybind_id, keybind in self.main_keybinds.items():
            was_active = keybind.is_active
            keybind.is_active = keybind.is_pressed(self.current_keys)
            
            if keybind.is_active:
                self.any_main_keybind_active = True
                currently_active.append(keybind_id)
                
            # If this main keybind was released and it was the active keybind
            if was_active and not keybind.is_active and keybind_id == self.active_main_keybind_id:
                if self.debug:
                    print(f"Active keybind '{keybind_id}' released")
                    
                if self.thread_running:
                    if self.debug:
                        print(f"Cancelling current context due to releasing active keybind")
                    self.current_context.cancel()
                    self.override_queued = False
                    
                self.active_main_keybind_id = None
        
        # If no active keybind but we have active keys, set the first one as active
        if not self.active_main_keybind_id and currently_active:
            self.active_main_keybind_id = currently_active[0]
            if self.debug:
                print(f"New active main keybind: {self.active_main_keybind_id}")
        
        # Update override keybinds
        for keybind_id, keybind in self.override_keybinds.items():
            keybind.is_active = keybind.is_pressed(self.current_keys)
    
    def run_callback(self, keybind_id, is_override=False):
        keybind = (self.override_keybinds.get(keybind_id) if is_override else self.main_keybinds.get(keybind_id))

        # No keybind found, do nothing
        if not keybind:
            if self.debug:
                print(f"Keybind '{keybind_id}' not found")
            return
        
        # If this is an override keybind, but there's no main keybind active, ignore
        if is_override and not self.any_main_keybind_active:
            if self.debug:
                print(f"Override keybind '{keybind_id}' ignored because no main keybind is active")
            return

        # If this is an override keybind and there's a main thread running
        if self.thread_running and is_override and not self.current_thread_is_override:
            if self.debug:
                print(f"Override keybind '{keybind_id}' requested - cancelling current thread and queueing override")
            self.current_context.cancel()
            self.override_queued = True
            self.queued_override_id = keybind_id
            return
        
        with self.action_lock:
            # If there's a thread running, ignore
            if self.thread_running:
                if self.debug:
                    print(f"Thread already running, ignoring '{keybind_id}'")
                return
            
            self.thread_running = True
            self.current_thread_is_override = is_override


            # If this is a main keybind, store the ID
            if not is_override:
                self.triggering_main_keybind_id = keybind_id
            
            self.current_context.reset()
            self.current_context.set_keybind_id(keybind_id)
        
        def thread_wrapper():
            try:
                keybind.callback(self.current_context)
            except Exception as e:
                print(f"Error in keybind callback for '{keybind_id}': {e}")
            finally:
                with self.action_lock:
                    was_running = self.thread_running
                    was_override = self.current_thread_is_override
                    queued_id = getattr(self, "queued_override_id", None)
                    self.thread_running = False
                    self.current_thread_is_override = False

                    if not is_override:
                        self.triggering_main_keybind_id = None
                    
                if self.debug:
                    print(f"Callback thread completed for '{keybind_id}'")

                # If this was a main thread and there's a queued override, run it
                # only if the keybind associated with the main thread is still active
                if (not is_override and self.override_queued and was_running and 
                    queued_id and self.active_main_keybind_id == self.current_context.keybind_id):
                    
                    if self.debug:
                        print(f"Running queued override '{queued_id}'")
                    
                    self.override_queued = False
                    self.run_callback(queued_id, True)  # is_override=True
                    
                # If this was a main thread and there's a queued override, but the main keybind is no longer active, cancel the queue
                elif not is_override and self.override_queued and not self.main_keybinds[self.current_context.keybind_id].is_active:
                    if self.debug:
                        print(f"Cancelling queued override because no main keybind is active")
                    self.override_queued = False
                    
        self.action_thread = threading.Thread(target=thread_wrapper)
        self.action_thread.daemon = True  # Make thread a daemon so it doesn't block program exit
        self.action_thread.start()
        
        if self.debug:
            print(f"Started thread for '{keybind_id}'")
    
    def win32_event_filter(self, msg, data):
        old_keys = self.current_keys.copy()

        # Log all events to track what's happening
        if self.debug:
            print(f"Event: msg={msg}, scanCode={data.scanCode}, keys={self.current_keys}")

        if msg == 256:  # Key down
            self.current_keys.add(data.scanCode)
        elif msg == 257:  # Key up
            self.current_keys.discard(data.scanCode)
        
        # Process key state changes regardless of whether we handle callbacks
        if old_keys != self.current_keys:
            self.update_keybind_states()

        # Handle callbacks separately - this is important!
        if msg == 256:  # Key down only
            # Try running override callbacks - and suppress them from reaching the game
            # ONLY if a main thread is running
            for keybind_id, keybind in self.override_keybinds.items():
                if keybind.is_active and self.any_main_keybind_active:
                    if self.thread_running and not self.current_thread_is_override:
                        # Main thread is running, suppress this key and queue the override
                        if self.debug:
                            print(f'Main thread running - suppressing override key {keybind_id} and queueing it')
                        self.run_callback(keybind_id, is_override=True)
                        self.listener.suppress_event()
                    else:
                        # No main thread running, let the key through and run the override
                        if self.debug:
                            print(f'No main thread running - allowing override key {keybind_id} through')
                        self.run_callback(keybind_id, is_override=True)
                        return None  # Let the key through
            
            # Try running main callbacks - don't suppress
            for keybind_id, keybind in self.main_keybinds.items():
                if keybind.is_active:
                    if self.debug:
                        print(f'Running main callback for {keybind_id}')
                    self.run_callback(keybind_id)
                    return None  # Don't suppress
        
        # Always return None to avoid suppressing the key
        return None
    
    def on_press(self, key):
        # Do nothing
        pass
    
    def on_release(self, key):
        # Do nothing
        pass

    def start(self):
        self.listener.start()
        if self.debug:
            print("Keyboard listener started")
    
    def stop(self):
        if self.listener:
            self.listener.stop()
            if self.debug:
                print("Keyboard listener stopped")
        
        # Cancel any running actions
        self.current_context.cancel()
        self.override_queued = False
        
        # Wait for any running thread to complete
        if self.action_thread and self.action_thread.is_alive():
            if self.debug:
                print("Waiting for action thread to complete...")
            self.action_thread.join(timeout=1.0)
            if self.debug:
                print("Action thread completed or timed out")
