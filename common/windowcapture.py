import numpy as np
import cv2 as cv
import win32gui, win32ui, win32con, win32api
from threading import Thread, Lock
from .vision import Vision
import keyboard
import mouse
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
        
        # Initialize region storage
        self.regions = {}
        self.buff_location = None
        self.skill_log_location = None
        self.target_debuffs_location = None
        self.bsr_location = None  # Add this line for BSR location

        # find the handle for the window we want to capture
        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(window_name))
    
    def initialize_regions(self):
        """Initialize regions from config"""
        try:
            # Import locally to avoid circular import
            from .config_manager import config_manager
            return config_manager.initialize_window_regions(self)
        except ImportError:
            print("WARNING: Could not load config_manager. UI regions not initialized.")
            return {}
    
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
        """Get screenshot of buffs region"""
        try:
            # First try to use configured region
            if hasattr(self, 'regions') and self.regions and "buffs" in self.regions:
                x, y, w, h = self.regions["buffs"]
                self.buff_location = (x, y)
                return self.get_screenshot(x, y, w, h)
        except (AttributeError, KeyError, ValueError):
            pass
            
        # Fall back to old approach
        if not self.buff_location:
            full_screen_ss = self.get_screenshot_fullscreen()
            for vision in [self.simple_cron, self.exquisite_cron, self.alch_stone_vision]:
                coords = vision.find(full_screen_ss)
                if len(coords) > 0 and len(coords[0]) > 2:
                    self.buff_location = coords[0][0] - 100, coords[0][1] - 65
                    
                    # Update regions dict if it exists
                    if hasattr(self, 'regions'):
                        self.regions["buffs"] = (self.buff_location[0], self.buff_location[1], 700, 60)
                        
                    # Try to update config
                    try:
                        from .config_manager import config_manager
                        config_manager.set("ui_regions.buffs", (self.buff_location[0], self.buff_location[1], 700, 60))
                    except ImportError:
                        pass
                    
                    break
        
        w = 700
        h = 60
        
        if not self.buff_location:
            return self.get_screenshot_fullscreen()
            
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
    
    def get_skill_log(self):
        """Get screenshot of skill log region"""
        try:
            # First try to use configured region
            if hasattr(self, 'regions') and self.regions and "skill_log" in self.regions:
                x, y, w, h = self.regions["skill_log"]
                self.skill_log_location = (x, y)
                return self.get_screenshot(x, y, w, h)
        except (AttributeError, KeyError, ValueError):
            pass
            
        # Fall back to old approach
        if not self.skill_log_location:
            return self.get_screenshot_fullscreen()
        
        w = 200
        h = 150
        return self.get_screenshot(self.skill_log_location[0], self.skill_log_location[1], w, h)
    
    def get_region(self, region_name):
        """
        Get a region from the configured regions
        
        Args:
            region_name: Name of the region
            
        Returns:
            (x, y, w, h) tuple or None if not found
            
        Raises:
            ValueError: If region is requested but not configured
        """
        if region_name in self.regions:
            return self.regions[region_name]
        
        # If regions dict exists but doesn't have this region
        if hasattr(self, 'regions') and self.regions is not None:
            raise ValueError(f"Region '{region_name}' is not configured")
            
        # Regions dict doesn't exist yet - try to initialize
        self.initialize_regions()
            
        # Check again after initialization
        if region_name in self.regions:
            return self.regions[region_name]
        else:
            raise ValueError(f"Region '{region_name}' is not configured")

    def get_debuffs(self):
        """Get screenshot of target debuffs region"""
        try:
            # Try to use configured region
            if hasattr(self, 'regions') and self.regions and "target_debuffs" in self.regions:
                x, y, w, h = self.regions["target_debuffs"]
                return self.get_screenshot(x, y, w, h)
        except (AttributeError, KeyError, ValueError):
            pass
            
        # Fall back to default location if not configured
        if hasattr(self, 'target_debuffs_location') and self.target_debuffs_location:
            x, y = self.target_debuffs_location
            return self.get_screenshot(x, y, 400, 50)  # Default size
            
        # Hard-coded fallback
        return self.get_screenshot(1085, 50, 400, 50, scale=True)

    def get_bsr(self):
        """Get screenshot of BSR meter region"""
        try:
            # Try to use configured region
            if hasattr(self, 'regions') and self.regions and "bsr_location" in self.regions:
                x, y, w, h = self.regions["bsr_location"]
                self.bsr_location = (x, y)
                return self.get_screenshot(x, y, w, h)
        except (AttributeError, KeyError, ValueError):
            pass
            
        # Fall back to default location if not configured
        if hasattr(self, 'bsr_location') and self.bsr_location:
            x, y = self.bsr_location
            return self.get_screenshot(x, y, 80, 80)  # Default size
            
        # Hard-coded fallback
        return self.get_screenshot(1280, 700, 80, 80)

# Create singleton instance
wincap = WindowCapture()
# Initialize regions from config
wincap.initialize_regions()