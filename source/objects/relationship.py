"""
relationship.py
Purpose: used by actor class to describe a relationship between them and another character
"""

import random

class Relationship():
    def __init__(self, char1, char2):
        self.character = char2

        # determine trust based on char1's gullibile trait and char2's trustworthy trait
        trust_val = int(char1.personality["gullible"] / 3) + int(char2.personality["trustworthy"] / 3) + random.randint(0, 5)
        self.trust = self.clamp(trust_val)
        # determine admiration based on how well the two character's morality align and how famous the other character is
        admire_val = int((9 - char1.personality["morality"] - char2.personality["morality"]) / 3) + int(char2.personality["fame"] / 3) + random.randint(0, 5)
        self.admiration = self.clamp(admire_val)
        # determine based on similarities in talkativeness and loyalty
        love_val = int((9 - char1.personality["talkative"] - char2.personality["talkative"]) / 3) + int(char2.personality["loyalty"] / 3) + random.randint(0, 5)
        self.love = self.clamp(love_val)

    def info(self):
        trust = 0
        respect = 0
        feel = 0
        trust_str = ""
        respect_str = ""
        feel_str = ""
        if self.trust >= 7:
            trust_str = f'I trust {self.character.get_pronoun2()} with my life'
            trust = 2
        elif self.trust >= 3:
            trust_str = f'I don\'t know if I trust {self.character.get_pronoun2()}'
            trust = 1
        else:
            trust_str = f'{self.character.get_pronoun1()} can\'t be trusted'

        if self.admiration >= 7:
            respect_str = f'{self.character.get_pronoun1()} is great'
            respect = 2
        elif self.admiration >= 3:
            respect_str = f'I don\'t know much about {self.character.get_pronoun2()}'
            respect = 1
        else:
            respect_str = f'{self.character.get_pronoun1()} {"are" if self.character.pronoun == "T" else "is"} kinda terrible'

        if self.love >= 7:
            feel_str = f'I am head over heels for {self.character.get_pronoun2()}'
            feel = 2
        elif self.love >= 3:
            feel_str = f'{self.character.get_pronoun2()} and I are friends'
            feel = 1
        else:
            feel_str = f'I hate {self.character.get_pronoun2()}'

        str = f'Oh, {self.character.name}? Well, {respect_str}, {"and" if trust >= respect else "but"} {trust_str}, {"and" if (trust > feel and trust != 1) else "but"} {feel_str}.'
        return str

    def clamp(self, value):
        if value > 9:
            value = 9
        elif value < 0:
            value = 0
        return value
