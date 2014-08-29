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
    MAX_RETRIES=5

    # support for observer

    def update(self, subject, message):
        body = self.preamble() + message + self.postamble()
        self.post_with_retries(self.API_PREFIX, body)

    def post_with_retries(self, url, body):
        retries = 0
        while(True):
            try:
                self.try_post(url, body)
                break
            except requests.ConnectionError as e:
                if (retries >= MAX_RETRIES):
                    raise
                sleep_time = self.make_holdoff_time(retries)
                print "Retrying ConnectionError({0}: {1}) in {2} seconds".format(e.errno, e.strerror, sleep_time)
                time.sleep(sleep_time)
                retries += 1

    def try_post(self, url, body):
        r = requests.post(url, data=body)
        msg = str(r.status_code) + " " + r.content + "\n"
        if r.status_code >= 300:
            sys.stderr.write("Error: POST returned " + msg)
        self.notify(msg + body)

    def make_holdoff_time(self, retries):
        return 2**(retries * 2)

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

