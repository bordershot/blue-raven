"""
Script to read XML from a file and process it, doing everything
except sending it to the weMonitor servers.  Useful for debugging.

SYNOPSIS:
    python file_read_script.py file_name.xml
"""

import sys
import time

import commands
import echo
import file_reader
import xml_fragment_collector
import we_monitor_formatter

def usage(argv):
    sys.exit("USAGE:\n    python " + sys.argv[0] + " file_name.xml\n")

if len(sys.argv) != 2:
    usage(sys.argv)

print("reading XML from " + sys.argv[1])

# Allocate an element that collects bits of XML until a complete XML
# fragment (<tag>...</tag>) has been assembled.  Then broadcast the
# fragment as a single message to its listeners.
fr = file_reader.FileReader(sys.argv[1])

# Allocate an element that collects bits of XML until a complete XML
# fragment (<tag>...</tag>) has been assembled.  Then broadcast the
# fragment as a single message to its listeners.
xfc = xml_fragment_collector.XMLFragmentCollector()

# Wrap the raw XML in a format understood by the weMonitor API.
wmf = we_monitor_formatter.WeMonitorFormatter()

# For debugging, allocate an element that simply echos its input
# to stdout.
ech = echo.Echo()

fr.attach(xfc).attach(wmf).attach(ech)

# Start the reader thread
fr.start()
# wait until the reader thread exits
fr.thread.join()
