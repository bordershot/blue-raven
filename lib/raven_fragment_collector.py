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
        # at each call to update(), collect bits of xml...
        self.collected += message

        # until we see an entire string of the form:
        # {leading trash}\n
        # <{opening tag}>\n
        #   {line 1}\n
        #   {line 2}\n
        #   ...
        #   {line n}\n
        # </{closing tag}>{trailing trash}

        # print("self.collected = \n" + self.collected)
        
        m = re.search('(^|\r\n)(<(.*?)>((\r\n +.*)*)\r\n</(.*?)>)((.|\n)*)', self.collected)
        if (m):
            # print(m.groups())

            # group 1: leading trash (not used)
            # group 2: complete xml fragment
            # group 3: opening tag
            # group 4: "body" between opening and closing tags (not used)
            # group 5: last body line (not used)
            # group 6: closing tag
            # group 7: trailing trash
            # group 8: trailing trash final char (not used)

            if m.group(3) == m.group(6):
                self.notify(m.group(2))

            self.collected = m.group(7)
            # print("collected now = \n" + self.collected)
