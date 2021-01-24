from z3 import *
from constants import BV_LENGTH
from collections import Counter
from component import Component
import itertools
import operator

class Program:
    def __init__(self, components=[]):
        self.components = components
        self.variable_numbers = Counter()

    def create_component(self, func, func_arity=2):
        input_vars = [self.fresh_I_variable() for _ in range(func_arity)]
        c = Component(input_vars, self.fresh_O_variable(), func)
        self.components.append(c)
        return c

    def create_add_component(self):
        return self.create_component(operator.add)

    def temp_name(self): # TODO refactor this method
        N = len(self.components)
        # should these be created as part of a component?
        P, R, L = [], [], []
        for _ in range(N):
            P.append(self.fresh_I_variable())
            R.append(self.fresh_O_variable())
            L.append(self.fresh_l_variable())
            L.append(self.fresh_l_variable())
        psi_cons = []
        for x, y in itertools.combinations(R, 2):
            psi_cons.append(x == y)
        return

    def fresh_variable(self, variable_character):
        fresh_var = BitVec(f'{variable_character}{self.variable_numbers[variable_character]}', BV_LENGTH)
        self.variable_numbers[variable_character] += 1
        return fresh_var

    def fresh_l_variable(self):
        return self.fresh_variable('l')
    
    def fresh_I_variable(self):
        return self.fresh_variable('I')

    def fresh_O_variable(self):
        return self.fresh_variable('O')
