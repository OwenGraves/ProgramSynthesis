from z3 import *
from constants import BV_LENGTH
from collections import Counter

class Program:
    def __init__(self, components=[]):
        self.components = components
        self.variables = []
        self.variable_numbers = Counter()

    def fresh_variable(self, variable_character):
        fresh_var = BitVec(f'{variable_character}{self.variable_numbers[variable_character]}', BV_LENGTH)
        self.variable_numbers[variable_character] += 1
        self.variables.append(fresh_var) # is this necessary?
        return fresh_var

    def fresh_x_variable(self):
        return self.fresh_variable('x')
    
    def fresh_i_variable(self):
        return self.fresh_variable('i')

    def fresh_o_variable(self):
        return self.fresh_variable('o')
