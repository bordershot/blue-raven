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
import re

class XMLFragmentCollector(Subject, Observer):
    """Receives bits of XML via the update() method.  Look for a
    pattern that matches an opening <tag_name ...>, then start
    collecting XML until a matching closing </tag_name ...> is found,
    then emit everything between the opening and closing tags.

    Note: this will not properly handle nested tags, e.g.:
    <tag_name> ...
      <tag_name> ... </tag_name>
    </tag_name>
    """

    def __init__(self):
        Subject.__init__(self)
        Observer.__init__(self)
        self.state = 0
        self.collected = ""

    # support for observer

    def update(self, subject, message):
        self.collected += message
        # print("collected = " + self.collected)

        if (self.state == 0):
            # searching for <tag_name>...
            m = re.search('.*?(<([^\/][^>]*)>.*)', self.collected, flags=re.DOTALL)
            if not(m): return
            # here:
            #  m.group(1) is the entire string starting with the opening <
            #  m.group(2) is the tag
            self.collected = m.group(1)
            self.tag = m.group(2)
            self.state = 1
                
        m = re.search('(.*<\/' + self.tag + '>)(.*)', self.collected, flags=re.DOTALL)
        # searching for </tag_name>...
        if not(m): return
        # here: m.group(1) is everything upto and including </tag_name>,
        # m.group(2) is anything following it.
        self.notify(m.group(1))
        self.collected = m.group(2)
        self.state = 0

