from z3 import *
from constants import BV_LENGTH
from collections import Counter
from component import Component
import itertools
import operator
import copy

class Program:
    def __init__(self, num_prog_inputs=1, components=[]):
        self.variable_numbers = Counter()
        self.prog_inputs = [self.fresh_I_variable() for _ in range(num_prog_inputs)]
        self.components = copy.deepcopy(components)

    def __str__(self): # TODO write __str__ for Component
        s = ''
        for c in self.components:
            s += str(c.constraint()) + '\n'
        return s  

    def create_component(self, func, func_arity=2):
        input_vars = [self.fresh_i_variable() for _ in range(func_arity)]
        c = Component(input_vars, self.fresh_O_variable(), func)
        self.components.append(c)
        return c

    def create_add_component(self):
        return self.create_component(operator.add)

    def create_increment_component(self):
        return self.create_component(lambda x: x + 1, 1)

    def generate_encoding_constraints(self):
        P, R = [], []
        for c in self.components:
            P.extend(c.inputs)
            R.append(c.output)
        L = dict()
        for x in P + R:
            L[x] = self.fresh_l_variable()
        I_size = len(self.prog_inputs)
        M = I_size + len(self.components)
        
        psi_cons = []
        for x, y in itertools.combinations(R, 2):
            psi_cons.append(L[x] != L[y])

        psi_acyc = []
        for c in self.components:
            for x in c.inputs:
                psi_acyc.append(L[x] < L[c.output])

        psi_wfp = []
        for x in P:
            psi_wfp.append(0 <= L[x])
            psi_wfp.append(L[x] < M)
        for x in R:
            psi_wfp.append(I_size <= L[x])
            psi_wfp.append(L[x] < M)
        psi_wfp += psi_cons + psi_acyc

        s = Solver()
        s.add(psi_wfp)
        s.check()
        l_values = s.model()

        def decode():
            pass

        # Lval2Prog
        p = Program(I_size, self.components)
        for c in p.components:
            pass

        return p

    def fresh_variable(self, variable_character):
        self.variable_numbers[variable_character] += 1
        fresh_var = BitVec(f'{variable_character}{self.variable_numbers[variable_character]}', BV_LENGTH)
        return fresh_var

    def fresh_l_variable(self):
        return self.fresh_variable('l')
    
    def fresh_i_variable(self): # for component inputs
        return self.fresh_variable('i')

    def fresh_I_variable(self): # for program inputs
        return self.fresh_variable('I')

    def fresh_O_variable(self):
        return self.fresh_variable('O')
