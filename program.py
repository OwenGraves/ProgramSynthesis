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
        self.prog_output = BitVec('result', BV_LENGTH)
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

    def generate_constrained_program_1IO(self, inputs, output):
        if not isinstance(inputs, list):
            inputs = [inputs]
        return self.generate_constrained_program([(inputs, output)])

    def generate_constrained_program(self, list_inputs_outputs):
        P, R = [], []
        for c in self.components:
            P.extend(c.inputs)
            R.append(c.output)
        L = dict()
        for x in P + R:
            L[x] = self.fresh_l_variable()
        I_size = len(self.prog_inputs)
        M = I_size + len(self.components)

        decode = dict() # maps integer l value to variable
        for i in range(I_size):
            decode[i] = self.prog_inputs[i]
        for i in range(I_size, M):
            decode[i] = R[i - I_size] 
        
        # syntactic well-formedness constraints
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

        # semantic constraints
        phi_lib = []
        for c in self.components:
            phi_lib.append(c.constraint())
        psi_conn = []
        pinputs = []
        poutputs = []
        for j in range(len(list_inputs_outputs)):
            pinputs.append([self.append_number_variable(x, j) for x in self.prog_inputs])
            poutputs.append(self.append_number_variable(self.prog_output, j))
            for i, input in enumerate(pinputs[j]):
                L[input] = i
            L[poutputs[j]] = M - 1
            for x, y in itertools.combinations(P + R + pinputs[j] + [poutputs[j]], 2):
                psi_conn.append(Implies(L[x] == L[y], x == y))

        s = Solver()
        s.add(psi_wfp)
        s.add(psi_conn)
        s.add(phi_lib)
        for j, (inputs, output) in enumerate(list_inputs_outputs):
            s.add(output == poutputs[j])
            assert len(inputs) == len(pinputs[j])
            s.add([inputs[i] == pinputs[j][i] for i in range(len(inputs))])
        print(s)
        check = s.check() 
        if check != sat:
            return False
        l_values = s.model()

        # Lval2Prog
        p = Program(I_size, self.components)
        for c in p.components:
            for i in range(len(c.inputs)):
                c.inputs[i] = decode[int(str(l_values[L[c.inputs[i]]]))]
            c.output = decode[int(str(l_values[L[c.output]]))]
        p.components.sort()

        return p

    @staticmethod
    def append_number_variable(variable, number):
        return BitVec(f'{str(variable)}_{number}', BV_LENGTH)

    def fresh_variable(self, variable_character):
        self.variable_numbers[variable_character] += 1
        return BitVec(f'{variable_character}{self.variable_numbers[variable_character]}', BV_LENGTH)

    def fresh_l_variable(self):
        return self.fresh_variable('l')
    
    def fresh_i_variable(self): # for component inputs
        return self.fresh_variable('i')

    def fresh_I_variable(self): # for program inputs
        return self.fresh_variable('I')

    def fresh_o_variable(self):
        return self.fresh_variable('o')