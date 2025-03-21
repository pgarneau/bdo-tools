import pygetwindow

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

class Variables:
    def __init__(self, *args):
        self._variables = {}
        for var in args:
            self._variables[var] = 0

    def __getattr__(self, name):
        if name in self._variables:
            return self._variables[name]
        raise AttributeError(f"'Variables' object has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        # Protection
        if name == "_variables":
            super().__setattr__(name, value)
        else:
            self._variables[name] = value