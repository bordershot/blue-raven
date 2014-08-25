"""Send a stop message to an object after N messages have been
received.
"""

from subject import *
from observer import *
import sys

class Stopper(Subject, Observer):

    def __init__(self, obj, n_packets):
        Subject.__init__(self)
        Observer.__init__(self)
        self.obj = obj
        self.n_packets = n_packets

    # support for observer

    # by using 'a' (append) mode, we flush the output after each
    # write, which is probably the preferred behavior.
    def update(self, subject, message):
        if (self.n_packets <= 0):
            self.obj.stop()
        else:
            self.n_packets -= 1
        self.notify(message)
