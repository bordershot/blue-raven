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

from we_monitor_writer import WeMonitorWriter
from test_helpers import captured_output
import mock
import unittest
import requests

class TestWeMonitorWriter(unittest.TestCase): 
    
    @mock.patch('we_monitor_writer.requests.post')
    def test_successful_write(self, mock_post):
        xml_frag = """<InstantaneousDemand></InstantaneousDemand>"""

        response = mock.MagicMock()
        response.status_code = 200
        response.content = "OK"
        mock_post.return_value = response

        writer = WeMonitorWriter()
        writer.update(xml_frag)
        self.assertTrue(mock_post.called, "Failed to call requests.post")

    @mock.patch('we_monitor_writer.syslog.syslog')
    @mock.patch('we_monitor_writer.requests.post')
    def test_failing_write(self, mock_post, mock_syslog):
        xml_frag = """<InstantaneousDemand></InstantaneousDemand>"""

        response = mock.MagicMock()
        response.status_code = 403
        response.content = "Forbidden"
        mock_post.return_value = response

        writer = WeMonitorWriter()
        writer.update(xml_frag)
        observed_arg = mock_syslog.call_args[0][1]
        self.assertRegexpMatches(observed_arg, 'Forbidden')

    @mock.patch('we_monitor_writer.os.system')
    @mock.patch('we_monitor_writer.syslog.syslog')
    @mock.patch('we_monitor_writer.time.sleep')
    @mock.patch('we_monitor_writer.requests.post')
    def test_one_connection_error(self, mock_post, mock_sleep, mock_syslog, mock_system):
        xml_frag = """<InstantaneousDemand></InstantaneousDemand>"""

        mock_post.side_effect = requests.ConnectionError("whoops")
        mock_system.return_value = 0

        writer = WeMonitorWriter()
        with self.assertRaises(requests.ConnectionError):
            writer.update(xml_frag)

        observed_arg = mock_syslog.call_args[0][1]
        self.assertRegexpMatches(observed_arg, 'ping')
