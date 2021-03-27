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

class World():
    def __init__(self):
        self.actors = []
        self.areas = []
        self.initial_rumors = []
        self.default_actor = None
        self.default_area = None

        self.init_areas()
        self.init_actors()
        self.init_relationships()
        self.init_rumors()

        self.info()

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

    # create actors
    def init_actors(self):
        files = [file for file in listdir(ACTORS_DIR)]
        for file in files:
            if not file.endswith(".txt"):
                continue
            new_actor = Actor(f'{ACTORS_DIR}/{file}')
            new_actor.move(self.find_area(new_actor.starting_area))
            if new_actor.name == "Default":
                self.default_actor = new_actor
            else:
                self.actors.append(new_actor)
    # all actors generated, initialize their relationships
    def init_relationships(self):
        for actor in self.actors:
            others = self.actors.copy()
            others.remove(actor)
            for other in others:
                actor.start_relationship(other)

    # pick some rumors out and give them to characters
    def init_rumors(self):
        files = [file for file in listdir(RUMORS_DIR)]
        for file in files:
            if not file.endswith(".txt"):
                continue
            self.initial_rumors.append(Rumor(f'{RUMORS_DIR}/{file}', self))

    def find_area(self, areaname):
        for area in self.areas:
            if area.name == areaname:
                return area
        print(f'ERROR: {areaname} not found')
        return self.default_area

    def find_actor(self, actorname):
        for actor in self.actors:
            if actor.name == actorname:
                return actor
        print(f'ERROR: {actorname} not found')
        return self.default_actor

    def info(self):
        for area in self.areas:
            area.info()

        for actor in self.actors:
            actor.info()

        for rumor in self.initial_rumors:
            rumor.info()
