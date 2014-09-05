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

import unittest
from test_helpers import captured_output
import we_monitor_formatter
import tap

class TestWeMonitorFormatter(unittest.TestCase):

    def testGoodMessage(self):
        wmf = we_monitor_formatter.WeMonitorFormatter()
        slp_ = tap.Tap()
        wmf.attach(slp_)

        message = """<woof>
  <DeviceMacId>0x00158d00001ab152</DeviceMacId>
  <MeterMacId>0x000781000028c07d</MeterMacId>
  <TimeStamp>0x191868fb</TimeStamp>
</woof>"""

        wmf.update(message)
        observed = slp_.lastMessage()
        self.assertRegexpMatches(observed, 'xml version=')
        self.assertRegexpMatches(observed, 'rainforest macId=')
        self.assertRegexpMatches(observed, 'version="undefined"')
        self.assertRegexpMatches(observed, 'timestamp=')
        self.assertRegexpMatches(observed, 'DeviceMacId')

    def testMalformedMessage(self):
        wmf = we_monitor_formatter.WeMonitorFormatter()
        slp_ = tap.Tap()
        wmf.attach(slp_)

        message = """<woof>
  <DeviceMacId>0x00158d00001ab152</DeviceMacId>
  <MeterMacId>0x000781000028c07d</MeterMacId>
  <TimeStamp>0x191868fb</TimeStamp>
asdf<#saywhat?>
</woof>"""

        with captured_output() as (out, err):
            wmf.update(message)
        observed = slp_.lastMessage()
        self.assertEqual(observed, '')
        # In the future, this wll be logged, not sent to stdout
        stdobserved = out.getvalue()
        self.assertRegexpMatches(stdobserved, 'XML ParseError')
