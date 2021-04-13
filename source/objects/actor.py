"""
actor.py
Purpose: Implements the data structures and mechanics of an actor
"""
import string
from objects.relationship import Relationship
from objects.area import Area
import math
import random

class Actor():
    # assumes it is given a .txt filename
    def __init__(self, filename, world):
        self.name = ""
        self.shortname = ""
        self.pronoun = ""
        self.world = world
        self.eavsedropping = False
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
                names = value.split()
                if "the" in names:
                    self.shortname = names[0]
                else:
                    self.shortname = names[1]
            elif item == "pronoun":
                self.pronoun = value
            elif item == "area":
                self.starting_area = value
            elif item in self.personality:
                self.personality[item] = int(value)
            else:
                print(f'WARNING: trait {item} is not a valid trait')

    def start_relationship(self, char):
        self.relationships.append(Relationship(self, char))

    def get_relationship(self, name):
        for r in self.relationships:
            if r.character.shortname == name:
                return r

    def hear_rumor(self, rumor):
        hadHeard = False
        for r in self.rumors:
            if rumor.id == r.id:
                # I've heard this before
                rumor = r
                hadHeard = True
                return

        if not hadHeard:
            self.rumors.append(rumor)

        # TODO: now adjust relationships
        # find the action object in the rumor
        action = self.world.find_action(rumor.action)
        # based on personality, choose how much to believe the rumor
        belief = 5
        subj_rel = self.get_relationship(rumor.subject.shortname)

        if action == None or subj_rel == None:
            return

        belief -= self.personality["gullible"] - subj_rel.trust
        belief += subj_rel.admiration - (9-self.personality["loyalty"])
        belief += subj_rel.love - 5

        print(f'{rumor.speaker.shortname} is telling {self.shortname} that {rumor.subject.shortname} {rumor.action} {rumor.objects[0].shortname}')
        speaker_rel = self.get_relationship(rumor.speaker.shortname)
        if speaker_rel != None:
            str = f'1. Relationship of {self.shortname} and {speaker_rel.character.shortname}\n  {speaker_rel.trust} {speaker_rel.admiration} {speaker_rel.love}'
            if belief > 10:
                belief = 2
                speaker_rel.Trust(1)
                print(f'{self.shortname} really believes it!')

            elif belief > 5:
                belief = 1
                print(f'{self.shortname} believes it.')
            elif belief > 0:
                belief = 0
                speaker_rel.Trust(-1)
                print(f'{self.shortname} doesn\'t believe it!')
            else:
                belief = 0
                speaker_rel.Trust(-2)
                speaker_rel.Admiration(-1)
                print(f'{self.shortname} doesn\'t believe it at all!')
            print(str)
            print(f'-->\n  {speaker_rel.trust} {speaker_rel.admiration} {speaker_rel.love}')

        print(f'2. Relationship of {self.shortname} and {subj_rel.character.shortname}\n  {subj_rel.trust} {subj_rel.admiration} {subj_rel.love}')
        subj_rel.Trust(int(action.trust * belief / 2))
        subj_rel.Admiration(int(action.admire * belief / 2))
        subj_rel.Love(int(action.love * belief / 2))
        print(f'-->\n  {subj_rel.trust} {subj_rel.admiration} {subj_rel.love}\n')

    def take_action(self):
        # choose wait, move, or gossip
        # probability array [p_wait, p_gossip, p_move, p_eavsedrop]
        p = [5, 5, 0, 5]

        # talkative people will want to tell a rumor
        p[1] += self.personality["talkative"] - 4

        # if there are people in the area, nosy people are more likely to eavsedrop
        if len(self.current_area.occupants) >= 2:
            p[3] += self.personality["nosy"] - 4
        else:
            # if the person is alone, don't gossip, but potentially move
            p[1] = 0
            #p[2] += self.personality["nosy"]- 4
            p[3] = 0

        if len(self.rumors) == 0:
            p[1] = 0

        if self.shortname == "Blair":
            p[2] = 0

        #print(f'{self.name} action probs: {p}')
        total = sum(p)
        rand = random.randint(0, total)
        action = 0
        for i in range(len(p)):
            if rand < p[i]:
                action = i
                break
            else:
                rand -= p[i]

        if action == 0:
            self.wait()
        elif action == 1:
            self.gossip()
        elif action == 2:
            self.move()
        elif action == 3:
            self.wait_to_eavsedrop()

    # do nothing
    def wait(self):
        #print(f'{self.name} waited')
        self.action_log.append("wait")

    # given an Area object
    def move(self, area=None):
        if area == None:
            area = random.choice(self.current_area.connections)
        if self.current_area != None:
            self.action_log.append("move")
            self.current_area.leave(self)
        #print(f'{self.name} moved from {self.current_area.name} to {area.name}')
        self.current_area = area
        area.enter(self)
        self.action_log.append(f'move to {self.current_area.name}')

    def select_listener(self, listeners):
        return random.choice(listeners)

    def select_rumor(self, listener, about=None):
        # based on listener, select a rumor, and modify it.
        # if listener is the player, tell them something about a specific character if specified
        # TODO: possibly make up a rumor if there is nothing to gossip about

        if len(self.rumors) > 0:
            return random.choice(self.rumors)

        return None

    # tell another character a rumor. pick rumor from ones the agent knows
    def gossip(self):
        listeners = self.current_area.occupants
        listeners.remove(self)
        listener = self.select_listener(listeners)
        self.current_area.occupants.append(self)

        rumor = self.select_rumor(listener)
        rumor = rumor.clone(rumor)
        rumor.speaker = self
        listener.hear_rumor(rumor)
        self.action_log.append(f'tell {listener.shortname} a rumor')

    def wait_to_eavsedrop(self):
        # wait until all other characeters have done their action, then find a rumor to hear
        self.eavsedropping = True
        self.action_log.append("eavsedrop")

    def eavsedrop(self):
        # find someone to listen to based on relationships
        self.eavsedropping = False
        #print(f'{self.name} eavsedrops')

    def ask(self, character, isRumor):
        if isRumor:
            # get a rumor
            rumors = []
            # filter the rumors
            for rumor in self.rumors:
                names = []
                for object in rumor.objects:
                    names.append(object.shortname)
                if character.shortname in names:
                    rumors.append(rumor)
            if len(rumors) > 0:
                return random.choice(rumors)
        else:
            self.get_relationship(character.shortname)
        return None

    def get_pronoun1(self):
        if self.pronoun == "F":
            return "she"
        elif self.pronoun == "M":
            return "he"
        else:
            return "they"

    def get_pronoun2(self):
        if self.pronoun == "F":
            return "her"
        elif self.pronoun == "M":
            return "him"
        else:
            return "them"

    def info(self, options=[]):
        if len(options) == 0:
            options = ["p", "ru", "re"]
        print("+---------ACTOR---------+")
        print(f'Name: {self.name} ({self.pronoun})')
        print(f'Current Location: {self.current_area.name}')
        if "p" in options:
            print(f'\nPERSONALITY:')
            for p in self.personality:
                num_tabs = 4 - math.floor((len(p)+3) / 4)
                if num_tabs == 1:
                    num_tabs += 1
                tabs = ""
                for t in range(num_tabs):
                    tabs += "\t"
                print(f'  {p}:{tabs}{self.personality[p]}')
        if "re" in options:
            print(f'\nRELATIONSHIPS')
            for i in range(len(self.relationships)):
                r = self.relationships[i]
                print(f'{i+1}. {r.character.shortname}')
                print(f'   trust:               {r.trust}\n' +
                      f'   admiration:          {r.admiration}\n' +
                      f'   love:                {r.love}'
                )
        if "ru" in options:
            print(f'\nRUMORS:')
            for i in range(len(self.rumors)):
                rumor = self.rumors[i]
                if rumor != None:
                    rumor.info()
        print("+-----------------------+\n")
