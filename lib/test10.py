import usbio
import xml_fragment_collector
import we_monitor_writer
import echo
import skipper

print """testing usb, xml_fragment_collector, we_monitor_writer"""

# Allocate an element that broadcasts raw Rainforest packets
usb = usbio.USBIO()

# Allocate an element that skips initial packets.  We do this because
# the USB driver wakes up in a strange state and emits incomplete
# fragments peppered with nulls.  After an indeterminate number of
# packets, everything appears to get straightened out.
#
# TODO: Since the number of bad packets is really indeterminate, 
# figure out a better heuristic for knowning which packets to skip.
skp = skipper.Skipper(40)

# Allocate an element that collects bits of XML until a complete XML
# fragment (<tag>...</tag>) has been collected.  Then broadcast the
# fragment as a single message to its listeners.
xfc = xml_fragment_collector.XMLFragmentCollector()

# Allocate an element that POSTs XML fragments to the weMonitor 
# Rainforest API
wmw = we_monitor_writer.WeMonitorWriter("0x00158d00001AB152")

# For debugging, allocate an element that simply echos its input
# to stdout.
ech = echo.Echo()

# String the elements together and start the reader thread.
usb.attach(skp).attach(xfc).attach(wmw).attach(ech)
usb.start()
usb.thread.join()

