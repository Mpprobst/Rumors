"""
world.py
Purpose: creates and contains characters, relationships, areas, and rumors
Is responsible for simulating time and prompting actors to take actions
"""

import string
from os import listdir
from os.path import isfile, join
import objects
from objects.actor import Actor
from objects.actor import Area

ACTORS_DIR = "../resources/actors"
AREAS_DIR = "../resources/areas"
RUMORS_DIR = "../resources/rumors"

class World():
    def __init__(self):
        self.actors = []
        self.areas = []

        # create areas
        files = [file for file in listdir(AREAS_DIR)]
        for i in range(len(files)):
            if not files[i].endswith(".txt"):
                continue
            new_area = Area(i, f'{AREAS_DIR}/{files[i]}')
            self.areas.append(new_area)

        # create actors
        files = [file for file in listdir(ACTORS_DIR)]
        for file in files:
            if not file.endswith(".txt"):
                continue
            new_actor = Actor(f'{ACTORS_DIR}/{files[i]}')
            # find starting area
            start_area = self.areas[0]
            new_actor.move(self.find_area(new_actor.starting_area))
            self.actors.append(new_actor)

        # all actors generated, initialize their relationships
        for actor in self.actors:
            others = self.actors.copy()
            others.remove(actor)
            for other in others:
                actor.start_relationship(other)

        # pick some rumors out and give them to characters
        files = [file for file in listdir(RUMORS_DIR)]
        for file in files:
            if not file.endswith(".txt"):
                continue


        for area in self.areas:
            area.info()

        for actor in self.actors:
            actor.info()


    def find_area(self, areaname):
        for area in self.areas:
            if area.name == areaname:
                return area

        print(f'ERROR: {areaname} not found')

    def find_actor(self, actorname):
        for actor in self.actors:
            if actor.name == actorname:
                return actor

        print(f'ERROR: {actorname} not found')
