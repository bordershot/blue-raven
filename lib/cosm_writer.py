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
import json
import os
import sys

class CosmWriter(Subject, Observer):

    def __init__(self):
        Subject.__init__(self)
        Observer.__init__(self)
        
    API_PREFIX='http://api.cosm.com/v2'
    FEED_ID='129722'

    # support for observer

    def update(self, subject, message):
        body = {"datapoints":[message]}
        r = requests.post(self.API_PREFIX + '/feeds/' + self.FEED_ID + '/datastreams/1/datapoints.json',
                          data=json.dumps(body),
                          headers = {'X-ApiKey': self.cosm_api_key()})
        if r.status_code >= 300:
            sys.stderr.write("Error:" + r.content + "\n")
        self.notify(message)

    def cosm_api_key(self):
        return os.environ["COSM_API_KEY"]
