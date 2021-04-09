"""
world.py
Purpose: creates and contains characters, relationships, areas, and rumors
Is responsible for simulating time and prompting actors to take actions
"""

import string
from os import listdir
from os.path import isfile, join
import objects
from objects.area import Area
from objects.actor import Actor
from objects.rumor import Rumor

ACTORS_DIR = "../resources/actors"
AREAS_DIR = "../resources/areas"
RUMORS_DIR = "../resources/rumors"
SIM_TIME = 2

class World():
    def __init__(self):
        self.actors = []
        self.areas = []
        self.initial_rumors = []
        self.default_actor = None
        self.default_area = None
        self.time = 0

        self.init_areas()
        self.connect_areas()
        self.init_actors()
        self.init_relationships()
        self.init_rumors()

        self.info()

        self.simulate()

    def play(self):
        # wait for player to input, then do a time_step
        done = False
        while not done:
            in_val = input("What do you do? ")
            args = in_val.split()
            if len(args) > 0:
                if args[0] == "quit":
                    done = True
                    print("Thanks for playing!")
                    break
                elif args[0] == "help":
                    print("+--------------------HELP--------------------+")
                    print(f'Here is a list of the valid commands:\n' +
                          f' - <character1>, <question> <character2> <?>: talk to a specific character about something \n' +
                          f'\t<question>: ask anyting! Say things like: \"do you like\", \"how do you feel about\" \"tell me about\"\n'+
                          f'\t\tbut if the action is too complex for the character, they will not understand it\n' +
                          f'\t <character2>: a specific character pertaining to your question.\n\t\tThis can be the same as <character1> if you enter \"yourself\".\n\t\tYou can also use yourself as the second character.\n\t\tIf the character doesn\'t exist, the character will let you know.\n' +
                          f'\t<?>: put a question mark if you want to ask a question. Otherwise it is assumed you are stating a fact. \n' +
                          f' - gossip <character> <rumor>: tell a character a rumor. if <character> is empty, Blair is default\n' +
                          f'\t<rumor>: Say anything! Only valid actions and characters will be registered.\n' +
                          f'\tlist of valid actions:\n' +
                          f' - look: get info on your current area\n' +
                          f' - info <shortname> <options separated by spaces>: get info about something.\n\t\tenter the shortname of the item of interest or \"all\" to get all info\n' +
                          f'\t<character> p re ru: print character info. p - personality, re - relationships, ru - rumors known.\n' +
                          f'\t<area> o c: print area info. o - occupants, c - connected areas.\n'
                          f'\t you can enter no additional options to get all info about the designated object\n' +
                          f' - quit: ends the experience\n' +
                          f' - help: print the help menu\n'
                    )
                    print("+---------------------------------------------+")
                elif args[0][len(args[0])-1] == ",":
                    # we are prompting a character for something
                    character1 = self.find_actor(args[0].replace(',', ''))
                    char2 = args[len(args)-1]
                    question = " ".join(args[2:len(args)-2])
                    isQ = False
                    if '?' in char2:
                        isQ = True
                        char2 = char2.replace('?', '')

                    character2 = self.find_actor(char2)

                    if isQ:
                        if "tell" in question or "know" in question:
                            rumor = character1.ask(character2, True)
                            if rumor != None:
                                rumor.info()
                            else:
                                print(f'{character1.name}: Sorry. I don\'t know anything about {char2}')

                        else:
                            relationship = character1.ask(character2, False)
                            if relationship != None:
                                print(f'{character1.shortname}: {relationship.info()}')
                            else:
                                print(f'{character1.shortname}: Sorry. I don\'t know anything about {char2}')

                    else:
                        # parse the rumor
                        #character1.hear_rumor()
                        print("TODO: Parse a rumor from user")

                elif args[0] == "gossip":
                    rumorIdx = 2
                    character1 = self.find_actor(args[1])
                    if character1 == self.default_actor:
                        character1 = self.find_actor("Blair")
                        rumorIdx = 1
                    rumor = " ".join(args[rumorIdx:])
                    # parse the rumor
                elif args[0] == "look":
                    area = self.find_area("Saloon")
                    patrons = []
                    for a in area.occupants:
                        patrons.append(a.shortname)
                    if len(patrons) > 1:
                        patrons[len(patrons)-1] = "and " + patrons[len(patrons)-1]
                    patrons = ", ".join(patrons)
                    print(f'You are sitting at the bar in the {area.name}. \nIn the saloon is: {patrons}')
                    continue
                elif args[0] == "info":
                    if args[1] == "all":
                        self.info()
                    else:
                        obj = self.find_actor(args[1])
                        if obj == self.default_actor:
                            obj = self.find_area(args[1])
                            if obj == self.default_area:
                                continue
                        obj.info(args[2:])
                        continue
            self.time_step()

    # simulate time before the experience begins
    def simulate(self):
        while self.time < SIM_TIME:
            self.time_step()
        self.play()

    def time_step(self):
        # process player input if needed
        #print(f'time step: {self.time}')
        eavsedroppers = []
        for actor in self.actors:
            actor.take_action()
            if actor.eavsedropping:
                eavsedroppers.append(actor)

        for e in eavsedroppers:
            e.eavsedrop()
        self.time += 1
        print("")
        return 0

    # create areas
    def init_areas(self):
        files = [file for file in listdir(AREAS_DIR)]
        for i in range(len(files)):
            if not files[i].endswith(".txt"):
                continue
            new_area = Area(i, f'{AREAS_DIR}/{files[i]}')
            if new_area.name == "Placeholder":
                self.default_area = new_area
            else:
                self.areas.append(new_area)
        return 0

    def connect_areas(self):
        for area in self.areas:
            connections = []    # new array to give references to area objects
            for c in area.get_connections():
                other = self.find_area(c)
                connections.append(other)

            area.connections = connections
        return 0

    # create actors
    def init_actors(self):
        files = [file for file in listdir(ACTORS_DIR)]
        for file in files:
            if not file.endswith(".txt"):
                continue
            new_actor = Actor(f'{ACTORS_DIR}/{file}')
            new_actor.move(self.find_area(new_actor.starting_area))
            if new_actor.name == "Default Character":
                self.default_actor = new_actor
            else:
                self.actors.append(new_actor)
        return 0

    # all actors generated, initialize their relationships
    def init_relationships(self):
        for actor in self.actors:
            others = self.actors.copy()
            others.remove(actor)
            for other in others:
                actor.start_relationship(other)
        return 0

    # pick some rumors out and give them to characters
    def init_rumors(self):
        files = [file for file in listdir(RUMORS_DIR)]
        for file in files:
            if not file.endswith(".txt"):
                continue
            rumor = Rumor(file=f'{RUMORS_DIR}/{file}', world=self)
            rumor.speaker.hear_rumor(rumor)
            rumor.listener.hear_rumor(rumor)
            self.initial_rumors.append(rumor)

        return 0

    def find_area(self, areaname):
        for area in self.areas:
            if area.name == areaname:
                return area
        #print(f'ERROR: {areaname} not found')
        return self.default_area

    def find_actor(self, actorname):
        for actor in self.actors:
            if actor.name == actorname or actor.shortname == actorname:
                return actor
        print(f'ERROR: {actorname} not found')
        return self.default_actor

    def info(self):
        for area in self.areas:
            area.info()

        for actor in self.actors:
            actor.info()

        print("initial rumors")
        for rumor in self.initial_rumors:
            rumor.info()
