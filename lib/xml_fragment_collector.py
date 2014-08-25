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
        self.notify(m.group(1) + "\n")
        self.collected = m.group(2)
        self.state = 0

