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
        self.prog_output = BitVec('R', BV_LENGTH)
        self.components = copy.deepcopy(components)

    def __str__(self):
        return '\n'.join(str(c) for c in self.components)

    def create_component(self, func, func_arity=2):
        input_vars = [self.fresh_i_variable() for _ in range(func_arity)]
        c = Component(input_vars, self.fresh_o_variable(), func)
        self.components.append(c)
        return c

    def create_add_component(self):
        return self.create_component(operator.add)

    def create_increment_component(self):
        return self.create_component(lambda x: x + 1, 1)

    def generate_constrained_program(self):
        P, R = [], []
        O = []
        for c in self.components:
            P.extend(c.inputs)
            R.append(c.output)
            O.append(self.fresh_O_variable())
        L = dict()
        for x in P + R:
            L[x] = self.fresh_l_variable()
        I_size = len(self.prog_inputs)
        M = I_size + len(self.components)

        decode = dict() # maps integer l value to variable
        for i in range(I_size):
            decode[i] = self.prog_inputs[i]
        for i in range(I_size, M):
            decode[i] = O[i - I_size] 
        
        psi_cons = []
        for x, y in itertools.combinations(R, 2):
            psi_cons.append(L[x] != L[y])

        psi_acyc = []
        for c in self.components:
            for x in c.inputs:
                psi_acyc.append(L[x] < L[c.output])

        psi_wfp = [] # syntactic well-formedness constraints
        for x in P:
            psi_wfp.append(0 <= L[x])
            psi_wfp.append(L[x] < M)
        for x in R:
            psi_wfp.append(I_size <= L[x])
            psi_wfp.append(L[x] < M)
        psi_wfp += psi_cons + psi_acyc

        psi_conn = []
        for i, input in enumerate(self.prog_inputs):
            L[input] = i
        L[self.prog_output] = M - 1
        for x, y in itertools.combinations(P + R + self.prog_inputs + [self.prog_output], 2):
            psi_conn.append(Implies(L[x] == L[y], x == y))

        phi_lib = []
        for c in self.components:
            phi_lib.append(c.constraint())

        result = 10
        output_constraint = result == self.prog_output
        input1 = 4
        input1_constraint = input1 == self.prog_inputs[0]
        print(input1_constraint)
        print(output_constraint)

        s = Solver()
        s.add(psi_wfp)
        s.add(psi_conn)
        s.add(phi_lib)
        s.add(output_constraint)
        s.add(input1_constraint)
        # for testing
        # s.add(BitVec('l4', BV_LENGTH) == 2)
        # s.add(BitVec('l1', BV_LENGTH) != 0)
        # print(psi_wfp)
        # print(psi_conn)
        # print(phi_lib)

        s.check()
        l_values = s.model()
        print(self)
        print(l_values)

        # Lval2Prog
        p = Program(I_size, self.components)
        for c in p.components:
            for i in range(len(c.inputs)):
                c.inputs[i] = decode[int(str(l_values[L[c.inputs[i]]]))]
            c.output = decode[int(str(l_values[L[c.output]]))]
        p.components.sort()

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

    def fresh_o_variable(self):
        return self.fresh_variable('o')

    def fresh_O_variable(self):
        return self.fresh_variable('O')