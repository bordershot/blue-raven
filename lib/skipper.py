from subject import *
from observer import *

class Skipper(Subject, Observer):
    """Skip the first N packets received.  Thereafter, forward all
    packets."""

    def __init__(self, packets_to_skip):
        Subject.__init__(self)
        Observer.__init__(self)
        self.packets_to_skip = packets_to_skip

    # support for observer

    def update(self, subject, message):
        if (self.packets_to_skip <= 0):
            self.notify(message)
        else:
            self.packets_to_skip -= 1
            print("skipping: " + message)




