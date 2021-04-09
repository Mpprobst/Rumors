"""
relationship.py
Purpose: used by actor class to describe a relationship between them and another character
"""

import random

class Relationship():
    def __init__(self, char1, char2):
        self.character = char2
        # TODO: skew these random values with the personalities of the characters involved

        # determine trust based on char1's gullibile trait and char2's trustworthy trait
        trust_val = int(char1.personality["gullible"] / 3) + int(char2.personality["trustworthy"] / 3) + random.randint(0, 4)
        self.trust = self.clamp(trust_val)
        # determine admiration based on how well the two character's morality align and how famous the other character is
        admire_val = int((9 - char1.personality["morality"] - char2.personality["morality"]) / 3) + int(char2.personality["fame"] / 3) + random.randint(0, 4)
        self.admiration = self.clamp(admire_val)
        # determine based on similarities in talkativeness and loyalty
        love_val = int((9 - char1.personality["talkative"] - char2.personality["talkative"]) / 3) + int(char2.personality["loyalty"] / 3) + random.randint(0, 4)
        self.love = self.clamp(love_val)


    def clamp(self, value):
        if value > 9:
            value = 9
        elif value < 0:
            value = 0
        return value
