import numpy as np
import cv2 as cv
import win32gui, win32ui, win32con, win32api
from threading import Thread, Lock
from .vision import Vision
import os

class WindowCapture:
    # Base resolution that coordinates are designed for
    BASE_WIDTH = 2560  # 1440p monitor width
    BASE_HEIGHT = 1440  # 1440p monitor height

    # threading properties
    stopped = True
    lock = None
    screenshot = None
    # properties
    hwnd = None
    screen_width = 0
    screen_height = 0

    # constructor
    def __init__(self, window_name=None):
        self.lock = Lock()
        
        # Get current screen dimensions
        self.screen_width = win32api.GetSystemMetrics(0)
        self.screen_height = win32api.GetSystemMetrics(1)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.alch_stone_vision = Vision('alch_stone', base_path=os.path.join(current_dir, 'spells'))
        self.simple_cron = Vision('simple_cron_meal', base_path=os.path.join(current_dir, 'spells'))
        self.exquisite_cron = Vision('exquisite_cron_meal', base_path=os.path.join(current_dir, 'spells'))
        self.buff_location = None

        # find the handle for the window we want to capture
        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(window_name))
    
    def get_screenshot(self, x, y, w, h, scale=False):
        # Scale coordinates based on current screen resolution
        if scale:
            x = int(x * (self.screen_width / self.BASE_WIDTH))
            y = int(y * (self.screen_height / self.BASE_HEIGHT))
        
        # get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (w, h), dcObj, (x, y), win32con.SRCCOPY)

        # convert the raw data into a format opencv can read
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (h, w, 4)

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # drop the alpha channel
        img = img[...,:3]

        # make image C_CONTIGUOUS
        return np.ascontiguousarray(img)
    
    def get_screenshot_fullscreen(self):
        """Get a screenshot of the entire screen without scaling"""
        x = 0
        y = 0
        w = self.screen_width
        h = self.screen_height
        
        # get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (w, h), dcObj, (x, y), win32con.SRCCOPY)

        # convert the raw data into a format opencv can read
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (h, w, 4)

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # drop the alpha channel
        img = img[...,:3]

        # make image C_CONTIGUOUS
        return np.ascontiguousarray(img)
    
    def get_accel(self):
        w = 80
        h = 80
        x = 1110
        y = 960
        
        img = self.get_screenshot(x, y, w, h)

        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        lower_yellow = np.array([25, 100, 100])
        upper_yellow = np.array([26, 255, 255])
        mask = cv.inRange(hsv, lower_yellow, upper_yellow)
        isolated = cv.bitwise_and(img, img, mask=mask)

        return isolated
    
    def get_buffs(self):
        if not self.buff_location:
            full_screen_ss = self.get_screenshot_fullscreen()
            for vision in [self.simple_cron, self.exquisite_cron, self.alch_stone_vision]:
                coords = vision.find(full_screen_ss)
                if len(coords) > 0 and len(coords[0]) > 2:
                    self.buff_location = coords[0][0] - 100, coords[0][1] - 65
                    break
        
        w = 700
        h = 60
        # cv.imshow('gay', self.get_screenshot(self.buff_location[0], self.buff_location[1], w, h))
        # cv.waitKey(0)
        # print(self.buff_location)
        # x = 470
        # y = 1070
        
        return self.get_screenshot(self.buff_location[0], self.buff_location[1], w, h)

    def get_skills(self):
        # Use the fullscreen method for this one since it already uses system metrics
        return self.get_screenshot_fullscreen()
    
    def get_nearby_targets(self):
        x = 830
        y = 270
        w = 900
        h = 900

        img = self.get_screenshot(x, y, w, h, scale=True)

        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        lower_yellow = np.array([22, 100, 100])
        upper_yellow = np.array([26, 255, 255])
        mask = cv.inRange(hsv, lower_yellow, upper_yellow)
        isolated = cv.bitwise_and(img, img, mask=mask)

        gray = cv.cvtColor(isolated, cv.COLOR_BGR2GRAY)

        return cv.GaussianBlur(gray, (5, 5), 0)
    
    def get_debuffs(self):
        x = 1085
        y = 50
        w = 400
        h = 50

        return self.get_screenshot(x, y, w, h, scale=True)
    
    def get_defense_icon(self):
        x = 1343
        y = 550
        w = 74
        h = 200

        return self.get_screenshot(x, y, w, h, scale=True)
    
    def get_hunting_crosshair(self):
        x = 1215
        y = 650
        w = 140
        h = 140

        return self.get_screenshot(x, y, w, h, scale=True)

    def get_reloader(self):
        x = 1200
        y = 1120
        w = 180
        h = 200

        return self.get_screenshot(x, y, w, h, scale=True)




    # find the name of the window you're interested in.
    # once you have it, update window_capture()
    # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the __init__ constructor.
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)
    
    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        while not self.stopped:
            # get an updated image of the game
            screenshot = self.get_screenshot()
            # lock the thread while updating the results
            self.lock.acquire()
            self.screenshot = screenshot
            self.lock.release()

wincap = WindowCapture()