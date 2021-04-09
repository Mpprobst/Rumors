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
        print(f'time step: {self.time}')
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
            self.initial_rumors.append(Rumor(file=f'{RUMORS_DIR}/{file}', world=self))
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
        #print(f'ERROR: {actorname} not found')
        return self.default_actor

    def info(self):
        for area in self.areas:
            area.info()

        for actor in self.actors:
            actor.info()

        print("initial rumors")
        for rumor in self.initial_rumors:
            rumor.info()
