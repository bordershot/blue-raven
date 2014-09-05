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
Driver script to read from a Rainforest Automation RAVEN smart meter
interface and push the data to the weMonitor Rainforest API.

SYNOPSIS:
    PYTHONPATH=./lib nohup python scripts/we_monitor_script.py &
"""

import sys
import time

import commands
import echo
import usbio
import we_monitor_formatter
import we_monitor_writer
import xml_fragment_collector

def usage(argv):
    sys.exit("USAGE:\n    python " + sys.argv[0] + "\n")

if len(sys.argv) != 1:
    usage(sys.argv)

# Allocate an element that broadcasts raw Rainforest packets
usb = usbio.USBIO()

# Allocate an element that collects bits of XML until a complete XML
# fragment (<tag>...</tag>) has been assembled.  Then broadcast the
# fragment as a single message to its listeners.
xfc = xml_fragment_collector.XMLFragmentCollector()

# Wrap the XML fragments in a format understood by the weMonitor API
wmf = we_monitor_formatter.WeMonitorFormatter()

# Allocate an element that POSTs XML fragments to the weMonitor 
# Rainforest API
wmw = we_monitor_writer.WeMonitorWriter()

# For debugging, allocate an element that simply echos its input
# to stdout.
ech = echo.Echo()

# String the elements together and start the reader thread.
usb.attach(xfc).attach(wmf).attach(wmw).attach(ech)

# If you prefer to see the raw XML as it arrives from the USB
# device. comment out the above line and uncomment this line.
# usb.attach(xfc).attach(ech).attach(wmf).attach(wmw)

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
