"""
actor.py
Purpose: Implements the data structures and mechanics of an actor
"""
import string
from objects.relationship import Relationship
from objects.area import Area
import math

class Actor():
    # assumes it is given a .txt filename
    def __init__(self, filename):
        self.name = ""
        self.pronoun = ""
        self.starting_area = ""
        self.current_area = None
        self.rumors = []
        self.action_log = []
        self.relationships = []     # list of relationships the character has with all other characters. TODO: find where to initialize this list
        # dictionary of personality traits that influence the characters decisions. Always a value between 0 and 9
        self.personality = { "trustworthy" : 0, # how likely others are to tell this character a rumor
                             "talkative" : 0,   # how likely the character is to tell a rumor
                             "gullible" : 0,    # how likely the character is to believe a rumor
                             "nosy" : 0,        # how likely the character is to seek out rumors from others
                             "loyalty" : 0,     # how likely a character is to tell a bad rumor about a character they like
                             "fame" : 0,        # how well known the character is
                             "morality" : 0,    # how 'good' the character is. this influences the likelihood to mutate a rumor. 0-3 is evil, 4-5 is neutral, 6-9 is good
                             "memory" : 0,      # how good a character is at retelling a rumor
                             "perception" : 0   # how good a character is at understanding a rumor
                            }

        # initialize the character
        f = open(filename, "r")
        for line in f:
            line_array = line.split()
            item = line_array[0]
            value = " ".join(line_array[1:])
            if item == "name":
                self.name = value
            elif item == "pronoun":
                self.pronoun = value
            elif item == "area":
                self.starting_area = value
            elif item in self.personality:
                self.personality[item] = int(value)
            else:
                print(f'WARNING: trait {item} is not a valid trait')

    def start_relationship(self, character):
        self.relationships.append(Relationship(character))

    # do nothing
    def wait(self):
        self.action_log.append("wait")

    # given an Area object
    def move(self, area):
        if area == None:
            return
        if self.current_area != None:
            self.action_log.append("move")
            self.current_area.exit(self)
        self.current_area = area
        area.enter(self)

    # tell another character a rumor. pick rumor from ones the agent knows
    def gossip(self, listener):
        # TODO: get a character in the current location that is trusted and tell them a rumor
        self.action_log.append("gossip")

    def info(self):
        print("+---------ACTOR---------+")
        print(f'Name: {self.name} ({self.pronoun})')
        print(f'Current Location: {self.current_area.name}')
        print(f'PERSONALITY:')
        for p in self.personality:
            num_tabs = 4 - math.floor((len(p)+3) / 4)
            if num_tabs == 1:
                num_tabs += 1
            tabs = ""
            for t in range(num_tabs):
                tabs += "\t"
            print(f'  {p}:{tabs}{self.personality[p]}')
        print(f'RELATIONSHIPS')
        for i in range(len(self.relationships)):
            r = self.relationships[i]
            print(f'{i+1}. {r.character.name}')
            print(f'  trust:                {r.trust}\n' +
                  f'  admiration:           {r.admiration}\n' +
                  f'  love:                 {r.love}'
            )
        print("+-----------------------+\n")
