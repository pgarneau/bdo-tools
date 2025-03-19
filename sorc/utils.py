from common.bind import custom_mouse_handler
import win32api

width, height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

def violation_handler():
    global width, height
    return custom_mouse_handler(width / 2, height * 0.75, 0.23, True, True, 'release')

def imminent_handler():
    global width, height
    return custom_mouse_handler(width / 2, height * 0.75, 0.15, True, True, 'release')

def calamity_handler():
    global width, height
    return custom_mouse_handler(width / 2, height * 0.75, 0.05, True, True, 'hold_and_release_early')