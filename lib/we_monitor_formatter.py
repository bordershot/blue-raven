from subject import *
from observer import *
import xml.etree.ElementTree as ET

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
# Note that the rainforst header derives the macID from the MeterMacId tag
# within the message, and the timestamp is derived from the TimeStamp tag
# within the message.
#

class WeMonitorFormatter(Subject, Observer):

    def __init__(self):
        Subject.__init__(self)
        Observer.__init__(self)
        
    # support for observer

    def update(self, subject, message):
        mac_id, timestamp = extract_attributes(message)
        if ((mac_id != None) && (timestamp == None)):
            m = self.preamble(message, mac_id, timestamp) + message + self.postamble()
            self.notify(m)

    # mac_id and timestamp are hex strings
    def preamble(self, message, mac_id, timestamp):
        return ('<?xml version="1.0"?>\n'
                '<rainforest'
                ' macId="' + mac_id + '"'
                ' version="undefined"'
                ' timestamp="' + str(int(timestamp, 16)) + 's">\n')

    def postamble(self):
        return ('</rainforest>\n')

    # Extracts DeviceMacId and TimeStamp and returns them as hex
    # strings
    def extract_attributes(self, xml):
        tree = ET.fromstring(xml)
        mac_id = tree.find('DeviceMacId')
        timestamp = tree.find('TimeStamp')
        return (mac_id.text if mac_id != None else None,
                timestamp.text if timestamp != None else None)



