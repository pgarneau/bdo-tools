import pygetwindow
import threading
import time
import mouse
import pynput

def block_mouse(listener):
    listener.start()
    time.sleep(0.2)
    listener.stop()
def camera_180():
    mouse_listener = pynput.mouse.Listener(suppress=True)
    thread = threading.Thread(target=block_mouse, args=[mouse_listener])
    thread.start()
    max_x = 2545
    total = 2513
    x1, y = mouse.get_position()
    delta_x1 = max_x - x1
    mouse.move(delta_x1, 0, False, 0.1)
    mouse.move(total-delta_x1, 0, False, 0.1)

def camera_point_down():
    _, y = mouse.get_position()
    mouse.move(0, 1430, False, 0.1)

    return y
