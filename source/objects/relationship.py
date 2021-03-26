"""
relationship.py
Purpose: used by actor class to describe a relationship between them and another character
"""

import random

class Relationship():
    def __init__(self, _character):
        self.character = _character
        # TODO: skew these random values with the personalities of the characters involved
        self.trust = random.range(0, 9, 1)
        self.admiration = random.range(0, 9, 1)
        self.love = random.range(0, 9, 1)
