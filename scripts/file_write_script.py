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
interface and capture the raw XML to a file.  This is a useful
debugging tool when used in conjunction with file_reader.py,

SYNOPSIS:
    PYTHONPATH=./lib python file_write_script.py file_name.xml
"""

import sys
import time

import commands
import echo
import file_writer
import usbio

def usage(argv):
    sys.exit("USAGE:\n    python " + sys.argv[0] + " file_name.xml\n")

if len(sys.argv) != 2:
    usage(sys.argv)

# Allocate an element that broadcasts raw Rainforest packets
usb = usbio.USBIO()

print("writing XML output to " + sys.argv[1])

# Allocate an element that collects bits of XML until a complete XML
# fragment (<tag>...</tag>) has been assembled.  Then broadcast the
# fragment as a single message to its listeners.
fw = file_writer.FileWriter(sys.argv[1])

# For debugging, allocate an element that simply echos its input
# to stdout.
ech = echo.Echo()

# String the elements together and start the reader thread.
usb.attach(fw).attach(ech)

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
