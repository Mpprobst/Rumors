"""
rumor.py
Purpose: Implements the data structure of a rumor
"""

#from world import World
from objects.actor import Area
from objects.actor import Actor

class Rumor():
    def __init__(self, id, file=None, world=None, speaker=None, listener=None, subject=None, objects=[], action=None, location=None):
        self.id = id                    # identifier for the rumor
        self.speaker = speaker          # who told this instance of the rumor
        self.listener = listener        # who heard this instance of the rumor
        self.subject = subject          # character who is doing something
        self.objects = objects          # character acted upon
        self.action = action            # what the subject is doing to the object
        self.location = location        # where the action took place

        if file != None:
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
                elif item == "objects":
                    obj = ""
                    idx = 0
                    while idx < len(value):
                        if value[idx] == ',':
                            self.objects.append(world.find_actor(obj))
                            obj = ""
                            idx += 1
                        else:
                            obj += value[idx]
                        idx += 1
                    self.objects.append(world.find_actor(obj))
                elif item == "action":
                    self.action = value
                elif item == "location":
                    self.location = world.find_area(value)
        self.listener.hear_rumor(self)
        self.speaker.hear_rumor(self)

    def info(self, options=None):
        #print(f'+---------RUMOR---------+')
        #print(self.speaker.name)
        #print(self.listener.name)
        #print(self.subject.name)
        #print(self.object.name)
        #print(self.location.name)
        objects = []
        for obj in self.objects:
            objects.append(obj.shortname)

        objects[len(objects)-1] = "and " + objects[len(objects)-1]
        print(f'{self.speaker.shortname} told {self.listener.shortname} that {self.subject.shortname} did {self.action} with {", ".join(objects[0:])} in {self.location.name}')
        #print(f'+-----------------------+')
