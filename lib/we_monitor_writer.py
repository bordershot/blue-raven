from subject import *
from observer import *
import requests
import sys
import datetime

# Push a message to the weMonitor API service for Rainforest Eagle
# messages.  Each message should be a complete XML fragment, e.g.
# <?xml version="1.0"?>
# <rainForest macId="0x0000d8d5b9000348" version="undefined" timestamp="1373335064s">
# <InstantaneousDemand>
#   <DeviceMacId>0xd8d5b90000000c9c</DeviceMacId>
#   ...
# </InstantaneousDemand>
#
# As a convenience, the message is echoed to any listener attached
# to the WeMonitorWriter object (e.g. for logging or debugging).
#
class WeMonitorWriter(Subject, Observer):

    def __init__(self, rainforest_mac_id):
        Subject.__init__(self)
        Observer.__init__(self)
        self.rainforest_mac_id = rainforest_mac_id
        
    API_PREFIX='https://app.wemonitorhome.com/api/rainforest-eagle'

    # support for observer

    def update(self, subject, message):
        data = self.preamble() + message + self.postamble()
        r = requests.post(self.API_PREFIX, data=data)
        if r.status_code >= 300:
            sys.stderr.write("Error:" + r.content + "\n")
        self.notify("status = " + str(r.status_code) + " " + r.content + "\n" + data)

    def preamble(self):
        return ('<?xml version="1.0"?>\n'
                '<rainforest'
                ' macId="' + self.rainforest_mac_id + '"'
                ' version="undefined"'
                ' timestamp="' + str(self.seconds_since_1970()) + 's">\n')

    def postamble(self):
        return ('</rainforest>\n')

    def unix_time(self, dt):
        epoch = datetime.datetime.utcfromtimestamp(0)
        delta = dt - epoch
        return delta.total_seconds()

    def seconds_since_1970(self):
        return int(round(self.unix_time(datetime.datetime.now())))

