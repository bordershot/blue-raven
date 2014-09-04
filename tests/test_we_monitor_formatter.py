# Test WeMonitorFormatter's ability to catch malformed fragments
# Synopsis:
#  python spec/test_we_monitor_formatter.py log/faulty.xml

import sys
import time

import echo
import file_reader
import we_monitor_formatter
import xml_fragment_collector

def usage(argv):
    sys.exit("USAGE:\n    python " + sys.argv[0] + "test_filename\n")

if len(sys.argv) != 2:
    usage(sys.argv)

# Allocate an element that broadcasts raw Rainforest packets
filename = sys.argv[1]

fr = file_reader.FileReader(filename)
xfc = xml_fragment_collector.XMLFragmentCollector()
wmf = we_monitor_formatter.WeMonitorFormatter()
ech = echo.Echo()

# String the elements together and start the reader thread.
fr.attach(xfc).attach(wmf).attach(ech)

# Start the reader thread
fr.start()
# Here at end of file (or some errror)
fr.thread.join()
