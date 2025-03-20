import json
import os
import cv2 as cv
import numpy as np
import time
import pygetwindow

class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.init()
        return cls._instance
    
    def init(self):
        """Initialize the configuration manager"""
        self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.json')
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from file or create default if not exists"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                print(f"Error loading config file. Creating a new one.")
                return self.create_default_config()
        else:
            return self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration"""
        default_config = {
            "ui_regions": {
                "skill_log": None,
                "buffs": None,
            },
        }
        self.save_config(default_config)
        return default_config
    
    def save_config(self, config=None):
        """Save configuration to file"""
        if config is None:
            config = self.config
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
    
    def get(self, key, default=None):
        """Get a configuration value by key with dot notation"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key, value):
        """Set a configuration value by key with dot notation"""
        keys = key.split('.')
        current = self.config
        
        # Navigate to the right nested dict
        for i, k in enumerate(keys[:-1]):
            if k not in current or not isinstance(current[k], dict):
                current[k] = {}
            current = current[k]
        
        # Set the value
        current[keys[-1]] = value
        
        # Save the updated config
        self.save_config()
    
    def select_region(self, region_name, wincap, default_dimensions=None):
        """
        Let user select a region on screen
        
        Args:
            region_name: Human-readable name of the region
            wincap: WindowCapture instance
            default_dimensions: (w, h) to use if defined
            
        Returns:
            (x, y, w, h) coordinates of the region or None if canceled
        """
        # Take a screenshot of the game window
        screenshot = wincap.get_screenshot_fullscreen()
        
        # Create a copy for drawing
        img_draw = screenshot.copy()
        
        # Initial message
        cv.putText(img_draw, f"Select {region_name} region", (20, 30), 
                   cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv.putText(img_draw, "Click and drag to select, Enter to confirm, Esc to cancel", 
                  (20, 70), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Track selection state
        selection = {'start_x': 0, 'start_y': 0, 'end_x': 0, 'end_y': 0, 'selecting': False, 'complete': False}
        
        def mouse_events(event, x, y, flags, param):
            if event == cv.EVENT_LBUTTONDOWN:
                selection['start_x'] = x
                selection['start_y'] = y
                selection['selecting'] = True
                selection['complete'] = False
                
            elif event == cv.EVENT_MOUSEMOVE and selection['selecting']:
                # Create a fresh copy of the screenshot
                img_temp = screenshot.copy()
                
                # Draw helpful text
                cv.putText(img_temp, f"Select {region_name} region", (20, 30), 
                           cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                          
                # Draw the current selection rectangle
                cv.rectangle(img_temp, (selection['start_x'], selection['start_y']), 
                             (x, y), (0, 255, 0), 2)
                
                # Show dimensions
                w = abs(x - selection['start_x'])
                h = abs(y - selection['start_y'])
                cv.putText(img_temp, f"Size: {w}x{h}", 
                          (min(x, selection['start_x']), min(y, selection['start_y']) - 10), 
                          cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
                
                # Show the image with rectangle
                cv.imshow(f'Select {region_name} region', img_temp)
                
            elif event == cv.EVENT_LBUTTONUP:
                selection['end_x'] = x
                selection['end_y'] = y
                selection['selecting'] = False
                selection['complete'] = True
                
                # Create a fresh copy of the screenshot
                img_temp = screenshot.copy()
                
                # Determine rectangle coordinates
                x1 = min(selection['start_x'], selection['end_x'])
                y1 = min(selection['start_y'], selection['end_y'])
                x2 = max(selection['start_x'], selection['end_x'])
                y2 = max(selection['start_y'], selection['end_y'])
                
                # Draw the current selection rectangle
                cv.rectangle(img_temp, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Show dimensions
                w = x2 - x1
                h = y2 - y1
                cv.putText(img_temp, f"Size: {w}x{h} - Press Enter to confirm", 
                          (x1, y1 - 10), 
                          cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
                
                # Show the image with rectangle
                cv.imshow(f'Select {region_name} region', img_temp)
        
        # Create window and set mouse callback
        cv.namedWindow(f'Select {region_name} region', cv.WINDOW_NORMAL)
        cv.setMouseCallback(f'Select {region_name} region', mouse_events)
        
        # Show initial image with instructions
        cv.imshow(f'Select {region_name} region', img_draw)
        
        # If default dimensions are provided and no selection is made yet,
        # show a suggested region in the center
        if default_dimensions and not selection['complete']:
            default_w, default_h = default_dimensions
            center_x = screenshot.shape[1] // 2
            center_y = screenshot.shape[0] // 2
            
            x1 = center_x - default_w // 2
            y1 = center_y - default_h // 2
            x2 = x1 + default_w
            y2 = y1 + default_h
            
            img_temp = screenshot.copy()
            
            # Change from cyan (0, 255, 255) to bright magenta (255, 0, 255)
            suggested_color = (255, 0, 255)  # Bright magenta in BGR
            
            cv.putText(img_temp, f"Suggested {region_name} region", (20, 30), 
                       cv.FONT_HERSHEY_SIMPLEX, 1, suggested_color, 2)
            cv.putText(img_temp, "Click and drag to select your own, or press Enter to use this one", 
                      (20, 70), cv.FONT_HERSHEY_SIMPLEX, 0.7, suggested_color, 2)
            
            cv.rectangle(img_temp, (x1, y1), (x2, y2), suggested_color, 2)
            cv.putText(img_temp, f"Size: {default_w}x{default_h}", 
                      (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.6, suggested_color, 1)
            
            cv.imshow(f'Select {region_name} region', img_temp)
            
            # Set the selection to the default values
            selection['start_x'] = x1
            selection['start_y'] = y1
            selection['end_x'] = x2
            selection['end_y'] = y2
            selection['complete'] = True
        
        # Wait for key or selection
        while True:
            key = cv.waitKey(10)
            
            # Enter key confirms selection
            if key == 13 and selection['complete']:
                x = min(selection['start_x'], selection['end_x'])
                y = min(selection['start_y'], selection['end_y'])
                w = abs(selection['end_x'] - selection['start_x'])
                h = abs(selection['end_y'] - selection['start_y'])
                
                cv.destroyAllWindows()
                return (x, y, w, h)
            
            # Escape key cancels
            elif key == 27:
                cv.destroyAllWindows()
                return None

    def configure_missing_regions(self, wincap, required_regions=None, force_config=False):
        """
        Configure all missing regions in the config file
        
        Args:
            wincap: WindowCapture instance to use for screenshots
            required_regions: List of regions that must be configured
                              If None, configures all regions in the default config
            force_config: If True, reconfigures all regions even if they exist
        
        Returns:
            True if all required regions are configured, False otherwise
        """
        # Default to all regions in the default config if none specified
        if required_regions is None:
            required_regions = list(self.create_default_config()["ui_regions"].keys())
        
        print(f"Checking configuration for regions: {', '.join(required_regions)}")
        
        # Default dimensions for different regions
        default_dimensions = {
            "skill_log": (200, 150),
            "buffs": (300, 50),
        }
        
        # Configure each required region
        all_configured = True
        for region in required_regions:
            region_config = self.get(f"ui_regions.{region}")
            
            if force_config or region_config is None:
                print(f"\nRegion '{region}' needs configuration.")
                
                # Get default dimensions if available
                dimensions = default_dimensions.get(region, (150, 150))
                
                # Ask user to select the region
                region_coords = self.select_region(region, wincap, default_dimensions=dimensions)
                
                if region_coords:
                    # Save the region configuration
                    self.set(f"ui_regions.{region}", region_coords)
                    print(f"Region '{region}' configured: {region_coords}")
                else:
                    # User canceled configuration
                    print(f"WARNING: Region '{region}' configuration was canceled.")
                    all_configured = False
        
        return all_configured

    def verify_regions(self, wincap, regions=None):
        """
        Show all configured regions for verification
        
        Args:
            wincap: WindowCapture instance
            regions: List of regions to verify (defaults to all configured regions)
        """
        # Get a full screenshot
        screenshot = wincap.get_screenshot_fullscreen()
        display_img = screenshot.copy()
        
        # Updated colors for different regions (BGR format)
        colors = {
            "skill_log": (0, 255, 0),      # Green 
            "buffs": (0, 0, 255),          # Pure Red (was Blue in your code)
        }
        
        # Default to all regions if none specified
        if regions is None:
            regions = self.config.get("ui_regions", {}).keys()
        
        # Draw each configured region
        configured_count = 0
        for region_name in regions:
            region = self.get(f"ui_regions.{region_name}")
            if region:
                x, y, w, h = region
                color = colors.get(region_name, (255, 255, 255))
                
                # Make the rectangle thicker for better visibility
                cv.rectangle(display_img, (x, y), (x+w, y+h), color, 3)  # Increased thickness from 2 to 3
                
                # Add a black outline to text for better visibility against any background
                text_pos = (x, y-10)
                cv.putText(display_img, region_name, (text_pos[0]+1, text_pos[1]+1), 
                          cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 3)  # Black shadow
                cv.putText(display_img, region_name, text_pos, 
                          cv.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                
                configured_count += 1
        
        # Show the image if any regions were drawn
        if configured_count > 0:
            cv.namedWindow("Configured Regions", cv.WINDOW_NORMAL)
            cv.imshow("Configured Regions", display_img)
            print(f"Showing {configured_count} configured regions. Press any key to continue.")
            cv.waitKey(0)
            cv.destroyAllWindows()
        else:
            print("No configured regions to display.")

    def initialize_window_regions(self, window_capture):
        """
        Initialize window regions from config
        
        Args:
            window_capture: WindowCapture instance to initialize
            
        Returns:
            Dict of initialized regions
        """
        # Get UI regions from config
        ui_regions = self.get("ui_regions", {})
        initialized_regions = {}
        
        # Initialize each region if it exists in config
        for region_name, coords in ui_regions.items():
            if coords is not None:
                initialized_regions[region_name] = coords
                
                # Update specific locations for backward compatibility
                if region_name == "skill_log":
                    window_capture.skill_log_location = (coords[0], coords[1])
                elif region_name == "buffs":
                    window_capture.buff_location = (coords[0], coords[1])
        
        # Store the regions in the window_capture instance
        window_capture.regions = initialized_regions
        
        if initialized_regions:
            print(f"Initialized {len(initialized_regions)} UI regions from config")
        
        return initialized_regions
        
    def ensure_regions_configured(self):
        """
        Ensure all required regions are configured, configuring them if needed
        
        Returns:
            True if all regions configured, False otherwise
        """
        # Import here to avoid circular imports
        from .windowcapture import wincap
        
        # Check if config file exists and has regions configured
        required_regions = ["skill_log", "buffs"]
        missing_regions = []
        
        # Check which regions are missing
        for region in required_regions:
            if not self.get(f"ui_regions.{region}"):
                missing_regions.append(region)
        
        # If we have missing regions, configure them
        if missing_regions:
            print(f"Missing configuration for regions: {', '.join(missing_regions)}")
            print("Please select the regions on your screen...")
            
            # Configure each missing region
            for region in missing_regions:
                print(f"\nConfiguring {region} region...")
                
                # Default dimensions by region type
                if region == "skill_log":
                    dimensions = (200, 150)
                elif region == "buffs":
                    dimensions = (700, 60)
                else:
                    dimensions = (200, 200)
                
                # Let user select the region
                region_coords = self.select_region(region, wincap, default_dimensions=dimensions)
                
                if region_coords:
                    self.set(f"ui_regions.{region}", region_coords)
                    print(f"{region} region configured: {region_coords}")
                else:
                    print(f"WARNING: {region} configuration was canceled.")
                    # Use default coordinates if user cancels
                    if region == "skill_log":
                        self.set(f"ui_regions.{region}", (1200, 700, 200, 150))
                    elif region == "buffs":
                        self.set(f"ui_regions.{region}", (1085, 50, 700, 60))
        
        # Initialize WindowCapture with the configuration
        regions = self.initialize_window_regions(wincap)
        
        # Check if all required regions are configured
        all_configured = all(self.get(f"ui_regions.{region}") for region in required_regions)
        
        if all_configured:
            print(f"All {len(required_regions)} required regions are configured.")
        else:
            print(f"WARNING: Some required regions are not configured.")
        
        return all_configured

# Create a singleton instance
config_manager = ConfigManager()

# Decorator to check if BDO is selected
def bdo_selected(func):
    def wrapper(*args, **kwargs):
        current_window = pygetwindow.getActiveWindow()

        if current_window:
            current_title = current_window.title.lower()
            if current_title and "black desert" in current_title:
                return func(*args, **kwargs)
        
        print("Black Desert is not the active window")
        return False
    
    return wrapper

@bdo_selected
def init_spells(spell_instances):
    """
    Initialize spell templates by checking if they're ready
    
    Args:
        spell_instances: List of Spell instances to initialize
        
    Returns:
        True if initialization successful, False otherwise
    """
    from .windowcapture import wincap
    try:
        screenshot = wincap.get_skills()
        for spell in spell_instances:
            spell.ready(screenshot)
        
        print("Spells Initiated")
        return True
    except Exception as e:
        print(f"Error initializing spells: {e}")
        return False

def _initialize_configuration_internal():
    """
    Internal function to initialize configuration 
    Only runs when BDO is active
    
    Returns:
        True if configuration successful, False otherwise
    """
    if is_bdo_active():
        return config_manager.ensure_regions_configured()
    return False

def initialize_configuration(wait_for_bdo=True, max_wait_seconds=60):
    """
    Initialize configuration - waits for BDO to be active if needed
    
    Args:
        wait_for_bdo: Whether to wait for BDO to become active
        max_wait_seconds: Maximum seconds to wait (0 for infinite)
        
    Returns:
        True if configuration successful, False otherwise
    """
    # Check if config exists and has required regions
    required_regions = ["skill_log", "buffs"]
    all_configured = all(config_manager.get(f"ui_regions.{region}") for region in required_regions)
    
    # If already configured, initialize silently
    if all_configured:
        from .windowcapture import wincap
        config_manager.initialize_window_regions(wincap)
        return True
    
    # If not configured, we need BDO to be active
    if not is_bdo_active():
        if wait_for_bdo:
            # Wait for BDO to become active
            if not wait_for_bdo_active(max_wait_seconds):
                print("Could not initialize configuration: Black Desert is not active.")
                return False
        else:
            print("Black Desert is not active. Configuration cannot be initialized.")
            return False
    
    # Now that BDO is active, run the initialization
    return _initialize_configuration_internal()

# Add this to the bottom of your config_manager.py file
import time

def is_bdo_active():
    """
    Check if BDO is the active window
    
    Returns:
        True if BDO is active, False otherwise
    """
    current_window = pygetwindow.getActiveWindow()
    if current_window:
        current_title = current_window.title.lower()
        return current_title and "black desert" in current_title
    return False

def wait_for_bdo_active(max_wait_seconds=60, check_interval=1.0):
    """
    Wait for BDO to become the active window
    
    Args:
        max_wait_seconds: Maximum time to wait in seconds (0 for infinite)
        check_interval: How often to check in seconds
        
    Returns:
        True if BDO became active, False if timeout occurred
    """
    print("Waiting for Black Desert window to become active...")
    
    start_time = time.time()
    while max_wait_seconds == 0 or (time.time() - start_time) < max_wait_seconds:
        if is_bdo_active():
            print("Black Desert window is now active!")
            return True
            
        # Show periodic reminder
        elapsed = int(time.time() - start_time)
        if elapsed % 5 == 0:  # Show message every 5 seconds
            if max_wait_seconds > 0:
                remaining = max_wait_seconds - elapsed
                print(f"Waiting for Black Desert window... ({remaining}s remaining)")
            else:
                print(f"Waiting for Black Desert window... ({elapsed}s elapsed)")
                
        time.sleep(check_interval)
    
    print(f"Timeout after {max_wait_seconds} seconds waiting for Black Desert window.")
    return False