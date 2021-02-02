from z3 import *
from constants import BV_LENGTH
from collections import Counter
from component import Component
import itertools
import operator

class Program:
    def __init__(self, prog_name='', num_prog_inputs=1, components=[]):
        self.prog_name = prog_name
        self.variable_numbers = Counter()
        self.prog_inputs = [self.fresh_I_variable() for _ in range(num_prog_inputs)]
        self.prog_output = self.fresh_O_variable()
        self.components = []
        for c in components:
            self.create_component(c.func, c.func_arity)
        self.update_values_based_on_components()

    def update_values_based_on_components(self, distinctl=False):
        self.P, self.R = [], []
        for c in self.components:
            self.P.extend(c.inputs)
            self.R.append(c.output)
        self.reset_l_variables()
        self.L = dict()
        for x in self.P + self.R:
            if distinctl:
                self.L[x] = self.fresh_l_variable()
            else:
                self.L[x] = self.fresh_l_variable_no_prefix()
        self.I_size = len(self.prog_inputs)
        self.M = self.I_size + len(self.components)

    def __str__(self):
        return '\n'.join(str(c) for c in self.components)

    def create_component(self, func, func_arity=2):
        input_vars = [self.fresh_i_variable() for _ in range(func_arity)]
        c = Component(input_vars, self.fresh_o_variable(), func, func_arity)
        self.components.append(c)
        return c

    def create_add_component(self):
        return self.create_component(operator.add)

    def create_and_component(self):
        return self.create_component(operator.and_)

    def create_xor_component(self):
        return self.create_component(operator.xor)

    def create_bitshiftright_component(self, shift_amount):
        return self.create_component(lambda x: x >> shift_amount, 1)

    def create_increment_component(self):
        return self.create_component(lambda x: x + 1, 1)

    def create_decrement_component(self):
        return self.create_component(lambda x: x - 1, 1)

    def distinct_constraint(self, list_inputs_outputs):
        dist_input = [self.fresh_d_variable() for _ in range(len(self.prog_inputs))]
        dist_output = BitVec('doutput1', BV_LENGTH)
        dist_output2 = BitVec('doutput2', BV_LENGTH)

        constraints = []
        constraints.append(dist_output != dist_output2)
        constraints += self.behave_constraints(list_inputs_outputs)
        constraints += self.generate_constraints(dist_input, dist_output)

        name = f'{self.prog_name}d_'
        p = Program(name, self.I_size, self.components)
        constraints += p.behave_constraints(list_inputs_outputs)
        constraints += p.generate_constraints(dist_input, dist_output2, distinctl=True)
        return constraints

    def behave_constraints(self, list_inputs_outputs):
        constraints = []
        self.update_values_based_on_components()
        for j, (inputs, output) in enumerate(list_inputs_outputs):
            name = f'{self.prog_name}{j}_'
            p = Program(name, self.I_size, self.components)
            constraints += p.generate_constraints(inputs, output)
        return constraints

    def solve_constraints(self, constraints):
        s = Solver()
        s.add(constraints)
        check = s.check()
        if check != sat:
            print('could not solve constraints')
            print(constraints)
            return False
        l_values = s.model()
        return l_values

    def generate_constraints(self, inputs, output, distinctl=False):
        self.update_values_based_on_components(distinctl)

        # syntactic well-formedness constraints
        psi_cons = []
        for x, y in itertools.combinations(self.R, 2):
            psi_cons.append(self.L[x] != self.L[y])
        psi_acyc = []
        for c in self.components:
            for x in c.inputs:
                psi_acyc.append(self.L[x] < self.L[c.output])
        psi_wfp = []
        for x in self.P:
            psi_wfp.append(0 <= self.L[x])
            psi_wfp.append(self.L[x] < self.M)
        for x in self.R:
            psi_wfp.append(self.I_size <= self.L[x])
            psi_wfp.append(self.L[x] < self.M)
        psi_wfp += psi_cons + psi_acyc

        # semantic constraints
        phi_lib = []
        for c in self.components:
            phi_lib.append(c.constraint())
        psi_conn = []
        for i, input in enumerate(self.prog_inputs):
            self.L[input] = i
        self.L[self.prog_output] = self.M - 1
        for x, y in itertools.combinations(self.P + self.R + self.prog_inputs + [self.prog_output], 2):
            psi_conn.append(Implies(self.L[x] == self.L[y], x == y))

        constraints = psi_wfp + phi_lib + psi_conn
        constraints.append(output == self.prog_output)
        assert len(inputs) == len(self.prog_inputs)
        constraints += [inputs[i] == self.prog_inputs[i] for i in range(len(inputs))]
        return constraints

    def l_values_to_prog(self, l_values):
        decode = dict() # maps integer l value to variable
        for i in range(self.I_size):
            decode[i] = self.prog_inputs[i]
        for i in range(self.I_size, self.M):
            decode[i] = self.R[i - self.I_size]

        p = Program(self.prog_name, self.I_size, self.components)
        for c in p.components:
            for i in range(len(c.inputs)):
                c.inputs[i] = decode[int(str(l_values[self.L[c.inputs[i]]]))]
            c.output = decode[int(str(l_values[self.L[c.output]]))]
        p.components.sort()
        return p

    def fresh_variable(self, variable_character):
        self.variable_numbers[variable_character] += 1
        return BitVec(f'{self.prog_name}{variable_character}{self.variable_numbers[variable_character]}', BV_LENGTH)

    def fresh_variable_no_prefix(self, variable_character):
        self.variable_numbers[variable_character] += 1
        return BitVec(f'{variable_character}{self.variable_numbers[variable_character]}', BV_LENGTH)

    def reset_l_variables(self):
        self.variable_numbers['l'] = 0

    def fresh_l_variable_no_prefix(self): # for l values
        return self.fresh_variable_no_prefix('l')

    def fresh_l_variable(self): # for distinct l values
        return self.fresh_variable('l')
    
    def fresh_i_variable(self): # for component inputs
        return self.fresh_variable('i')

    def fresh_I_variable(self): # for program inputs
        return self.fresh_variable('I')

    def fresh_o_variable(self): # for component outputs
        return self.fresh_variable('o')

    def fresh_O_variable(self): # for program outputs
        return self.fresh_variable('O')

    def fresh_d_variable(self): # for distinguishing constraints
        return self.fresh_variable_no_prefix('dinput')