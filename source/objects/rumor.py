"""
rumor.py
Purpose: Implements the data structure of a rumor
"""

#from world import World
from objects.actor import Area
#from objects.actor import Actor
import random

class Rumor():
    def __init__(self, id, file=None, world=None, speaker=None, listener=None, subject=None, objects=[], action=None, location=None, versions=[]):
        self.id = id                    # identifier for the rumor
        self.speaker = speaker          # who told this instance of the rumor
        self.listener = listener        # who heard this instance of the rumor
        self.subject = subject          # character who is doing something
        self.objects = objects          # character acted upon
        self.action = action            # what the subject is doing to the object
        #self.preposition = preposition    # something like with, or, on, or nothing
        self.location = location        # where the action took place
        self.versions = []

        if file != None:
            self.objects = []
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
            #self.listener.hear_rumor(self)
            #self.speaker.hear_rumor(self)
            self.versions.append(self.copy())
        #print(f'construct {id}')
        return None

    def update(self, rumor):
        self.versions.append(self.copy())
        self.speaker = rumor.speaker
        self.listener = rumor.listener
        self.subject = rumor.subject
        self.objects = rumor.objects
        self.action = rumor.action
        self.location = rumor.location

    def copy(self):
        #print(f'copying {self.id}')
        return Rumor(id=self.id, speaker=self.speaker, listener=self.listener, subject=self.subject, objects=self.objects.copy(), action=self.action, location=self.location, versions=[])

    # given player input string, construct a rumor and spread it
    def parse(s, args, world):
        speaker = s
        listener = None
        subject = world.actors[0]
        objects = []
        action = world.actions[0]
        location = world.find_area("Saloon")

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
            #print(f'looking for {aname}')
            if action_idx < 0:
                for alias in a.aliases:
                    #print(f'alias: {alias}')
                    if rumor.find(alias) > 0:
                        action = a
                        action_idx = rumor.find(alias)
                        break
            if action_idx > -1:
                action = a
                break

        if action_idx < 0:
            print(f'{listener.name}: I don\'t know what that means.')
            return None

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

        rumor = Rumor(id=len(world.rumors)+1, speaker=speaker, listener=listener, subject=subject, objects=objects, action=action, location=location)
        rumor.versions.append(rumor.copy())
        # TODO: See if rumor already exists, update it if so.
        new_rumor = True
        for ru in world.rumors:
            if ru.exists(rumor):
                rumor.id = ru.id
                ru.new_version(rumor, world)
                new_rumor = False
                break

        if new_rumor:
            world.rumors.append(rumor)
        return rumor

    def exists(self, rumor, exact=False):
        req = 3 if not exact else 4

        last = self
        if (len(self.versions) > 0):
            last = self.versions[len(self.versions)-1]

        same = 0

        #if rumor.speaker.shortname == last.speaker.shortname:
        #    same += 1
        #if rumor.listener.shortname == last.listener.shortname:
        #    same += 1
        if rumor.subject.shortname == last.subject.shortname:
            same += 1
        if len(rumor.objects) == len(last.objects):
            match = 1
            for i in range(len(rumor.objects)):
                if rumor.objects[i].shortname != last.objects[i].shortname:
                    match = 0
                    break
            same += match
        if rumor.action.name == last.action.name:
            same += 1
        if rumor.location.name == last.location.name:
            same += 1

        if same < req:
            return False
        return True

    # return True if the rumor was unique enough for updating it, False otherwise
    def new_version(self, rumor, world):
        if rumor == None:
            return False
        #print(f'num Version: {len(self.versions)}')
        unique = False
        if not self.exists(rumor, True):
            self.update(rumor)
            unique = True

        for r in world.rumors:
            if r.id == rumor.id:
                #print(f'adding version to {self.id}')
                if not r.exists(rumor, True):
                    r.update(rumor)
                    unique = True
                #r.info(1)
        return unique

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

    def prnt_rumor(self, rumor):
        objects = []
        for obj in rumor.objects:
            objects.append(obj.shortname)

        if len(objects) > 1:
            objects[len(objects)-1] = "and " + objects[len(objects)-1]
        #print(f'id: {self.id}')
        rumor_str = f'{rumor.subject.shortname} {rumor.action.name} {", ".join(objects[0:])}'
        rumor_str += f' in the {rumor.location.name}.' if rumor.location != None else "."
        return rumor_str

    def info(self, options=None):
        #print(f'+---------RUMOR---------+')
        #print(self.speaker.name)
        #print(self.speaker.shortname)
        #print(self.listener.name)
        #print(self.subject.name)
        #if self.location != None:
        #    print(self.location.name)
        #print(f'versions of {self.id}: {len(self.versions)}')
        if len(self.versions) == 0 or options == None:
            rumor_str = f'{self.speaker.name}: {self.random_intro()} ' if options == None else ""
            rumor_str += self.prnt_rumor(self)
            print(rumor_str)
        else:
            for i in range(len(self.versions)):
                rumor = self.versions[i]
                rumor_str = f'\tv{i}: '
                rumor_str += f'{rumor.speaker.shortname} told {rumor.listener.shortname} that '
                rumor_str += self.prnt_rumor(rumor)
                print(rumor_str)
        #print(f'+-----------------------+')
