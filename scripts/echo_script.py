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

"""
Script to read from a Rainforest Automation RAVEN smart meter
interface and print raw output to stdout.  Sends a get_device_info() 
command to elicit a response even when there's no connection
to a meter.

SYNOPSIS:
    PYTHONPATH=./lib python scripts/echo_script.py [usb_port]
"""

import sys
import time

import commands
import echo
import usbio

def usage(argv):
    sys.exit("USAGE:\n    python " + sys.argv[0] + "[usb_port]\n")

port = "/dev/ttyUSB0"

if len(sys.argv) == 2:
    port = sys.argv[1]
else if len(sys.argv) > 2:
    usage(sys.argv)


# Allocate an element that broadcasts raw Rainforest packets
usb = usbio.USBIO(port)

# For debugging, allocate an element that simply echos its input
# to stdout.
ech = echo.Echo()

# String the elements together and start the reader thread.
usb.attach(ech)

# Sending an 'initialize' message causes the RAVEn to synchronize its
# XML output -- without that, it sends an arbitrary number of partial
# packets and lots of nulls.  (The initialize message also elicits an
# "Unknown command" response, but that appears to be benign.)
usb.update(commands.initialize())

# Start the reader thread
usb.start()

# Send a GET_DEVICE_INFO message to get a DeviceInfo response.
time.sleep(1)
usb.update(commands.get_device_info())

# Should never get here...
usb.thread.join()
