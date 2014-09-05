#   ================================================================
#   Copyright (C) 2014 weMonitor, Inc.
#  
#   Permission is hereby granted, free of charge, to any person obtaining
#   a copy of this software and associated documentation files (the
#   "Software"), to deal in the Software without restriction, including
#   without limitation the rights to use, copy, modify, merge, publish,
#   distribute, sublicense, and/or sell copies of the Software, and to
#   permit persons to whom the Software is furnished to do so, subject to
#   the following conditions:
#  
#   The above copyright notice and this permission notice shall be
#   included in all copies or substantial portions of the Software.
#  
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
#   LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#   OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
#   WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#   ================================================================

from subject import *
from observer import *
import threading
import serial

class USBIO(Subject, Observer):
    """subject / observer interface for a serial USB device: Any
    message received via update() is written to the USB device
    directly.  Any data read from the USB device is broadcast to
    observers.  Note that reads from the USB device happen in a
    separate thread.
    """

    def __init__(self, port="/dev/ttyUSB0", baud=115200):
        Subject.__init__(self)
        Observer.__init__(self)
        self.serial = serial.Serial(port, baud)
        self.thread = None

    # support for observer

    def update(self, message):
        self.serial.write(message)

    # support for threading

    def start(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.thread = None

    # this code runs in a separate thread.
    def run(self):
        while threading.current_thread() == self.thread:
            line = self.serial.readline()
            self.notify(line)
            

