"""
Driver script to read from a Rainforest Automation RAVEN smart meter
interface and push the data to the weMonitor Rainforest API.

SYNOPSIS:
    nohup python we_monitor_script.py
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
usb.update(usb, commands.initialize())

# Start the reader thread
usb.start()
# Send a GET_DEVICE_INFO message to get a DeviceInfo response.
time.sleep(1)
usb.update(usb, commands.get_device_info())

# Should never get here...
usb.thread.join()
