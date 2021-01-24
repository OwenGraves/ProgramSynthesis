from z3 import *
from constants import BV_LENGTH

class Program:
    def __init__(self, components=[]):
        self.components = components
        self.variables = []
        self.variable_number = 0

    def fresh_variable(self):
        nvar = BitVec(f'x{self.variable_number}', BV_LENGTH)
        self.variable_number += 1
        return nvar
