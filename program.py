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

    def generate_encoding_constraints(self):
        P, R = [], []
        for c in self.components:
            P.extend(c.inputs)
            R.append(c.output)
        L = dict()
        for x in P + R:
            L[x] = self.fresh_l_variable()
        
        encode, decode = dict(), dict()
        for i, var in enumerate(P):
            encode[var], decode[i] = i, var
        for i, var in enumerate(R): # should this represent assignment statements or output variables?
            encode[var], decode[i + len(P)] = i + len(P), var
        M = len(P) + len(R) # len(P) = |I|, len(R) = N
        
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
            psi_wfp.append(len(P) <= L[x])
            psi_wfp.append(L[x] < M)
        psi_wfp += psi_cons + psi_acyc

        print(decode[0])
        print(decode[2])
        # TODO figure out Lval2Prog encoding and if examples in prog_synth make sense
        return psi_wfp

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
