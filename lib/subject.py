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

"""Subject is the publish half of a publish / subscribe framework.  A Subject has a
set of Observers.  A call to subject.notify(msg) generates a call to 
observer.update(msg) in each of the observers.  Message passing is thread
safe.

To associate an observer with the sender, call sender.attach(observer).  As
a convenience, attach() returns the observer, so creating a chain of connections is
as simple as s1.attach(s2).attach(s3).attach(s4)
"""

class Subject:

    def __init__(self):
        self.observers = set()

    def notify(self, message):
        for observer in self.observers:
            try:
                observer.lock.acquire()
                observer.update(message)
            finally:
                observer.lock.release()

    def attach(self, observer):
        self.observers.add(observer)
        return observer         # facilitate chaining

    def detach(self, observer):
        self.observers.discard(observer)

