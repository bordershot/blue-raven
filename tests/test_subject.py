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
import tap
from subject import *

class SampleSubject(Subject):
    pass

class TestSubject(unittest.TestCase):

    def testVanillaNotify(self):
        subject_ = SampleSubject()
        tap_ = tap.Tap()
        subject_.attach(tap_)

        expected = """a
b
c
"""
        subject_.notify(expected)
        observed = tap_.lastMessage()
        self.assertEqual(expected, observed)

    def testDoubleAttach(self):
        subject_ = SampleSubject()
        tap_ = tap.Tap()
        subject_.attach(tap_)
        subject_.attach(tap_)   # should only attach once
        expected = """a
b
c
"""
        subject_.notify(expected)
        observed = tap_.lastMessage()
        self.assertEqual(expected, observed)

    def testDetach(self):
        subject_ = SampleSubject()
        tap_ = tap.Tap()
        subject_.attach(tap_)
        subject_.detach(tap_)
        expected = """a
b
c
"""
        subject_.notify(expected)
        observed = tap_.lastMessage()
        self.assertEqual("", observed)

