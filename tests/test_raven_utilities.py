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

import raven_utilities
import unittest
import mock

class TestRavenUtilities(unittest.TestCase): 
    
    @staticmethod
    def persevered_fn_01():
        raise RuntimeError("whoops!")

    @staticmethod
    def concede_after(n):
        n = [n]
        def conceder():
            if (n[0] > 0):
                n[0] -= 1
                return False
            else:
                return True
        return conceder
    
    @mock.patch('we_monitor_writer.syslog.syslog')
    def test_with_perseverance_should_retry_and_log(self, mock_syslog):
        n = 3
        with self.assertRaises(RuntimeError):
            raven_utilities.with_perseverance(TestRavenUtilities.persevered_fn_01, 
                                              TestRavenUtilities.concede_after(n))

        self.assertEqual(mock_syslog.call_count, n+1)
        # yuck.  what's the correct way to extract the arg?
        for i in range(n + 1):
            expected = "retrying" if (i < n) else "giving up"
            self.assertRegexpMatches(mock_syslog.call_args_list[i][0][0], expected)




