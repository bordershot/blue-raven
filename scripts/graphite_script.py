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
    PYTHONPATH=./lib nohup python scripts/graphite_script.py &
"""

import sys
import time
import syslog

import commands
import echo
import raven_fragment_collector
import raven_utilities
import usbio
import graphiteclient

def usage(argv):
    sys.exit("USAGE:\n    python " + sys.argv[0] + "\n")

def toplevel():
    # configure syslog
    syslog.openlog(ident="blue-raven", logoption=syslog.LOG_PID)
    syslog.syslog(syslog.LOG_INFO, 'starting up')

    # Allocate an element that broadcasts raw Rainforest packets
    usb = usbio.USBIO()
    
    # Allocate an element that collects bits of XML until a complete XML
    # fragment (<tag>...</tag>) has been assembled.  Then broadcast the
    # fragment as a single message to its listeners.
    rfc = raven_fragment_collector.RavenFragmentCollector()
    graphite = graphiteclient.upload_to_graphite()
    usb.attach(rfc).attach(graphite)

    # For debugging, allocate an element that simply echos its input
    # to stdout.
    # ech = echo.Echo()
    
    # Sending an 'initialize' message causes the RAVEn to synchronize its
    # XML output -- without that, it sends an arbitrary number of partial
    # packets and lots of nulls.  (The initialize message also elicits an
    # "Unknown command" response, but that appears to be benign.)
    usb.update(commands.initialize())
    
    # Start the reader thread
    syslog.syslog(syslog.LOG_INFO, 'launching reader thread')
    usb.start()
    # Send a GET_DEVICE_INFO message to get a DeviceInfo response.
    while True:
        time.sleep(1)
        usb.update(commands.get_current_summation_delivered())
        time.sleep(1)
        usb.update(commands.get_instantaneous_demand())
        time.sleep(1)
        usb.update(commands.get_current_period_usage())
        time.sleep(30)
    
    # Should never get here...
    usb.thread.join()

if len(sys.argv) != 1:
    usage(sys.argv)

# here's where it all really starts...
with raven_utilities.exceptions_logged():
    toplevel()


