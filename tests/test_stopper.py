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
import stopper
import file_reader
import tap

def create_file(filename, text):
    with open(filename, "w") as f:
        f.write(text)

class TestStopper(unittest.TestCase):

    def testUpdate(self):
        filename = "/tmp/test_stopper_01.txt"
        written = """a
b
c
d
e
"""
        create_file(filename, written)

        file_reader_ = file_reader.FileReader(filename)
        stp_ = stopper.Stopper(file_reader_, 3)
        tap_ = tap.Tap()
        file_reader_.attach(stp_).attach(tap_)

        file_reader_.start()
        file_reader_.thread.join()

        expected = """a
b
c
"""
        observed = tap_.lastMessage()
        self.assertEqual(expected, observed)
