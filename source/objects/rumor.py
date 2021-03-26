"""
rumor.py
Purpose: Implements the data structure of a rumor
"""

class Rumor():
    def __init__(self):
        self.speaker = None         # who told this instance of the rumor
        self.listener = None        # who heard this instance of the rumor
        self.subject = None         # character who is doing something
        self.object = None          # character acted upon
        self.action = ""            # what the subject is doing to the object
        self.location = None        # where the action took place
