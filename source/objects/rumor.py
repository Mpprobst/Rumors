"""
rumor.py
Purpose: Implements the data structure of a rumor
"""

#from world import World
from objects.actor import Area
from objects.actor import Actor
import random

class Rumor():
    def __init__(self, id, file=None, world=None, speaker=None, listener=None, subject=None, objects=[], action=None, location=None):
        self.id = id                    # identifier for the rumor
        self.speaker = speaker          # who told this instance of the rumor
        self.listener = listener        # who heard this instance of the rumor
        self.subject = subject          # character who is doing something
        self.objects = objects          # character acted upon
        self.action = action            # what the subject is doing to the object
        #self.preposition = preposition    # something like with, or, on, or nothing
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
                    self.action = world.find_action(value)
                elif item == "location":
                    self.location = world.find_area(value)
            self.listener.hear_rumor(self)
            self.speaker.hear_rumor(self)

    def clone(self, r):
        return Rumor(id=r.id, speaker=r.speaker, listener=r.listener, subject=r.subject, objects=r.objects.copy(), action=r.action, location=r.location)

    # given player input string, construct a rumor and spread it
    def parse(s, args, world):
        speaker = s
        listener = None
        subject = world.actors[0]
        objects = []
        action = world.actions[0]
        location = world.areas[0]

        rumorIdx = 0
        listener = world.find_actor(args[0].replace(',', ''))
        if listener == world.default_actor:
            listener = world.find_actor("Blair")

        if args[0].find(','):
            rumorIdx = 1

        rumor = " ".join(args[rumorIdx:])

        # find things relative to the found action
        action_idx = 0       # position at which the action occurs
        for a in world.actions:
            aname = a.name
            action_idx = rumor.find(aname)
            if action_idx > -1:
                action = a
                break

        if action_idx < 0:
            print(f'{listener.name}: I don\'t know what that means.')

        for actor in world.actors:
            if rumor[0:action_idx].find(actor.shortname) > -1:
                subject = actor
            if rumor[action_idx:].find(actor.shortname) > -1:
                if actor not in objects:
                    objects.append(actor)

        for area in world.areas:
            if rumor.find(area.name) > -1:
                location = area
                break

        return Rumor(id=len(world.initial_rumors)+1, speaker=speaker, listener=listener, subject=subject, objects=objects, action=action, location=location)

    def random_intro(self):
        rand = random.randint(0, 2)
        tell_speaker = True if random.random() < 0.5 else False
        str = ""
        if self.speaker.name == self.listener.name or not tell_speaker:
            if rand == 0:
                str += f'I can\'t believe that'
            elif rand == 1:
                str += f'Apparently,'
            elif rand == 2:
                str += f'Word on the street is'
        else:
            if rand == 0:
                str += f'I heard from {self.speaker.name} that'
            elif rand == 1:
                str += f'{self.speaker.name} told me that'
            elif rand == 2:
                str += f'{self.speaker.name} was saying'
        return str

    def info(self, options=None):
        #print(f'+---------RUMOR---------+')
        #print(self.speaker.name)
        #print(self.speaker.shortname)
        #print(self.listener.name)
        #print(self.subject.name)
        #if self.location != None:
        #    print(self.location.name)
        objects = []
        for obj in self.objects:
            objects.append(obj.shortname)

        if len(objects) > 1:
            objects[len(objects)-1] = "and " + objects[len(objects)-1]
        rumor_str = f'{self.speaker.name}: {self.random_intro()} {self.speaker.shortname} told {self.listener.shortname} that {self.subject.shortname} {self.action.name} {", ".join(objects[0:])}'
        rumor_str += f' in {self.location.name}.' if self.location != None else "."
        print(rumor_str)
        #print(f'+-----------------------+')
