"""
Driver script to read from a Rainforest Automation RAVEN smart meter
interface and push the data to the weMonitor Rainforest API.

SYNOPSIS:
    nohup python we_monitor_driver.py mac_id
"""

import sys
import time

import commands
import echo
import usbio
import we_monitor_writer
import xml_fragment_collector

def usage(argv):
    sys.exit("USAGE:\n    python " + argv[0] + " device_mac_id\n")

if len(sys.argv) != 2:
    usage(sys.argv)

# RAINFOREST_MAC_ID = "0x00158d00001AB152"
rainforest_mac_id = sys.argv[1]

# Allocate an element that broadcasts raw Rainforest packets
usb = usbio.USBIO()

# Allocate an element that collects bits of XML until a complete XML
# fragment (<tag>...</tag>) has been assembled.  Then broadcast the
# fragment as a single message to its listeners.
xfc = xml_fragment_collector.XMLFragmentCollector()

# Allocate an element that POSTs XML fragments to the weMonitor 
# Rainforest API
wmw = we_monitor_writer.WeMonitorWriter(rainforest_mac_id)

# For debugging, allocate an element that simply echos its input
# to stdout.
ech = echo.Echo()

# String the elements together and start the reader thread.
usb.attach(xfc).attach(wmw).attach(ech)

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
