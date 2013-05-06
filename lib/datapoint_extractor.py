from subject import *
from observer import *
import re
import datetime
import calendar
import time

class DatapointExtractor(Subject, Observer):
    """Receive an XML fragment of the form:

<InstantaneousDemand>
  <DeviceMacId>0x00158d00001ab152</DeviceMacId>
  <MeterMacId>0x000781000028c07d</MeterMacId>
  <TimeStamp>0x1918513b</TimeStamp>
  <Demand>0x0000be</Demand>
  <Multiplier>0x00000001</Multiplier>
  <Divisor>0x000003e8</Divisor>
  <DigitsRight>0x03</DigitsRight>
  <DigitsLeft>0x06</DigitsLeft>
  <SuppressLeadingZero>Y</SuppressLeadingZero>
</InstantaneousDemand>

      Note that timestamp is seconds from Jan 1, 2000 rather than Jan 1 1970.

      From this, extract the timestamp as an ISO 8601 string and the
      instantaneous usage in Watts and pass as a dictionary on to the
      observers:

    {"at": "2013-05-20T11:01:43Z", "value": 22.3}
    """

    def __init__(self):
        Subject.__init__(self)
        Observer.__init__(self)

    def update(self, subject, message):
        self.process_xml(message)

    def process_xml(self, message):
        seconds_since_2000 = self.extract_field('TimeStamp', message)
        demand = self.extract_field('Demand', message)
        multiplier = self.extract_field('Multiplier', message)
        divisor = self.extract_field('Divisor', message)
        if seconds_since_2000 and demand and multiplier and divisor:
            self.notify({"at": self.convert_to_gmt(seconds_since_2000),
                         "value": 1000.0 * demand * multiplier / divisor})
        
    # a typical field in xml is:
    #   <FieldName>0x12345abcd</FieldName>
    # Search for FieldName and convert to decimal.
    def extract_field(self, name, xml):
        m = re.search('<'+name+'>(.*?)<\/'+name+'>', xml)
        if m:
            return int(m.group(1), 16)
        else:
            return None

    def convert_to_gmt(self, seconds_since_2000):
        epoch_offset = calendar.timegm(time.strptime("2000-01-01", "%Y-%m-%d"))
        return datetime.datetime.utcfromtimestamp(seconds_since_2000+epoch_offset).isoformat()
