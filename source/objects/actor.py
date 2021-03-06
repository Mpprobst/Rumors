"""
actor.py
Purpose: Implements the data structures and mechanics of an actor
"""

import copy
import sys
import string
from objects.relationship import Relationship
from objects.area import Area
from objects.rumor import Rumor
import math
import random

class Actor():
    # assumes it is given a .txt filename
    def __init__(self, filename=None, world=None):
        self.name = "You, the Player"
        self.shortname = "You"
        self.pronoun = "T"
        self.description = ""               # a description of the character
        self.world = world
        self.eavsedropping = False
        self.starting_area = ""
        self.current_area = None
        self.rumors = []
        self.action_log = []
        self.relationships = []     # list of relationships the character has with all other characters. TODO: find where to initialize this list
        # dictionary of personality traits that influence the characters decisions. Always a value between 0 and 9
        self.personality = { "trustworthy" : 5, # how likely others are to tell this character a rumor
                             "talkative" : 5,   # how likely the character is to tell a rumor
                             "gullible" : 5,    # how likely the character is to believe a rumor
                             "nosy" : 5,        # how likely the character is to seek out rumors from others
                             "loyalty" : 5,     # how likely a character is to tell a bad rumor about a character they like
                             "fame" : 0,        # how well known the character is
                             "morality" : 5,    # how 'good' the character is. this influences the likelihood to mutate a rumor. 0-3 is evil, 4-5 is neutral, 6-9 is good
                             "memory" : 5,      # how good a character is at retelling a rumor
                             "perception" : 5,  # how good a character is at understanding a rumor
                             "opinion" : 5      # what characters generally think about this one
                            }

        # initialize the character
        if filename != None:
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
                elif item == "description":
                    self.description = value
                else:
                    print(f'WARNING: trait {item} is not a valid trait')

    def start_relationship(self, char):
        self.relationships.append(Relationship(self, char))

    def get_relationship(self, name):
        for r in self.relationships:
            if r.character.shortname == name:
                return r

    def hear_rumor(self, rumor, speaker=None, force_believe=False):
        #print(f'{self.shortname} hearing rumor {rumor.id}')
        if rumor == None:
            return
        existing_rumor = None
        unique_rumor = True
        r_idx = 0
        for r in self.rumors:
            if r.exists(rumor):
                # I've heard this before
                rumor.id = r.id
                existing_rumor = r
                break
            r_idx += 1

        if speaker == None:
            speaker = self
        rumor.listener = self
        #rumor.info(1)

        # TODO: now adjust relationships
        # find the action object in the rumor
        if isinstance(rumor.action, str):
            return

        #if rumor.action == None:
        #    return

        action = rumor.action#self.world.find_action(rumor.action.name)
        # based on personality, choose how much to believe the rumor
        belief = 1
        subj_rel = self.get_relationship(rumor.subject.shortname)
        obj_rels = []
        for obj in rumor.objects:
            obj_rels.append(self.get_relationship(obj.shortname))

        #if action == None:
        #    return

        speaker_rel = self.get_relationship(rumor.speaker.shortname)
        s = ""
        if speaker_rel != None:
            s = f'1. Relationship of {self.shortname} and {speaker_rel.character.shortname}\n  {speaker_rel.trust} {speaker_rel.admiration} {speaker_rel.love}'

        if not force_believe:
            trust_val = 0
            admire_val = 0
            love_val = 0
            if subj_rel != None:
                trust_val = self.personality["gullible"] - (5 - int(subj_rel.trust/10))
                admire_val = int(subj_rel.admiration/10) - (5 - self.personality["loyalty"])
                love_val = int(subj_rel.love/10)
                if rumor.action.morality >= 5:
                    belief += 1 if trust_val >= rumor.action.r_trust else 0
                    belief += 1 if admire_val >= rumor.action.r_admire else 0
                    belief += 1 if love_val >= rumor.action.r_love else 0
                else:
                    belief += 1 if trust_val < rumor.action.r_trust else 0  # gullible characters believe things
                    belief += 1 if admire_val < rumor.action.r_admire else 0 # if low resepect and disloyal
                    belief += 1 if love_val < rumor.action.r_love else 0 # if character hates other, believe it

            #belief += random.randint(0, 1)
            """print(f'ACTION: {action.name} is {"good" if rumor.action.morality > 5 else "bad"}\n'+
                  f'\ttrust: {trust_val} >= {action.r_trust}\n'+
                  f'\tadmire: {admire_val} >= {action.r_admire}\n'+
                  f'\tlove: {love_val} >= {action.r_love}\n'+
                  f'Belief: {belief}'
            )
            print(f'{rumor.speaker.shortname} is telling {self.shortname} that {rumor.subject.shortname} {rumor.action.name} {rumor.objects[0].shortname}')#q belief: {belief}')
            """
            if speaker_rel != None:
                if belief > 3:
                    belief = 2
                    speaker_rel.Trust(5)
                    speaker_rel.Love(3)
                    #rumor.new_version(rumor.copy(), self.world)
                    if existing_rumor == None:
                        clone = rumor.copy()
                        clone.versions.append(clone.copy())
                        self.rumors.append(clone)
                    else:
                        unique_rumor = existing_rumor.new_version(rumor, self.world)
                    #print(f'{self.shortname} really believes it!\n')
                elif belief > 2:
                    belief = 1
                    speaker_rel.Trust(2)
                    #rumor.new_version(rumor.copy(), self.world)
                    if existing_rumor == None:
                        clone = rumor.copy()
                        clone.versions.append(clone.copy())
                        self.rumors.append(clone)
                    else:
                        unique_rumor = existing_rumor.new_version(rumor, self.world)
                    #print(f'{self.shortname} believes it.\n')
                elif belief > 1:
                    belief = 0
                    speaker_rel.Trust(-3)
                    #print(f'{self.shortname} doesn\'t believe it!\n')
                else:
                    belief = 0
                    speaker_rel.Trust(-7)
                    speaker_rel.Admiration(-4)
                    #print(f'{self.shortname} doesn\'t believe it at all!\n')
                #print(s)
                #print(f'-->\n  {speaker_rel.trust} {speaker_rel.admiration} {speaker_rel.love}')
        else:
            if speaker_rel != None:
                speaker_rel.Trust(2)
            #rumor.new_version(rumor.copy(), self.world)
            if existing_rumor == None:
                clone = rumor.copy()
                clone.versions.append(clone.copy())
                self.rumors.append(clone)
            else:
                unique_rumor = existing_rumor.new_version(rumor, self.world)
        # relationship between the listener and the subject and objects need to change based on
        # their respective current relationships and the affectors of the action
        # ex: if someone the listener doesn't like does something intimate with someone
        # the listener does like, then the listener should like the person they like less.
        # if the listener loves the one character and hates the other, the listener should
        # hate the person they hate even more if the action between them is nefarious.
        # if the action between the subject and objects is a good action, the listener might
        # begin to like the character they hate. Special case is that there is nothing wrong with
        # love, but if the subject and object are in love and the listener loves one of them
        # then they can be jealous and begin to like them less.

        #print(f'2. Relationship of {self.shortname} and {subj_rel.character.shortname}\n  {subj_rel.trust} {subj_rel.admiration} {subj_rel.love}')

        # listener should update their opinions on the characters invloved in the rumor
        # based on how they align with thier values

        # PRODUCE RESPONSE #
        morals_align = True
        if rumor.action.morality >= 5 and self.personality["morality"] < 5:
            morals_align = False
        if rumor.action.morality < 5 and self.personality["morality"] >= 5:
            morals_align = False

        like_ct = 0
        for rel in obj_rels:
            if rel == None:
                continue
            if rel.likes():
                like_ct += 1

        likes_obj = like_ct >= len(rumor.objects) / 2
        likes_sub = True
        if subj_rel != None:
             subj_rel.likes()

        response = f'{self.shortname}: '
        if len(rumor.versions) > 0:
            response += f'Yeah I heard that from {rumor.versions[len(rumor.versions)-1].speaker.shortname}. ' if not unique_rumor else ""
        dont = "doesn\'t" if rumor.objects[0].pronoun != 'T' else "don\'t"
        if not morals_align:
            response += f'I\'m not surprised {rumor.subject.shortname} would do that.' if likes_sub else f'I can\'t believe {rumor.subject.get_pronoun1()} would do that!'
            response += f'But poor {rumor.objects[0].shortname}... {rumor.objects[0].get_pronoun1()} {dont} deserve that.' if likes_obj else f'{rumor.objects[0].shortname} got what they deserved!'
            belief *= -1
        else:
            response += f'I\'m glad {rumor.subject.get_pronoun1()} did that!' if likes_sub else f'That\'s surprising!'
            response += f' {rumor.objects[0].shortname} deserved that!' if not likes_obj else f' Good for {rumor.objects[0].shortname}!'
        #elif abs(moral) >= 5: # someone with perfect morals (9) and a neutral action (5) shouln't think too differently
        #    belief *= -1
        if not unique_rumor:
            belief = 0
        response += f' ({belief})'
        if subj_rel != None:
            subj_rel.Trust(int(action.subject_trust * belief / 2))
            subj_rel.Admiration(int(action.subject_admire * belief / 2))
            subj_rel.Love(int(action.subject_love * belief / 2))

        for rel in obj_rels:
            if rel == None:
                continue
            rel.Trust(int(action.object_trust * belief / 2))
            rel.Admiration(int(action.object_admire * belief / 2))
            rel.Love(int(action.object_love * belief / 2))

        if force_believe:
            print(response)
        return None
        #print(f'-->\n  {subj_rel.trust} {subj_rel.admiration} {subj_rel.love}\n')

    def take_action(self):
        self.gossip()
        return None
        # choose wait, move, or gossip
        # probability array [p_wait, p_gossip, p_move, p_eavsedrop]
        p = [5, 5, 0, 0]    # TODO: change p_move in final version when there are more characters

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
        if total <= 0:
            total = 1
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

    def mutate_character(self, og_char, likes):
        #print("mutate character")
        rels = self.relationships.copy()
        for r in rels:
            if likes and not r.likes():
                rels.remove(r)
            elif not likes and r.likes():
                rels.remove(r)

        if len(rels) > 0:
            rel = random.choice(rels)
            return rel.character
        return og_char

    def mutate_action(self, og_action, like_sub, like_obj):
        #print("mutate action")
        sub_thresh = og_action.sum_sub()
        obj_thresh = og_action.sum_obj()
        actions = self.world.actions.copy()

        for a in actions:
            sub_aff = a.sum_sub()
            obj_aff = a.sum_obj()

            # subject is liked, remove immoral or worse actions
            if like_sub and (a.morality < 4 or sub_thresh > sub_aff):
                actions.remove(a)
            # subject is hated, remove good or better actions
            elif not like_sub and (a.morality > 5 or sub_thresh < sub_aff):
                actions.remove(a)
            # object is liked, remove immoral or worse actions
            elif like_obj and (a.morality < 4 or obj_thresh > obj_aff):
                actions.remove(a)
            # object is hated, remove good or better actions
            elif not like_obj and (a.morality > 5 or obj_thresh < obj_aff):
                actions.remove(a)

        mutate_action = og_action
        if len(actions) > 0:
            mutate_action = random.choice(actions)

        return mutate_action

    def select_rumor(self, listener, about=None):
        # if listener is the player, tell them something about a specific character if specified
        rumors = []
        if about != None:
            for rumor in self.world.rumors.copy():
                object_names = []
                for obj in rumor.objects:
                    object_names.append(obj.shortname)
                if rumor.subject.shortname == about.shortname or about.shortname in object_names:
                    rumors.append(rumor)

        # based on listener, select a rumor
        if listener != None:
            listener_rel = self.get_relationship(listener.shortname)
            if listener_rel == None:
                return None

            t_thresh = listener_rel.trust/10          # threshold for action trust
            a_thresh = listener_rel.admiration/10     # threshold for action admiration
            l_thresh = listener_rel.love/10           # threshold for action love
            # 2 or more thresholds must be exceeded to tell the rumor
            for rumor in rumors:
                thresh_ct = 0
                if rumor.action.r_trust <= t_thresh:
                    thresh_ct += 1
                if rumor.action.r_admire <= a_thresh:
                    thresh_ct += 1
                if rumor.action.r_love <= l_thresh:
                    thresh_ct += 1

                thresh_ct += random.randint(0,1)
                if thresh_ct < 2:
                    rumors.remove(rumor)

        ru = None
        if len(rumors) > 0:
            ru = random.choice(rumors)
            if listener.shortname == "You":
                return ru
        else:
            #print(f'{self.shortname} is making something up...')
            # make something up
            ru = Rumor(id=len(self.world.rumors)+1, speaker=self, listener=listener, location=random.choice(self.world.areas))
            like_s = True if random.random() < 0.5 else False
            like_o = True if random.random() < 0.5 else False
            valid_actors = self.world.actors.copy()
            for a in valid_actors:
                if a.shortname == self.shortname or a.shortname == listener.shortname or a.shortname == "You":
                    valid_actors.remove(a)

            ru.objects = list()
            rand_actor = random.choice(valid_actors)
            ru.objects.append(rand_actor)
            valid_actors.remove(rand_actor)
            rand_actor = random.choice(valid_actors)
            ru.subject = rand_actor
            ru.action = random.choice(self.world.actions)
            self.mutate_character(ru.objects[0], like_o)
            self.mutate_character(ru.subject, like_s)
            self.mutate_action(ru.action, like_s, like_o)
            ru.versions.append(ru.copy())

            new_rumor = True
            for rumor in self.world.rumors:
                if rumor.exists(ru):
                    new_rumor = False
                    ru = rumor.copy()
                    break
            if new_rumor:
                self.world.rumors.append(ru)
            #ru.info(1)
            #print("THAT WAS A LIE")

        sub_rel = self.get_relationship(ru.subject.shortname)
        obj_rels = []

        if sub_rel == None:
            return ru

        like_ct = 0
        for obj in ru.objects:
            rel = self.get_relationship(obj.shortname)
            if rel == None:
                continue
            obj_rels.append((rel, rel.likes()))
            if rel.likes():
                like_ct += 1

        likes_obj = like_ct >= len(ru.objects) / 2
        likes_sub = sub_rel.likes()
        # if loyal:
        if self.personality["loyalty"] >= 5 and ru.action.morality <= 3:
            # if character likes a character that would be negatively affected, choose a better action
            if likes_sub:
                if self.personality["morality"] < 5:
                    # change the character that is negatively affected with one they dont like.
                    ru.subject = self.mutate_character(ru.subject, likes_sub)
                else:
                    # choose action that has sum(newaction.affectors) > sum(oldaction.affectors)
                    ru.action = self.mutate_action(ru.action, likes_sub, likes_obj)
            if likes_obj:
                if self.personality["morality"] < 5:
                    # change the character that is negatively affected with one they dont like.
                    for o in ru.objects:
                        o = self.mutate_character(o, o.likes())
                else:
                    # choose action that has sum(newaction.affectors) > sum(oldaction.affectors)
                    ru.action = self.mutate_action(ru.action, likes_sub, likes_obj)

        rand = random.randint(0, 9)
        twist = (9-self.personality["morality"])
        if rand < twist:            # if ill-moraled:
            ru.action = self.mutate_action(ru.action, likes_sub, likes_obj)
            """
            if likes_obj and likes_sub:
                # if the character likes all characters involved in the rumor, they will want them to look good
                # choose an action where avg(affectors) > 1 and morality >= 5
                ru.action = self.mutate_action(ru.action, likes_sub, likes_obj)
            elif likes_obj and not likes_sub:
                # if the character hates the subject and likes the objects,
                # twist action s.t. sum(subject_affectors) < sum(avg(object_affectors))
                ru.action = self.mutate_action(ru.action, likes_sub, likes_obj)
            elif not likes_obj and likes_sub:
                # if the character likes the subject and hates the objects,
                # twist action s.t. sum(subject_affectors) > sum(avg(object_affectors))
                ru.action = self.mutate_action(ru.action, likes_sub, likes_obj)
            else:
                # if the character hates all characters involved in the rumor, they will want them to all look bad.
                # choose action where avg(affectors) > 1 and morality < 5
                ru.action = self.mutate_action(ru.action, likes_sub, likes_obj)
            """

        # if the character doesn't like or respect the object or subject of the rumor, and are ill moraled,
        # then they are more likely to twist the rumor. But if they like the objects,
        # and are loyal, they will not intentionally twist the rumor

        return ru

    # tell another character a rumor. pick rumor from ones the agent knows
    def gossip(self):
        #print(f'{self.shortname} is gossiping')
        listeners = []
        occupants = self.current_area.occupants.copy()
        for o in occupants:
            for a in self.world.available_actors:
                if a.shortname == o.shortname and a.shortname != "You" and a.shortname != self.shortname:
                    listeners.append(o)

        #s=""
        #for a in listeners:
        #    s += f'{a.shortname}, '
        #print(f'{self.shortname} can interact with: {s}')
        if len(listeners) == 0:
            self.wait()
            return 0
        listener = self.select_listener(listeners)
        #print(f'{self.shortname} interacted with {listener.shortname}')
        self.world.occupy_actor(listener)
        self.world.occupy_actor(self)
        #self.current_area.occupants.append(self)

        rumor = self.select_rumor(listener)
        if rumor == None:
            #print(f'no suitable rumor found')
            return
        rumor = rumor.copy()
        rumor.speaker = self
        listener.hear_rumor(rumor, self)
        self.action_log.append(f'tell {listener.shortname} a rumor')
        return

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
            """
            # get a rumor
            rumors = []
            # filter the rumors
            for rumor in self.rumors:
                names = []
                for object in rumor.objects:
                    names.append(object.shortname)
                names.append(rumor.subject.shortname)
                if character.shortname in names:
                    rumors.append(rumor)
            if len(rumors) > 0:
            """
                #return random.choice(rumors)
            return self.select_rumor(self.world.player_actor, character)
        else:
            return self.get_relationship(character.shortname)
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

    def introduce(self):
        if self.description == "":
            self.description = f'Hi, I\'m {self.shortname}, {self.get_pronoun1()}/{self.get_pronoun2()}'
        print(f'{self.shortname}: {self.description}')

    def info(self, options=[]):
        if len(options) == 0:
            options = ["p", "ru", "re"]
        print("+---------ACTOR---------+")
        print(f'Name: {self.name} ({self.get_pronoun1()}/{self.get_pronoun2()})')
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
                    print(f'RUMOR: {i+1}')
                    rumor.info(1)

        print("+-----------------------+\n")
