"""
Driver script to read from a Rainforest Automation RAVEN smart meter
interface and push the data to the weMonitor Rainforest API.

SYNOPSIS:
    [1] Edit this file to set the RAINFOREST_MAC_ID
    [2] Invoke the script via 'python we_monitor_driver.py'

TODO: Make the Rainforest Mac ID be a command line argument.
"""

import usbio
import xml_fragment_collector
import we_monitor_writer
import echo
import skipper

RAINFOREST_MAC_ID = "0x00158d00001AB152"

# Allocate an element that broadcasts raw Rainforest packets
usb = usbio.USBIO()

# Allocate an element that skips initial packets.  We do this because
# the USB driver wakes up in a strange state and emits incomplete
# fragments peppered with nulls.  After an indeterminate number of
# packets, everything appears to get straightened out.
#
# TODO: Since the number of bad packets is truly indeterminate, 
# figure out a better heuristic for knowning which packets to skip.
# For example, detecting nulls in strings might work.
skp = skipper.Skipper(40)

# Allocate an element that collects bits of XML until a complete XML
# fragment (<tag>...</tag>) has been assembled.  Then broadcast the
# fragment as a single message to its listeners.
xfc = xml_fragment_collector.XMLFragmentCollector()

# Allocate an element that POSTs XML fragments to the weMonitor 
# Rainforest API
wmw = we_monitor_writer.WeMonitorWriter(RAINFOREST_MAC_ID)

# For debugging, allocate an element that simply echos its input
# to stdout.
ech = echo.Echo()

# String the elements together and start the reader thread.
usb.attach(skp).attach(xfc).attach(wmw).attach(ech)
usb.start()
usb.thread.join()

