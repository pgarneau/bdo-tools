from spell import Spell, default_speed_function
from vision import Vision, find_shards
import cv2

class Shards(Spell):
    def count_shards(self, debug=None):
        # Must know the empty shard location first
        if self.location:
            screenshot = self.wincap.get_screenshot(*self.location)
            return find_shards(screenshot, debug=debug)
        else:
            self.ready()
            return 0
