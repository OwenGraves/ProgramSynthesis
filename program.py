from z3 import *
from constants import BV_LENGTH
from collections import Counter
from component import Component
from bit_vector_tests import bv
import itertools
import operator

class Program:
    def __init__(self, prog_name='', num_prog_inputs=1, components=[]):
        self.prog_name = prog_name
        self.variable_numbers = Counter()
        self.prog_inputs = [self.fresh_I_variable() for _ in range(num_prog_inputs)]
        self.prog_output = self.fresh_O_variable()
        self.components: list[Component] = []
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
                self.L[x] = self.fresh_d_l_variable_no_prefix()
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

    def create_subtract_component(self):
        return self.create_component(operator.sub)

    def create_and_component(self):
        return self.create_component(operator.and_)

    def create_or_component(self):
        return self.create_component(operator.or_)

    def create_xor_component(self):
        return self.create_component(operator.xor)

    def create_bitshiftright_component(self, shift_amount):
        if isinstance(shift_amount, int):
            shift_amount = bv(shift_amount)
        return self.create_component(lambda x: LShR(x, shift_amount), 1)

    def create_ule_component(self):
        return self.create_component(lambda x, y: If(ULE(x, y), BitVecVal(1, BV_LENGTH), BitVecVal(0, BV_LENGTH)))

    def create_negate_component(self):
        return self.create_component(lambda x: -x, 1)

    def create_not_component(self):
        return self.create_component(lambda x: ~x, 1)

    def create_increment_component(self):
        return self.create_component(lambda x: x + 1, 1)

    def create_decrement_component(self):
        return self.create_component(lambda x: x - 1, 1)

    def distinct_constraint(self, list_inputs_outputs):
        self.reset_dinput_variables()
        dist_input = [self.fresh_dinput_variable() for _ in range(len(self.prog_inputs))]
        dist_output = BitVec('doutput1', BV_LENGTH)
        dist_output2 = BitVec('doutput2', BV_LENGTH)

        constraints = []
        constraints.append(dist_output != dist_output2)
        constraints += self.behave_constraints(list_inputs_outputs + [(dist_input, dist_output)])

        name = f'{self.prog_name}d_'
        p = Program(name, self.I_size, self.components)
        constraints += p.behave_constraints(list_inputs_outputs + [(dist_input, dist_output2)], distinctl=True)
        return constraints

    def get_distinct_inputs(self, values):
        dinputs = []
        for i in range(1, len(self.prog_inputs) + 1):
            dinput = BitVec(f'dinput{i}', BV_LENGTH)
            dinputs.append(int(str(values[dinput])))
        return dinputs

    def behave_constraints(self, list_inputs_outputs, distinctl=False):
        constraints = []
        self.update_values_based_on_components()
        for j, (inputs, output) in enumerate(list_inputs_outputs):
            name = f'{self.prog_name}{j}_'
            p = Program(name, self.I_size, self.components)
            constraints += p.generate_constraints(inputs, output, distinctl)
        return constraints

    def solve_constraints(self, constraints, timeout=10000000):
        s = Solver()
        s.set('timeout', timeout)
        s.add(constraints)
        check = s.check()
        if check != sat:
            if check == unknown:
                print(f'Timed out after {timeout/1000} seconds.')
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

    def cull_unused_components(self):
        if len(self.components) == 0:
            return

        # delete unused components
        i = len(self.components) - 1
        used_o_vars = set()
        used_o_vars.add(self.components[i].output)
        while 0 <= i < len(self.components):
            c = self.components[i]
            if c.output in used_o_vars:
                used_o_vars.update(c.inputs)
                i -= 1
            else:
                del self.components[i]

        # renumber remaining outputs
        self.reset_o_variables()
        output_remapping = dict()
        for c in self.components:
            output_remapping[c.output] = self.fresh_o_variable()
        for c in self.components:
            if c.output in output_remapping:
                c.output = output_remapping[c.output]
            for i in range(len(c.inputs)):
                if c.inputs[i] in output_remapping:
                    c.inputs[i] = output_remapping[c.inputs[i]]
        return self

    def fresh_variable(self, variable_character):
        self.variable_numbers[variable_character] += 1
        return BitVec(f'{self.prog_name}{variable_character}{self.variable_numbers[variable_character]}', BV_LENGTH)

    def fresh_variable_no_prefix(self, variable_character):
        self.variable_numbers[variable_character] += 1
        return BitVec(f'{variable_character}{self.variable_numbers[variable_character]}', BV_LENGTH)

    def fresh_l_variable_no_prefix(self): # for l values
        return self.fresh_variable_no_prefix('l')

    def reset_l_variables(self):
        self.variable_numbers['l'] = 0

    def fresh_d_l_variable_no_prefix(self): # for distinct l values
        return self.fresh_variable_no_prefix('d_l')
    
    def fresh_i_variable(self): # for component inputs
        return self.fresh_variable('i')

    def fresh_I_variable(self): # for program inputs
        return self.fresh_variable('I')

    def fresh_o_variable(self): # for component outputs
        return self.fresh_variable('o')

    def reset_o_variables(self):
        self.variable_numbers['o'] = 0

    def fresh_O_variable(self): # for program outputs
        return self.fresh_variable('O')

    def fresh_dinput_variable(self): # for distinguishing constraints
        return self.fresh_variable_no_prefix('dinput')

    def reset_dinput_variables(self):
        self.variable_numbers['dinput'] = 0