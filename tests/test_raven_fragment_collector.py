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
import raven_fragment_collector
import tap

class TestRavenFragmentCollector(unittest.TestCase):

    def test01(self):
        raven_fragment_collector_ = raven_fragment_collector.RavenFragmentCollector()
        tap_ = tap.Tap()
        raven_fragment_collector_.attach(tap_)

        raven_fragment_collector_.update("<a>\n")
        self.assertEqual("", tap_.lastMessage())
        raven_fragment_collector_.update("  <x>x</x>\n")
        self.assertEqual("", tap_.lastMessage())
        raven_fragment_collector_.update("  <y>y</y>\n")
        self.assertEqual("", tap_.lastMessage())
        raven_fragment_collector_.update("  <z>z</z>\n")
        self.assertEqual("", tap_.lastMessage())
        raven_fragment_collector_.update("</a>\n")
        expected = """<a>
  <x>x</x>
  <y>y</y>
  <z>z</z>
</a>"""
        self.assertEqual(expected, tap_.lastMessage())

    def test02(self):
        raven_fragment_collector_ = raven_fragment_collector.RavenFragmentCollector()
        tap_ = tap.Tap()
        raven_fragment_collector_.attach(tap_)

        raven_fragment_collector_.update("<b>\n")
        raven_fragment_collector_.update("<a>\n")
        self.assertEqual("", tap_.lastMessage())
        raven_fragment_collector_.update("  <x>x</x>\n")
        self.assertEqual("", tap_.lastMessage())
        raven_fragment_collector_.update("  <y>y</y>\n")
        self.assertEqual("", tap_.lastMessage())
        raven_fragment_collector_.update("  <z>z</z>\n")
        self.assertEqual("", tap_.lastMessage())
        raven_fragment_collector_.update("</a>\n")
        expected = """<a>
  <x>x</x>
  <y>y</y>
  <z>z</z>
</a>"""
        self.assertEqual(expected, tap_.lastMessage())

    def test03(self):
        raven_fragment_collector_ = raven_fragment_collector.RavenFragmentCollector()
        tap_ = tap.Tap()
        raven_fragment_collector_.attach(tap_)

        raven_fragment_collector_.update("<a>\n")
        self.assertEqual("", tap_.lastMessage())
        raven_fragment_collector_.update("  <x>x</x>\n")
        self.assertEqual("", tap_.lastMessage())
        raven_fragment_collector_.update("  <y>y</y>\n")
        self.assertEqual("", tap_.lastMessage())
        raven_fragment_collector_.update("  <z>z</z>\n")
        self.assertEqual("", tap_.lastMessage())
        raven_fragment_collector_.update("</b>\n")
        self.assertEqual("", tap_.lastMessage())

    def test04(self):
        raven_fragment_collector_ = raven_fragment_collector.RavenFragmentCollector()
        tap_ = tap.Tap()
        raven_fragment_collector_.attach(tap_)

        raven_fragment_collector_.update("<a>\n")
        raven_fragment_collector_.update("<b>\n")
        self.assertEqual("", tap_.lastMessage())
        raven_fragment_collector_.update("  <x>x</x>\n")
        self.assertEqual("", tap_.lastMessage())
        raven_fragment_collector_.update("  <y>y</y>\n")
        self.assertEqual("", tap_.lastMessage())
        raven_fragment_collector_.update("  <z>z</z>\n")
        self.assertEqual("", tap_.lastMessage())
        raven_fragment_collector_.update("</a>\n")
        self.assertEqual("", tap_.lastMessage())
