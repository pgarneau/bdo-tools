import time
from common.listener import Listener

def main_action1(context):
    keybind_id = context.get_keybind_id()
    print(f"Main action 1 activated by '{keybind_id}'! Starting long process...")
    print(f"Keep '{keybind_id}' pressed to continue. Release to cancel.")
    # Simulate a long-running process that checks for cancellation
    for i in range(8):
        if context.is_cancelled():
            print(f"Main action 1 was cancelled!")
            return
        print(f"Main action 1 working... {i+1}/8")
        time.sleep(1)
    print("Main action 1 completed successfully!")

def main_action2(context):
    keybind_id = context.get_keybind_id()
    print(f"Main action 2 activated by '{keybind_id}'! Starting alternate process...")
    print(f"Keep '{keybind_id}' pressed to continue. Release to cancel.")
    # Simulate another long-running process
    for i in range(5):
        if context.is_cancelled():
            print(f"Main action 2 was cancelled!")
            return
        print(f"Main action 2 working... {i+1}/5")
        time.sleep(1)
    print("Main action 2 completed successfully!")
    
def override_action1(context):
    keybind_id = context.get_keybind_id()
    print(f"Override action 1 activated by '{keybind_id}'!")
    print("NOTE: Main keybind must remain active during override execution!")
    # Simulate an override process
    for i in range(3):
        if context.is_cancelled():
            print(f"Override action 1 was cancelled!")
            return
        print(f"Override action 1 working... {i+1}/3")
        time.sleep(1)
    print("Override action 1 completed!")

def override_action2(context):
    keybind_id = context.get_keybind_id()
    print(f"Override action 2 activated by '{keybind_id}'!")
    print("NOTE: Main keybind must remain active during override execution!")
    # Simulate another override process
    for i in range(4):
        if context.is_cancelled():
            print(f"Override action 2 was cancelled!")
            return
        print(f"Override action 2 working... {i+1}/4")
        time.sleep(0.8)
    print("Override action 2 completed!")


listener = Listener()
listener.register_keybind('f24', main_action1)
# listener.register_keybind('x', main_action2)
listener.register_keybind('shift+d', override_action1, override=True)
listener.register_keybind('shift+a', override_action2, override=True)
listener.start()

try:
    while True:
        time.sleep(5)
        # pass
except KeyboardInterrupt:
    print("end")
finally:
    listener.stop()