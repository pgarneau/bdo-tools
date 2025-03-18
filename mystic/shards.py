from common.spell import Spell
from common.vision import find_shards
from common.windowcapture import wincap

class Shards(Spell):
    def count_shards(self, debug=None):
        # Must know the empty shard location first
        if self.shared_data.location:
            screenshot = wincap.get_screenshot(*self.shared_data.location)
            return find_shards(screenshot, debug=debug)
        else:
            self.ready()
            return 0
