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

class RavenFragmentCollector(Subject, Observer):
    """Receives bits of XML via the update() method.  Collect a
    complete XML fragment, starting with <newline>'<'<tagname> and
    ending with <newline>'</'<tagname>'>' before emitting the
    fragment.

    Note: this depends on whitespace formatted XML, as produced by the
    Rainforest Automation RAVEn, where toplevel tags have zero
    indentation and non-toplevel tags have nonzero identation, such as
    this:

    <InstantaneousDemand>
      <DeviceMacId>0x00158d00002ab152</DeviceMacId>
      <MeterMacId>0x000781000038c07d</MeterMacId>
      <TimeStamp>0x191868fb</TimeStamp>
      ...
    </InstantaneousDemand>
    """

    def __init__(self):
        Subject.__init__(self)
        Observer.__init__(self)
        self.collected = ""

    # support for observer

    def update(self, message):
        self.collected += message

        m1 = re.search('^<\/(.*?)>', self.collected, flags=re.DOTALL)
        if (m1):
            tag = m1.group(1)
            # search for last instance of ^<{tag}> in self.collected>
            # use greedy search to consume any prior instances
            pattern = '(.*)(^<' + tag + '>.*^<\/' + tag + '>)(.*)'
            m2 = re.search(pattern, self.collected, flags=re.DOTALL)
            if (m2):
                # here:
                #  m2.group(1) is the entire fragment of interest
                #  m2.group(2) is trailing text (perhaps part of next fragment)
                self.notify(m2.group(1))
                self.collected = m2.group(2)
            else:
                # didn't find a match.  clear out collected string
                self.collected = ''

