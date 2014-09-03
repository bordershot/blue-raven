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
import requests
import sys
import time

# Push a message to the weMonitor API service for Rainforest Eagle
# messages.  It receives complete XML fragments, such as:
#
# <?xml version="1.0"?>
# <rainforest macId="0x0000d8d5b9000348" version="undefined" timestamp="1373335064s">
#   <InstantaneousDemand>
#     <DeviceMacId>0x00158d00001ab152</DeviceMacId>
#     <MeterMacId>0x000781000028c07d</MeterMacId>
#     <TimeStamp>0x1918513b</TimeStamp>
#     ...
#   </InstantaneousDemand>
# </rainforest>

class WeMonitorWriter(Subject, Observer):

    def __init__(self):
        Subject.__init__(self)
        Observer.__init__(self)
        
    API_PREFIX='https://app.wemonitorhome.com/api/rainforest-eagle'
    MAX_RETRIES=5

    # support for observer

    def update(self, subject, message):
        self.post_with_retries(self.API_PREFIX, message)

    def post_with_retries(self, url, body):
        retries = 0
        while(True):
            try:
                self.try_post(url, body)
                break
            except requests.ConnectionError as e:
                if (retries >= self.MAX_RETRIES):
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

