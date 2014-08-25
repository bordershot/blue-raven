from subject import *
from observer import *
import sys

class FileWriter(Subject, Observer):

    def __init__(self, file_name):
        Subject.__init__(self)
        Observer.__init__(self)
        self.file_name = file_name

    # support for observer

    # by using 'a' (append) mode, we flush the output after each
    # write, which is probably the preferred behavior.
    def update(self, subject, message):
        with open(self.file_name, 'a') as f:
            f.write(message + '\n')
        self.notify(message)



