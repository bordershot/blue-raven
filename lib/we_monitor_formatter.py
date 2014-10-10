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

from subject import *
from observer import *
import xml.etree.ElementTree as ET
import syslog

# Format an XML fragment for sending to the WeMonitor API service for
# the Rainforest Eagle.  It receives complete XML fragments, such as:
#
#   <InstantaneousDemand>
#     <DeviceMacId>0x00158d00001ab152</DeviceMacId>
#     <MeterMacId>0x000781000028c07d</MeterMacId>
#     <TimeStamp>0x1918513b</TimeStamp>
#     ...
#   </InstantaneousDemand>
#
# and emits the same XML, but preceded by a header line and wrapped
# within a <rainforest ...></rainforest> tag, such as:
# 
#   <?xml version="1.0"?>
#   <rainforest macId="0x0000d8d5b9000348" version="undefined" timestamp="1373335064s">
#     <InstantaneousDemand>
#       <DeviceMacId>0x00158d00001ab152</DeviceMacId>
#       <MeterMacId>0x000781000028c07d</MeterMacId>
#       <TimeStamp>0x1918513b</TimeStamp>
#       ...
#     </InstantaneousDemand>
#   </rainforest>
#
# Note that the rainforst header derives the macID from the MeterMacId
# tag within the message, and the timestamp is derived from the
# TimeStamp tag within the message.  If either of those are missing,
# no message is emitted.
#

class WeMonitorFormatter(Subject, Observer):

    def __init__(self):
        Subject.__init__(self)
        Observer.__init__(self)
        
    # support for observer

    def update(self, message):
        mac_id, timestamp = self.extract_attributes(message)
        if ((mac_id != None) and (timestamp != None)):
            m = self.preamble(message, mac_id, timestamp) + message + self.postamble()
            self.notify(m)

    SECONDS_BETWEEN_2000_AND_1970 = 946684800

    # mac_id and timestamp are hex strings.  Note that timestamp refers to 
    # the number of seconds since 2000.  The preamble requires the number 
    # of seconds since 1970, so some conversion is required.
    def preamble(self, message, mac_id, timestamp):
        seconds_since_epoch = int(timestamp, 16) + self.SECONDS_BETWEEN_2000_AND_1970
        return ('<?xml version="1.0"?>\n'
                '<rainforest'
                ' macId="' + mac_id + '"'
                ' version="undefined"'
                ' timestamp="' + str(seconds_since_epoch) + 's">\n')

    def postamble(self):
        return ('</rainforest>\n')

    # Extracts DeviceMacId and TimeStamp and returns them as hex
    # strings.  Note that TimeStamp is expressed as the number of
    # seconds since Jan 1, 2000
    def extract_attributes(self, xml):
        try:
            tree = ET.fromstring(xml)
            mac_id = tree.find('DeviceMacId')
            timestamp = tree.find('TimeStamp')
            return (mac_id.text if mac_id != None else None,
                    timestamp.text if timestamp != None else None)
        except ET.ParseError as e:
            # Recover from malformed XML
            syslog.syslog(syslog.LOG_NOTICE, "XML ParseError:{0} (ignoring...)".format(e))
            return (None, None)




