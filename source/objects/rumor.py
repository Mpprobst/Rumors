"""
rumor.py
Purpose: Implements the data structure of a rumor
"""

#from world import World
from objects.actor import Area
from objects.actor import Actor

class Rumor():
    def __init__(self, file, world):
        self.speaker = None         # who told this instance of the rumor
        self.listener = None        # who heard this instance of the rumor
        self.subject = None         # character who is doing something
        self.object = None          # character acted upon
        self.action = ""            # what the subject is doing to the object
        self.location = None        # where the action took place

        f = open(file, "r")
        for line in f:
            line_array = line.split()
            item = line_array[0]
            value = " ".join(line_array[1:])
            if item == "speaker":
                self.speaker = world.find_actor(value)
            elif item == "listener":
                self.listener = world.find_actor(value)
            elif item == "subject":
                self.subject = world.find_actor(value)
            elif item == "object":
                self.object = world.find_actor(value)
            elif item == "action":
                self.action = value
            elif item == "location":
                self.location = world.find_area(value)

    def info(self):
        print(f'+---------RUMOR---------+')
        #print(self.speaker.name)
        #print(self.listener.name)
        #print(self.subject.name)
        #print(self.object.name)
        #print(self.location.name)
        print(f'{self.speaker.name} told {self.listener.name} that {self.subject.name} did {self.action} with {self.object.name} in {self.location.name}')
        print(f'+-----------------------+')
