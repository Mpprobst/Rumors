"""
Area.py
Purpose: Implements data structures and mechanics of an area in town
"""

import string

class Area():
    def __init__(self, _id, filename):
        self.id = _id
        self.name = ""
        self.capacity = ""
        self.noise = ""
        self.occupants = []
        self.connections = []

        # initialize the area
        f = open(filename, "r")
        for line in f:
            line_array = line.split()
            item = line_array[0]
            value = " ".join(line_array[1:])
            if item == "name":
                self.name = value
            elif item == "cap":
                self.capacity = int(value)
            elif item == "noise":
                self.noise = int(value)
            elif item == "connections":
                area = ""
                idx = 0
                while idx < len(value):
                    if value[idx] == ',':
                        self.connect_area(area)
                        area = ""
                        idx += 1
                    else:
                        area += value[idx]
                    idx += 1
                self.connect_area(area)


    def is_full(self):
        return self.capacity >= len(self.occupants)

    # character is the name of the character entering the area
    def enter(self, character):
        self.occupants.append(character)

    # character is the name of the character leaving the area
    def leave(self, character):
        self.occupants.remove(character)

    def occupants(self):
        return self.occupants

    # area is the name of the area connected to this one
    def connect_area(self, area):
        if area not in self.connections:
            self.connections.append(area)

    def get_connections(self):
        return self.connections

    def info(self, options=None):
        if options == None:
            options = ["o", "c"]
        print(f'+---------AREA {self.id}--------+')
        print(f'Name: {self.name}')
        print(f'Noise Factor: {self.noise}')
        print(f'Capacity: {len(self.occupants)} of {self.capacity}')
        if "o" in options:
            print(f'\nOCCUPANTS:')
            for o in self.occupants:
                print(f'  {o.name}')
        if "c" in options:
            print(f'\nCONNECTED AREAS:')
            for c in self.connections:
                print(f'  {c.name}')
        print("+-----------------------+\n")
        return 0
