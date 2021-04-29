"""
action.py
Purpose: provide data structure for actions in rumors and how they affect relationships
also suggests how the action should be used.
"""

class Action():
    def __init__(self, file):
        self.name = ""

        # requirements for this action between the involved characters.
        # Determines how believable it is and can be used by evil characters to tell lies
        self.r_trust = 5    # how much trust is needed between two characters
        self.r_admire = 5   # how much respect is needed between two characters. Someone who respects another wont try to discredit them
        self.r_love = 5     # how much love is needed between two characters. People who like each other won't likely fight

        # descriptors of the action
        self.morality = 5   # how good or bad the action is. Ex stealing is bad (0), generosity is good (9)
        self.taboo = 5      # how scandalous the action is. Ex cheating on a significant other (9) dating someone (0)

        # affectors on relationships. Character's who hear about this will change their opinion of the involved characters
        self.subject_trust = 1
        self.subject_admire = 1
        self.subject_love = 1

        self.object_trust = 1
        self.object_admire = 1
        self.object_love = 1

        if file != None:
            f = open(file, "r")
            i = 0
            for line in f:
                line = line.split()
                if i == 0:
                    self.name = " ".join(line[:])
                elif i == 1:

                    self.r_trust = int(line[0])
                    self.r_admire = int(line[1])
                    self.r_love = int(line[2])
                elif i == 2:
                    self.morality = int(line[0])
                    self.taboo = int(line[1])
                elif i == 3:
                    self.subject_trust = int(line[0])
                    self.subject_admire = int(line[1])
                    self.subject_love = int(line[2])
                elif i == 4:
                    self.object_trust = int(line[0])
                    self.object_admire = int(line[1])
                    self.object_love = int(line[2])
                i += 1

    def sum_sub(self):
        return self.subject_trust + self.subject_trust + self.subject_love

    def sum_obj(self):
        return self.object_trust + self.object_trust + self.object_love

    def info(self):
        print(f'-----ACTION-----\n'+
              f'{self.name}\n' +
              f'requirements\n  trust:\t{self.r_trust}\n  admire:\t{self.r_admire}\n  love:\t{self.r_love}  \n' +
              f'descriptors\n  moral:\t{self.morality}\n  taboo:\t{self.taboo}  \n' +
              f'affector(sub,obj)\n  trust:\t{self.subject_trust}, {self.object_trust}\n  admire:\t{self.object_admire}, {self.subject_trust}\n  love:\t\t{self.subject_love}, {self.object_love}  \n' +
              f'-----------------\n'
        )
